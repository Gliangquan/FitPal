from ..common import *

@api.post("/fit/health/record")
@login_required
def fit_add_health_record():
    payload = request.get_json(silent=True) or {}
    if payload.get("weightKg") is None:
        raise BusinessException(ERR_PARAMS, "体重不能为空")

    record_date = parse_date(get_string(payload, "recordDate"), "recordDate") or date.today()
    with engine.begin() as conn:
        result = execute_sql(
            """
            INSERT INTO health_record (
                user_id, record_date, weight_kg, body_fat_rate,
                calorie_intake, calorie_burn, sleep_hours, note, is_delete
            ) VALUES (
                :user_id, :record_date, :weight_kg, :body_fat_rate,
                :calorie_intake, :calorie_burn, :sleep_hours, :note, 0
            )
            """,
            {
                "user_id": int(g.login_user["id"]),
                "record_date": record_date,
                "weight_kg": payload.get("weightKg"),
                "body_fat_rate": payload.get("bodyFatRate"),
                "calorie_intake": payload.get("calorieIntake"),
                "calorie_burn": payload.get("calorieBurn"),
                "sleep_hours": payload.get("sleepHours"),
                "note": get_string(payload, "note"),
            },
            conn,
        )
        badge_awarded = None
        calorie_burn_value = safe_float(payload.get("calorieBurn"))
        if calorie_burn_value is not None and calorie_burn_value > 0:
            week_start = record_date - timedelta(days=record_date.weekday())
            week_end = week_start + timedelta(days=6)
            weekly_count_row = query_one(
                """
                SELECT COUNT(DISTINCT record_date) AS cnt
                FROM health_record
                WHERE user_id = :uid
                  AND is_delete = 0
                  AND record_date >= :week_start
                  AND record_date <= :week_end
                  AND COALESCE(calorie_burn, 0) > 0
                """,
                {"uid": int(g.login_user["id"]), "week_start": week_start, "week_end": week_end},
                conn,
            )
            weekly_count = int((weekly_count_row or {}).get("cnt", 0))
            if weekly_count >= 3 and not exists_point_log(conn, int(g.login_user["id"]), "WEEKLY_EXERCISE_3", week_start):
                reward_result = add_task_points(
                    conn,
                    int(g.login_user["id"]),
                    "WEEKLY_EXERCISE_3",
                    "每周3次运动记录",
                    50,
                    week_start,
                    f"完成周运动记录任务（{week_start.isoformat()}~{week_end.isoformat()}）",
                    unique_per_day=False,
                )
                badge_awarded = reward_result.get("badge")
        row = query_one("SELECT * FROM health_record WHERE id = :id", {"id": result.lastrowid}, conn) or {}
        row["badgeAwarded"] = badge_awarded
        return success(row)


@api.get("/fit/health/records")
@login_required
def fit_list_health_records():
    days = request.args.get("days", default=30, type=int)
    days = max(days, 1)
    start = date.today() - timedelta(days=days)
    rows = query_all(
        """
        SELECT * FROM health_record
        WHERE user_id = :user_id AND is_delete = 0 AND record_date >= :start
        ORDER BY record_date DESC
        """,
        {"user_id": int(g.login_user["id"]), "start": start},
    )
    return success(rows)


@api.get("/fit/health/report")
@login_required
def fit_health_report():
    days = request.args.get("days", default=30, type=int)
    days = max(days, 1)
    start = date.today() - timedelta(days=days)
    rows = query_all(
        """
        SELECT * FROM health_record
        WHERE user_id = :user_id AND is_delete = 0 AND record_date >= :start
        ORDER BY record_date ASC
        """,
        {"user_id": int(g.login_user["id"]), "start": start},
    )

    result: Dict[str, Any] = {"records": rows}
    if not rows:
        result["summary"] = {"recordCount": 0}
        result["trendPrediction"] = None
        result["suggestions"] = ["数据不足，先连续记录 7 天健康数据后可获得趋势分析。"]
        return success(result)

    start_weight = Decimal(str(rows[0].get("weight_kg") or 0))
    end_weight = Decimal(str(rows[-1].get("weight_kg") or 0))
    delta = (end_weight - start_weight).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    body_fats = [Decimal(str(r.get("body_fat_rate"))) for r in rows if r.get("body_fat_rate") is not None]
    avg_body_fat = None
    if body_fats:
        avg = sum(body_fats, Decimal("0")) / Decimal(len(body_fats))
        avg_body_fat = avg.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    result["summary"] = {
        "recordCount": len(rows),
        "startWeight": start_weight,
        "endWeight": end_weight,
        "weightDelta": delta,
        "avgBodyFatRate": avg_body_fat,
    }
    trend_data = build_weight_trend(rows, horizon_days=7)
    result["trendPrediction"] = trend_data
    result["suggestions"] = build_health_suggestions(rows, trend_data)
    return success(result)


@api.post("/fit/questionnaire/submit")
@login_required
def fit_submit_questionnaire():
    payload = request.get_json(silent=True) or {}
    if payload.get("currentWeightKg") is None or payload.get("targetWeightKg") is None:
        raise BusinessException(ERR_PARAMS, "当前体重和目标体重不能为空")

    with engine.begin() as conn:
        result = execute_sql(
            """
            INSERT INTO user_questionnaire (
                user_id, age, gender, height_cm, current_weight_kg,
                target_weight_kg, goal_cycle_days, diet_preference,
                sport_preference, intensity, health_condition, answer_json, is_delete
            ) VALUES (
                :user_id, :age, :gender, :height_cm, :current_weight_kg,
                :target_weight_kg, :goal_cycle_days, :diet_preference,
                :sport_preference, :intensity, :health_condition, :answer_json, 0
            )
            """,
            {
                "user_id": int(g.login_user["id"]),
                "age": payload.get("age"),
                "gender": get_string(payload, "gender"),
                "height_cm": payload.get("heightCm"),
                "current_weight_kg": payload.get("currentWeightKg"),
                "target_weight_kg": payload.get("targetWeightKg"),
                "goal_cycle_days": payload.get("goalCycleDays"),
                "diet_preference": get_string(payload, "dietPreference"),
                "sport_preference": get_string(payload, "sportPreference"),
                "intensity": get_string(payload, "intensity"),
                "health_condition": get_string(payload, "healthCondition"),
                "answer_json": get_string(payload, "answerJson"),
            },
            conn,
        )
        reward_result = add_task_points(
            conn,
            int(g.login_user["id"]),
            "ASSESSMENT_COMPLETE",
            "完成减脂评估",
            100,
            date.today(),
            "完成问卷评估",
            unique_per_day=True,
        )
        row = query_one("SELECT * FROM user_questionnaire WHERE id = :id", {"id": result.lastrowid}, conn) or {}
        row["badgeAwarded"] = reward_result.get("badge")
        return success(row)


@api.post("/fit/plan/generate")
@login_required
def fit_generate_plan():
    user_id = int(g.login_user["id"])
    with engine.begin() as conn:
        questionnaire = query_one(
            """
            SELECT * FROM user_questionnaire
            WHERE user_id = :user_id AND is_delete = 0
            ORDER BY create_time DESC
            LIMIT 1
            """,
            {"user_id": user_id},
            conn,
        )
        if not questionnaire:
            raise BusinessException(ERR_PARAMS, "请先填写问卷")

        weight = questionnaire.get("current_weight_kg")
        if weight is None:
            record = query_one(
                """
                SELECT * FROM health_record
                WHERE user_id = :user_id AND is_delete = 0
                ORDER BY record_date DESC
                LIMIT 1
                """,
                {"user_id": user_id},
                conn,
            )
            weight = record.get("weight_kg") if record else None
        if weight is None:
            raise BusinessException(ERR_PARAMS, "请先记录体重")

        weight_dec = Decimal(str(weight))
        height_dec = Decimal(str(questionnaire.get("height_cm") or 170))
        age_val = int(questionnaire.get("age") or 30)
        gender = (questionnaire.get("gender") or "male").strip().lower()

        bmr = (
            weight_dec * Decimal("10")
            + height_dec * Decimal("6.25")
            - Decimal(age_val * 5)
            + (Decimal("-161") if gender == "female" else Decimal("5"))
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        target_calories = int(bmr - Decimal("500"))
        if target_calories < 1200:
            target_calories = 1200

        current_topic = find_current_or_recent_topic(conn)

        history_records = query_all(
            """
            SELECT record_date, weight_kg
            FROM health_record
            WHERE user_id = :user_id AND is_delete = 0
            ORDER BY record_date DESC
            LIMIT 60
            """,
            {"user_id": user_id},
            conn,
        )
        history_records = sorted(
            history_records,
            key=lambda item: item.get("record_date") if isinstance(item.get("record_date"), date) else str(item.get("record_date") or ""),
        )
        trend_data = build_weight_trend(history_records, horizon_days=7)
        source = "mifflin-st-jeor"
        if trend_data and int(trend_data.get("sampleSize") or 0) >= 4:
            slope = safe_float(trend_data.get("slopePerDayKg")) or 0.0
            if slope >= 0.05:
                target_calories -= 120
            elif slope <= -0.15:
                target_calories += 100
            source = "mifflin-st-jeor+linear-regression"
        if target_calories < 1200:
            target_calories = 1200

        diet_suggestion = f"每日热量控制在{target_calories}kcal；优先高蛋白、低GI碳水，避免含糖饮料。"
        if questionnaire.get("diet_preference"):
            diet_suggestion += f" 饮食偏好建议：{questionnaire.get('diet_preference')}。"
        workout_suggestion = "每周4-5次中等强度运动，结合有氧与力量训练。"
        if questionnaire.get("sport_preference"):
            workout_suggestion += f" 运动偏好建议：{questionnaire.get('sport_preference')}。"
        if questionnaire.get("intensity"):
            workout_suggestion += f" 当前建议强度：{questionnaire.get('intensity')}。"
        if current_topic:
            season_tips = f"{current_topic.get('title')}：{current_topic.get('routine_advice') or ''}"
        else:
            season_tips = "结合当前节气，保持规律作息与清淡饮食。"
        if trend_data and int(trend_data.get("sampleSize") or 0) >= 4:
            trend_text = trend_data.get("trend")
            if trend_text == "up":
                season_tips += " 近期体重趋势偏上，可增加有氧训练占比。"
            elif trend_text == "down_fast":
                season_tips += " 近期体重下降较快，请注意恢复和睡眠。"

        goal_cycle_days = int(questionnaire.get("goal_cycle_days") or 30)
        effective_from = date.today()
        effective_to = effective_from + timedelta(days=goal_cycle_days)

        result = execute_sql(
            """
            INSERT INTO personalized_plan (
                user_id, questionnaire_id, plan_type, bmr,
                daily_calorie_target, diet_suggestion, workout_suggestion,
                season_tips, source, effective_from, effective_to, is_delete
            ) VALUES (
                :user_id, :questionnaire_id, 'fat_loss', :bmr,
                :daily_calorie_target, :diet_suggestion, :workout_suggestion,
                :season_tips, :source, :effective_from, :effective_to, 0
            )
            """,
            {
                "user_id": user_id,
                "questionnaire_id": questionnaire.get("id"),
                "bmr": bmr,
                "daily_calorie_target": target_calories,
                "diet_suggestion": diet_suggestion,
                "workout_suggestion": workout_suggestion,
                "season_tips": season_tips,
                "source": source,
                "effective_from": effective_from,
                "effective_to": effective_to,
            },
            conn,
        )
        plan = query_one("SELECT * FROM personalized_plan WHERE id = :id", {"id": result.lastrowid}, conn)
        return success(plan)


@api.get("/fit/plan/latest")
@login_required
def fit_latest_plan():
    row = query_one(
        """
        SELECT * FROM personalized_plan
        WHERE user_id = :user_id AND is_delete = 0
        ORDER BY create_time DESC
        LIMIT 1
        """,
        {"user_id": int(g.login_user["id"])}
    )
    return success(row)


@api.get("/fit/season/topic/current")
def fit_current_season_topic():
    with engine.connect() as conn:
        current = query_one(
            """
            SELECT * FROM solar_term_topic
            WHERE status = 'published' AND is_delete = 0
              AND start_date <= :today AND end_date >= :today
            ORDER BY update_time DESC
            LIMIT 1
            """,
            {"today": date.today()},
            conn,
        )
        if current:
            return success(current)
        fallback = query_all(
            """
            SELECT * FROM solar_term_topic
            WHERE status = 'published' AND is_delete = 0
            ORDER BY update_time DESC
            LIMIT 3
            """,
            conn=conn,
        )
        if fallback:
            return success(fallback)
        solar_term_fallback = query_all(
            """
            SELECT * FROM solar_term
            WHERE status = 'published' AND is_delete = 0
            ORDER BY updated_at DESC, id DESC
            LIMIT 3
            """,
            conn=conn,
        )
        return success([normalize_solar_term_topic_row(item) for item in solar_term_fallback])


@api.get("/fit/content/recommend")
def fit_recommend_content():
    stage_tag = request.args.get("stageTag")
    stage_tag = stage_tag.strip().lower() if stage_tag else None
    limit = request.args.get("limit", default=8, type=int)
    limit = max(limit, 1)
    login_user = get_login_user(required=False)

    conditions = ["publish_status = 'published'", "is_delete = 0"]
    params: Dict[str, Any] = {"max_rows": max(limit * 10, 60)}
    if stage_tag:
        conditions.append("LOWER(stage_tag) = :stage_tag")
        params["stage_tag"] = stage_tag
    where_clause = " AND ".join(conditions)

    with engine.connect() as conn:
        rows = query_all(
            f"""
            SELECT * FROM recommendation_content
            WHERE {where_clause}
            ORDER BY create_time DESC
            LIMIT :max_rows
            """,
            params,
            conn,
        )
        if not rows:
            return success([])
        if not login_user:
            return success(rows[:limit])

        user_id = int(login_user["id"])
        questionnaire = query_one(
            """
            SELECT * FROM user_questionnaire
            WHERE user_id = :uid AND is_delete = 0
            ORDER BY create_time DESC
            LIMIT 1
            """,
            {"uid": user_id},
            conn,
        )
        recent_records = query_all(
            """
            SELECT record_date, weight_kg FROM health_record
            WHERE user_id = :uid AND is_delete = 0
            ORDER BY record_date ASC
            LIMIT 45
            """,
            {"uid": user_id},
            conn,
        )
        recent_posts = query_all(
            """
            SELECT category FROM community_post
            WHERE user_id = :uid AND is_delete = 0
            ORDER BY create_time DESC
            LIMIT 10
            """,
            {"uid": user_id},
            conn,
        )
        user_stage_tags = infer_stage_tags(questionnaire, recent_records)
        user_body_tags = infer_body_tags(questionnaire, recent_records)
        interest_tokens = collect_user_interest_tokens(login_user, questionnaire, recent_posts)

        scored: List[Tuple[float, Dict[str, Any]]] = []
        for item in rows:
            score = score_recommendation_content(item, stage_tag, user_stage_tags, user_body_tags, interest_tokens)
            enriched = dict(item)
            enriched["recommend_score"] = Decimal(str(score)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            scored.append((score, enriched))

        def create_time_sort_value(raw: Any) -> float:
            if isinstance(raw, datetime):
                return raw.timestamp()
            if isinstance(raw, date):
                return datetime.combine(raw, datetime.min.time()).timestamp()
            if raw is None:
                return 0.0
            text_value = str(raw).strip()
            if not text_value:
                return 0.0
            try:
                return datetime.fromisoformat(text_value).timestamp()
            except Exception:
                return 0.0

        scored.sort(key=lambda pair: (pair[0], create_time_sort_value(pair[1].get("create_time"))), reverse=True)
        return success([item for _, item in scored[:limit]])


@api.get("/fit/content/<int:content_id>")
def fit_content_detail(content_id: int):
    row = query_one("SELECT * FROM recommendation_content WHERE id = :id LIMIT 1", {"id": content_id})
    if not row or (row.get("is_delete") == 1):
        raise BusinessException(ERR_NOT_FOUND, "内容不存在")
    if row.get("publish_status") != "published":
        raise BusinessException(ERR_NO_AUTH, "内容未发布")
    return success(row)


@api.post("/fit/community/post")
@login_required
def fit_add_community_post():
    payload = request.get_json(silent=True) or {}
    title = get_string(payload, "title")
    content = get_string(payload, "content")
    if not title or not content:
        raise BusinessException(ERR_PARAMS, "标题和内容不能为空")

    with engine.begin() as conn:
        result = execute_sql(
            """
            INSERT INTO community_post (
                user_id, title, content, category, image_urls,
                like_count, comment_count, view_count, status, is_delete
            ) VALUES (
                :user_id, :title, :content, :category, :image_urls,
                0, 0, 0, 'published', 0
            )
            """,
            {
                "user_id": int(g.login_user["id"]),
                "title": title,
                "content": content,
                "category": get_string(payload, "category") or "weight-loss",
                "image_urls": get_string(payload, "imageUrls"),
            },
            conn,
        )
        reward_result = add_task_points(
            conn,
            int(g.login_user["id"]),
            "COMMUNITY_POST",
            "发布社区内容",
            30,
            date.today(),
            "发布社区帖子",
            unique_per_day=False,
        )
        row = query_one("SELECT * FROM community_post WHERE id = :id", {"id": result.lastrowid}, conn) or {}
        row["badgeAwarded"] = reward_result.get("badge")
        return success(row)


@api.get("/fit/community/posts")
def fit_list_community_posts():
    current = request.args.get("current", default=1, type=int)
    size = request.args.get("size", default=10, type=int)
    category = request.args.get("category")
    current = max(current, 1)
    size = max(size, 1)
    offset = (current - 1) * size

    conditions = ["is_delete = 0", "status = 'published'"]
    params: Dict[str, Any] = {"limit": size, "offset": offset}
    if category:
        conditions.append("category = :category")
        params["category"] = category
    where_clause = " AND ".join(conditions)

    total = int((query_one(f"SELECT COUNT(1) AS cnt FROM community_post WHERE {where_clause}", params) or {}).get("cnt", 0))
    with engine.connect() as conn:
        posts = query_all(
            f"SELECT * FROM community_post WHERE {where_clause} ORDER BY create_time DESC LIMIT :limit OFFSET :offset",
            params,
            conn,
        )
        records = [to_community_post_view(conn, post) for post in posts]
    return success(gen_page(records, total, current, size))


@api.get("/fit/community/post/<int:post_id>")
def fit_get_community_post_detail(post_id: int):
    with engine.begin() as conn:
        post = query_one("SELECT * FROM community_post WHERE id = :id LIMIT 1", {"id": post_id}, conn)
        if not post or post.get("is_delete") == 1 or post.get("status") != "published":
            raise BusinessException(ERR_NOT_FOUND, "帖子不存在")
        execute_sql(
            "UPDATE community_post SET view_count = :view_count, update_time = NOW() WHERE id = :id",
            {"view_count": int(post.get("view_count") or 0) + 1, "id": post_id},
            conn,
        )
        updated = query_one("SELECT * FROM community_post WHERE id = :id", {"id": post_id}, conn)
        return success(to_community_post_view(conn, updated))


@api.post("/fit/community/post/<int:post_id>/like")
@login_required
def fit_like_post(post_id: int):
    login_user_id = int(g.login_user["id"])
    with engine.begin() as conn:
        post = query_one("SELECT * FROM community_post WHERE id = :id LIMIT 1", {"id": post_id}, conn)
        if not post or post.get("is_delete") == 1 or post.get("status") != "published":
            raise BusinessException(ERR_NOT_FOUND, "帖子不存在")
        like_inserted = True
        try:
            already_liked = query_one(
                """
                SELECT id FROM community_post_like
                WHERE post_id = :post_id AND user_id = :user_id
                LIMIT 1
                """,
                {"post_id": post_id, "user_id": login_user_id},
                conn,
            )
            if already_liked:
                return success(True)
            execute_sql(
                """
                INSERT INTO community_post_like (post_id, user_id)
                VALUES (:post_id, :user_id)
                """,
                {"post_id": post_id, "user_id": login_user_id},
                conn,
            )
        except Exception:
            like_inserted = False
        execute_sql(
            "UPDATE community_post SET like_count = :like_count, update_time = NOW() WHERE id = :id",
            {"like_count": int(post.get("like_count") or 0) + 1, "id": post_id},
            conn,
        )
        add_task_points(
            conn,
            login_user_id,
            "COMMUNITY_LIKE",
            "社区点赞",
            1,
            date.today(),
            "点赞社区帖子",
            unique_per_day=True,
        )
        author_id = int(post.get("user_id") or 0)
        if author_id > 0 and author_id != login_user_id and like_inserted:
            add_task_points(
                conn,
                author_id,
                "POST_LIKED",
                "内容被赞",
                5,
                date.today(),
                f"社区帖子#{post_id}获得点赞",
                unique_per_day=False,
            )
        return success(True)


@api.post("/fit/community/post/<int:post_id>/comment")
@login_required
def fit_comment_post(post_id: int):
    payload = request.get_json(silent=True) or {}
    content = get_string(payload, "content")
    if not content:
        raise BusinessException(ERR_PARAMS, "评论内容不能为空")
    with engine.begin() as conn:
        post = query_one("SELECT * FROM community_post WHERE id = :id LIMIT 1", {"id": post_id}, conn)
        if not post or post.get("is_delete") == 1 or post.get("status") != "published":
            raise BusinessException(ERR_NOT_FOUND, "帖子不存在")
        execute_sql(
            """
            INSERT INTO community_comment (post_id, user_id, content, is_delete)
            VALUES (:post_id, :user_id, :content, 0)
            """,
            {
                "post_id": post_id,
                "user_id": int(g.login_user["id"]),
                "content": content,
            },
            conn,
        )
        execute_sql(
            "UPDATE community_post SET comment_count = :comment_count, update_time = NOW() WHERE id = :id",
            {"comment_count": int(post.get("comment_count") or 0) + 1, "id": post_id},
            conn,
        )
        add_task_points(
            conn,
            int(g.login_user["id"]),
            "COMMUNITY_COMMENT",
            "社区评论",
            2,
            date.today(),
            "评论社区帖子",
            unique_per_day=False,
        )
        return success(True)


@api.get("/fit/community/post/<int:post_id>/comments")
def fit_list_post_comments(post_id: int):
    size = request.args.get("size", default=20, type=int)
    size = max(size, 1)
    with engine.connect() as conn:
        post = query_one("SELECT * FROM community_post WHERE id = :id LIMIT 1", {"id": post_id}, conn)
        if not post or post.get("is_delete") == 1 or post.get("status") != "published":
            raise BusinessException(ERR_NOT_FOUND, "帖子不存在")
        comments = query_all(
            """
            SELECT * FROM community_comment
            WHERE post_id = :post_id AND is_delete = 0
            ORDER BY create_time DESC
            LIMIT :limit
            """,
            {"post_id": post_id, "limit": size},
            conn,
        )
        result = []
        for item in comments:
            user = query_one("SELECT * FROM user WHERE id = :id LIMIT 1", {"id": item.get("user_id")}, conn)
            user_name = safe_user_name(user, item.get("user_id"))
            user_avatar = user.get("user_avatar") if user else None
            result.append(
                {
                    "id": item.get("id"),
                    "postId": item.get("post_id"),
                    "userId": item.get("user_id"),
                    "content": item.get("content"),
                    "createTime": item.get("create_time"),
                    "authorName": user_name,
                    "userName": user_name,
                    "authorAvatar": user_avatar,
                    "userAvatar": user_avatar,
                }
            )
        return success(result)


@api.get("/fit/admin/community/posts")
@admin_required
def fit_admin_list_community_posts():
    status = request.args.get("status")
    category = request.args.get("category")
    keyword = request.args.get("keyword")
    current = request.args.get("current", default=1, type=int)
    size = request.args.get("size", default=20, type=int)
    current = max(current, 1)
    size = max(size, 1)
    offset = (current - 1) * size

    conditions = ["is_delete = 0"]
    params: Dict[str, Any] = {"limit": size, "offset": offset}
    if status:
        conditions.append("status = :status")
        params["status"] = status
    if category:
        conditions.append("category = :category")
        params["category"] = category
    if keyword:
        conditions.append("(title LIKE :keyword OR content LIKE :keyword)")
        params["keyword"] = f"%{keyword}%"
    where_clause = " AND ".join(conditions)

    total = int((query_one(f"SELECT COUNT(1) AS cnt FROM community_post WHERE {where_clause}", params) or {}).get("cnt", 0))
    with engine.connect() as conn:
        posts = query_all(
            f"SELECT * FROM community_post WHERE {where_clause} ORDER BY create_time DESC LIMIT :limit OFFSET :offset",
            params,
            conn,
        )
        records = [to_community_post_view(conn, post) for post in posts]
    return success(gen_page(records, total, current, size))


@api.post("/fit/admin/community/post/<int:post_id>/review")
@admin_required
def fit_admin_review_community_post(post_id: int):
    payload = request.get_json(silent=True) or {}
    action = get_string(payload, "action")
    if not action:
        raise BusinessException(ERR_PARAMS, "审核动作不能为空")

    mapping = {
        "publish": "published",
        "hide": "hidden",
        "reject": "rejected",
    }
    if action not in mapping:
        raise BusinessException(ERR_PARAMS, "不支持的审核动作")

    with engine.begin() as conn:
        post = query_one("SELECT * FROM community_post WHERE id = :id LIMIT 1", {"id": post_id}, conn)
        if not post or post.get("is_delete") == 1:
            raise BusinessException(ERR_NOT_FOUND, "帖子不存在")
        execute_sql(
            "UPDATE community_post SET status = :status, update_time = NOW() WHERE id = :id",
            {"status": mapping[action], "id": post_id},
            conn,
        )
        save_audit(
            conn,
            int(g.login_user["id"]),
            "community_post",
            int(post_id),
            action,
            get_string(payload, "reason") or "",
        )
        return success(True)


@api.post("/fit/points/checkin")
@login_required
def fit_points_checkin():
    user_id = int(g.login_user["id"])
    today = date.today()
    with engine.begin() as conn:
        reward_result = add_task_points(
            conn,
            user_id,
            "DAILY_CHECKIN",
            "每日打卡",
            10,
            today,
            "完成每日健康打卡",
            unique_per_day=True,
        )
        account = ensure_point_account(user_id, conn) or {}
        account["badgeAwarded"] = reward_result.get("badge")
        return success(account)


@api.get("/fit/points/me")
@login_required
def fit_points_me():
    user_id = int(g.login_user["id"])
    with engine.begin() as conn:
        account = ensure_point_account(user_id, conn)
        logs = query_all(
            """
            SELECT * FROM user_point_log
            WHERE user_id = :uid
            ORDER BY create_time DESC
            LIMIT 20
            """,
            {"uid": user_id},
            conn,
        )
        task_badges = []
        for item in query_all(
            """
            SELECT ub.id AS user_badge_id, ub.obtain_time, ub.source,
                   pb.id AS badge_id, pb.badge_code, pb.badge_name, pb.badge_desc, pb.icon_url,
                   pb.required_point
            FROM user_badge ub
            JOIN point_badge pb ON pb.id = ub.badge_id
            WHERE ub.user_id = :uid
              AND ub.is_delete = 0
              AND pb.is_delete = 0
              AND ub.source = 'task_reward'
            ORDER BY ub.obtain_time DESC
            """,
            {"uid": user_id},
            conn,
        ):
            rule = TASK_BADGE_RULES.get(str(item.get("badge_code") or ""), None)
            if rule is None:
                for task_code, task_rule in TASK_BADGE_RULES.items():
                    if task_rule.get("badge_code") == item.get("badge_code"):
                        rule = {**task_rule, "task_code": task_code}
                        break
            task_badges.append(
                {
                    "id": item.get("user_badge_id"),
                    "badgeId": item.get("badge_id"),
                    "badgeCode": item.get("badge_code"),
                    "badgeName": item.get("badge_name"),
                    "badgeDesc": item.get("badge_desc"),
                    "iconUrl": item.get("icon_url"),
                    "requiredPoint": item.get("required_point"),
                    "obtainTime": item.get("obtain_time"),
                    "source": item.get("source"),
                    "taskCode": rule.get("task_code") if rule else None,
                    "taskName": rule.get("task_name") if rule else None,
                    "taskDesc": rule.get("task_desc") if rule else None,
                }
            )
        return success({"account": account, "logs": logs, "taskBadges": task_badges})


@api.get("/fit/points/checkin/calendar")
@login_required
def fit_checkin_calendar():
    month_text = request.args.get("month")
    if month_text:
        try:
            year, month = month_text.split("-")
            year = int(year)
            month = int(month)
            month_start = date(year, month, 1)
        except Exception as exc:
            raise BusinessException(ERR_PARAMS, "月份格式错误，应为 yyyy-MM") from exc
    else:
        today = date.today()
        month_start = date(today.year, today.month, 1)

    if month_start.month == 12:
        month_end = date(month_start.year + 1, 1, 1) - timedelta(days=1)
    else:
        month_end = date(month_start.year, month_start.month + 1, 1) - timedelta(days=1)

    user_id = int(g.login_user["id"])
    rows = query_all(
        """
        SELECT * FROM user_point_log
        WHERE user_id = :uid
          AND task_code = 'DAILY_CHECKIN'
          AND biz_date >= :start_date
          AND biz_date <= :end_date
        ORDER BY biz_date ASC
        """,
        {"uid": user_id, "start_date": month_start, "end_date": month_end},
    )

    checkin_dates = []
    seen = set()
    for row in rows:
        biz_date = row.get("biz_date")
        if isinstance(biz_date, date):
            text_day = biz_date.isoformat()
        else:
            text_day = str(biz_date)
        if text_day not in seen:
            seen.add(text_day)
            checkin_dates.append(text_day)

    selected = [{"date": d, "info": "已打卡"} for d in checkin_dates]
    return success(
        {
            "month": month_start.strftime("%Y-%m"),
            "count": len(checkin_dates),
            "checkinDates": checkin_dates,
            "selected": selected,
            "todayChecked": date.today().isoformat() in seen,
        }
    )


@api.get("/fit/points/badges")
@login_required
def fit_list_badges():
    user_id = int(g.login_user["id"])
    with engine.begin() as conn:
        account = ensure_point_account(user_id, conn)
        available = int(account.get("available_point") or 0)
        badges = query_all(
            """
            SELECT * FROM point_badge
            WHERE is_delete = 0 AND status = 1
            ORDER BY required_point ASC
            """,
            conn=conn,
        )
        owned_rows = query_all(
            """
            SELECT badge_id FROM user_badge
            WHERE user_id = :uid AND is_delete = 0
            """,
            {"uid": user_id},
            conn,
        )
        owned_ids = {int(item["badge_id"]) for item in owned_rows if item.get("badge_id") is not None}
        result = []
        badge_alias_map = {
            "BADGE_001": {"badgeName": "自律打卡勋章", "badgeDesc": "首次完成每日健康打卡后自动获得。"},
            "BADGE_002": {"badgeName": "运动达标勋章", "badgeDesc": "同一周完成3次有效运动记录后自动获得。"},
            "BADGE_003": {"badgeName": "评估启程勋章", "badgeDesc": "首次完成减脂评估并生成方案后自动获得。"},
            "BADGE_004": {"badgeName": "社区分享勋章", "badgeDesc": "首次发布社区内容后自动获得。"},
        }
        for badge in badges:
            required = int(badge.get("required_point") or 0)
            owned = int(badge.get("id")) in owned_ids
            alias = badge_alias_map.get(str(badge.get("badge_code") or ""), {})
            result.append(
                {
                    "id": badge.get("id"),
                    "badgeCode": badge.get("badge_code"),
                    "badgeName": alias.get("badgeName") or badge.get("badge_name"),
                    "badgeDesc": alias.get("badgeDesc") or badge.get("badge_desc"),
                    "iconUrl": "/static/icon_fit/jiangbei.png" if alias else badge.get("icon_url"),
                    "requiredPoint": required,
                    "owned": owned,
                    "canExchange": (not owned) and available >= required,
                }
            )
        return success(result)


@api.get("/fit/points/badges/me")
@login_required
def fit_my_badges():
    user_id = int(g.login_user["id"])
    with engine.connect() as conn:
        rows = query_all(
            """
            SELECT * FROM user_badge
            WHERE user_id = :uid AND is_delete = 0
            ORDER BY obtain_time DESC
            """,
            {"uid": user_id},
            conn,
        )
        result = []
        for user_badge in rows:
            badge = query_one(
                "SELECT * FROM point_badge WHERE id = :id LIMIT 1",
                {"id": user_badge.get("badge_id")},
                conn,
            )
            if not badge or badge.get("is_delete") == 1:
                continue
            badge_alias_map = {
                "BADGE_001": {"badgeName": "自律打卡勋章", "badgeDesc": "首次完成每日健康打卡后自动获得。"},
                "BADGE_002": {"badgeName": "运动达标勋章", "badgeDesc": "同一周完成3次有效运动记录后自动获得。"},
                "BADGE_003": {"badgeName": "评估启程勋章", "badgeDesc": "首次完成减脂评估并生成方案后自动获得。"},
                "BADGE_004": {"badgeName": "社区分享勋章", "badgeDesc": "首次发布社区内容后自动获得。"},
            }
            alias = badge_alias_map.get(str(badge.get("badge_code") or ""), {})
            result.append(
                {
                    "id": user_badge.get("id"),
                    "badgeId": badge.get("id"),
                    "badgeCode": badge.get("badge_code"),
                    "badgeName": alias.get("badgeName") or badge.get("badge_name"),
                    "badgeDesc": alias.get("badgeDesc") or badge.get("badge_desc"),
                    "iconUrl": "/static/icon_fit/jiangbei.png" if alias else badge.get("icon_url"),
                    "requiredPoint": badge.get("required_point"),
                    "costPoint": user_badge.get("cost_point"),
                    "obtainTime": user_badge.get("obtain_time"),
                }
            )
        return success(result)


@api.post("/fit/points/badges/<int:badge_id>/exchange")
@login_required
def fit_exchange_badge(badge_id: int):
    user_id = int(g.login_user["id"])
    with engine.begin() as conn:
        badge = query_one("SELECT * FROM point_badge WHERE id = :id LIMIT 1", {"id": badge_id}, conn)
        if not badge or badge.get("is_delete") == 1 or int(badge.get("status") or 0) != 1:
            raise BusinessException(ERR_NOT_FOUND, "勋章不存在或不可兑换")

        owned = query_one(
            """
            SELECT COUNT(1) AS cnt FROM user_badge
            WHERE user_id = :uid AND badge_id = :bid AND is_delete = 0
            """,
            {"uid": user_id, "bid": badge_id},
            conn,
        )
        if int((owned or {}).get("cnt", 0)) > 0:
            raise BusinessException(ERR_OPERATION, "该勋章已兑换")

        account = ensure_point_account(user_id, conn)
        available = int(account.get("available_point") or 0)
        required = int(badge.get("required_point") or 0)
        if available < required:
            raise BusinessException(ERR_OPERATION, "积分不足")

        execute_sql(
            """
            UPDATE user_point_account
            SET available_point = :available_point, update_time = NOW()
            WHERE id = :id
            """,
            {
                "available_point": available - required,
                "id": account.get("id"),
            },
            conn,
        )
        execute_sql(
            """
            INSERT INTO user_badge (user_id, badge_id, cost_point, source, obtain_time, is_delete)
            VALUES (:uid, :bid, :cost_point, 'exchange', NOW(), 0)
            """,
            {"uid": user_id, "bid": badge_id, "cost_point": required},
            conn,
        )
        execute_sql(
            """
            INSERT INTO user_point_log (user_id, task_code, task_name, point_change, biz_date, remark)
            VALUES (:uid, 'BADGE_EXCHANGE', '勋章兑换', :point_change, :biz_date, :remark)
            """,
            {
                "uid": user_id,
                "point_change": -required,
                "biz_date": date.today(),
                "remark": f"兑换勋章：{badge.get('badge_name')}",
            },
            conn,
        )
        return success(
            {
                "badgeId": badge_id,
                "badgeName": badge.get("badge_name"),
                "costPoint": required,
                "availablePoint": available - required,
            }
        )


@api.post("/fit/coach/certification/apply")
@login_required
def fit_apply_coach_certification():
    payload = request.get_json(silent=True) or {}
    real_name = get_string(payload, "realName")
    certificate_type = get_string(payload, "certificateType")
    certificate_no = get_string(payload, "certificateNo")
    if not real_name or not certificate_type or not certificate_no:
        raise BusinessException(ERR_PARAMS, "请填写完整认证信息")

    user_id = int(g.login_user["id"])
    with engine.begin() as conn:
        profile = query_one(
            """
            SELECT * FROM coach_profile
            WHERE user_id = :uid AND is_delete = 0
            ORDER BY id DESC
            LIMIT 1
            """,
            {"uid": user_id},
            conn,
        )
        params = {
            "user_id": user_id,
            "real_name": real_name,
            "certificate_type": certificate_type,
            "certificate_no": certificate_no,
            "specialties": get_string(payload, "specialties"),
            "introduction": get_string(payload, "introduction"),
        }
        if not profile:
            result = execute_sql(
                """
                INSERT INTO coach_profile (
                    user_id, real_name, certificate_type, certificate_no,
                    specialties, introduction, status,
                    passed_time, reject_reason, is_delete
                ) VALUES (
                    :user_id, :real_name, :certificate_type, :certificate_no,
                    :specialties, :introduction, 'pending',
                    NULL, NULL, 0
                )
                """,
                params,
                conn,
            )
            profile_id = result.lastrowid
        else:
            execute_sql(
                """
                UPDATE coach_profile
                SET real_name = :real_name,
                    certificate_type = :certificate_type,
                    certificate_no = :certificate_no,
                    specialties = :specialties,
                    introduction = :introduction,
                    status = 'pending',
                    passed_time = NULL,
                    reject_reason = NULL,
                    update_time = NOW()
                WHERE id = :id
                """,
                {**params, "id": profile.get("id")},
                conn,
            )
            profile_id = profile.get("id")

        saved = query_one("SELECT * FROM coach_profile WHERE id = :id", {"id": profile_id}, conn)
        return success(saved)


@api.get("/fit/coach/certification/me")
@login_required
def fit_my_coach_certification():
    row = query_one(
        """
        SELECT * FROM coach_profile
        WHERE user_id = :uid AND is_delete = 0
        ORDER BY id DESC
        LIMIT 1
        """,
        {"uid": int(g.login_user["id"])}
    )
    return success(row)


@api.get("/fit/coach/my")
@login_required
def fit_my_coach():
    user_id = int(g.login_user["id"])
    with engine.connect() as conn:
        assigned = query_one(
            """
            SELECT * FROM coach_consultation
            WHERE user_id = :uid AND is_delete = 0 AND coach_user_id IS NOT NULL
            ORDER BY create_time DESC
            LIMIT 1
            """,
            {"uid": user_id},
            conn,
        )
        coach_user_id = assigned.get("coach_user_id") if assigned else None
        if coach_user_id is None:
            coach = query_one(
                """
                SELECT * FROM coach_profile
                WHERE status = 'approved' AND is_delete = 0
                ORDER BY update_time ASC
                LIMIT 1
                """,
                conn=conn,
            )
            coach_user_id = coach.get("user_id") if coach else None
        if coach_user_id is None:
            return success(None)

        profile = query_one(
            """
            SELECT * FROM coach_profile
            WHERE user_id = :uid AND status = 'approved' AND is_delete = 0
            ORDER BY id DESC
            LIMIT 1
            """,
            {"uid": coach_user_id},
            conn,
        )
        if not profile:
            return success(None)

        coach_user = query_one("SELECT * FROM user WHERE id = :id LIMIT 1", {"id": coach_user_id}, conn)
        reviews = query_all(
            "SELECT * FROM coach_review WHERE coach_user_id = :uid AND is_delete = 0",
            {"uid": coach_user_id},
            conn,
        )
        valid_ratings = [int(item.get("rating")) for item in reviews if item.get("rating") is not None]
        avg_rating = round(sum(valid_ratings) / len(valid_ratings), 1) if valid_ratings else 5.0

        students = query_all(
            "SELECT DISTINCT user_id FROM coach_consultation WHERE coach_user_id = :uid AND is_delete = 0",
            {"uid": coach_user_id},
            conn,
        )
        student_count = len(students)

        plan_count = int(
            (
                query_one(
                    """
                    SELECT COUNT(1) AS cnt FROM coach_consultation
                    WHERE coach_user_id = :uid AND status = 'replied' AND is_delete = 0
                    """,
                    {"uid": coach_user_id},
                    conn,
                )
                or {}
            ).get("cnt", 0)
        )

        passed_time = profile.get("passed_time")
        if isinstance(passed_time, datetime):
            experience = max(1, date.today().year - passed_time.year + 1)
        else:
            experience = 1

        result = {
            "id": coach_user_id,
            "name": profile.get("real_name") or safe_user_name(coach_user, coach_user_id),
            "avatar": coach_user.get("user_avatar") if coach_user else None,
            "rating": avg_rating,
            "certification": profile.get("certificate_type"),
            "planCount": plan_count,
            "studentCount": student_count,
            "experience": experience,
            "introduction": profile.get("introduction"),
            "specialties": profile.get("specialties"),
        }
        return success(result)


@api.post("/fit/coach/rate")
@login_required
def fit_rate_coach():
    payload = request.get_json(silent=True) or {}
    coach_id = get_required_long(payload, "coachId", "教练ID不能为空")
    rating = get_int(payload, "rating")
    content = get_required_string(payload, "content", "评价内容不能为空")
    if rating is None or rating < 1 or rating > 5:
        raise BusinessException(ERR_PARAMS, "评分范围为1-5")

    with engine.begin() as conn:
        coach = query_one(
            """
            SELECT * FROM coach_profile
            WHERE user_id = :uid AND status = 'approved' AND is_delete = 0
            LIMIT 1
            """,
            {"uid": coach_id},
            conn,
        )
        if not coach:
            raise BusinessException(ERR_NOT_FOUND, "教练不存在或未通过认证")
        execute_sql(
            """
            INSERT INTO coach_review (user_id, coach_user_id, rating, content, is_delete)
            VALUES (:user_id, :coach_user_id, :rating, :content, 0)
            """,
            {
                "user_id": int(g.login_user["id"]),
                "coach_user_id": coach_id,
                "rating": rating,
                "content": content,
            },
            conn,
        )
        return success(True)


@api.get("/fit/coach/reviews/my")
@login_required
def fit_my_coach_reviews():
    user_id = int(g.login_user["id"])
    with engine.connect() as conn:
        rows = query_all(
            """
            SELECT * FROM coach_review
            WHERE user_id = :uid AND is_delete = 0
            ORDER BY create_time DESC
            """,
            {"uid": user_id},
            conn,
        )
        result = []
        for item in rows:
            coach_user = query_one("SELECT * FROM user WHERE id = :id LIMIT 1", {"id": item.get("coach_user_id")}, conn)
            profile = query_one(
                """
                SELECT * FROM coach_profile
                WHERE user_id = :uid AND is_delete = 0
                ORDER BY id DESC
                LIMIT 1
                """,
                {"uid": item.get("coach_user_id")},
                conn,
            )
            coach_name = (
                profile.get("real_name")
                if profile and profile.get("real_name")
                else safe_user_name(coach_user, item.get("coach_user_id"))
            )
            result.append(
                {
                    "id": item.get("id"),
                    "coachId": item.get("coach_user_id"),
                    "coachName": coach_name,
                    "rating": item.get("rating"),
                    "content": item.get("content"),
                    "createTime": item.get("create_time"),
                }
            )
        return success(result)


@api.post("/fit/coach/consultation/create")
@login_required
def fit_create_consultation():
    payload = request.get_json(silent=True) or {}
    question = get_string(payload, "question")
    if not question:
        raise BusinessException(ERR_PARAMS, "咨询问题不能为空")

    coach_user_id = get_long(payload, "coachUserId")
    with engine.begin() as conn:
        if coach_user_id is None:
            coach = query_one(
                """
                SELECT * FROM coach_profile
                WHERE status = 'approved' AND is_delete = 0
                ORDER BY update_time ASC
                LIMIT 1
                """,
                conn=conn,
            )
            coach_user_id = coach.get("user_id") if coach else None
        result = execute_sql(
            """
            INSERT INTO coach_consultation (user_id, coach_user_id, question, status, is_delete)
            VALUES (:user_id, :coach_user_id, :question, 'pending', 0)
            """,
            {
                "user_id": int(g.login_user["id"]),
                "coach_user_id": coach_user_id,
                "question": question,
            },
            conn,
        )
        row = query_one("SELECT * FROM coach_consultation WHERE id = :id", {"id": result.lastrowid}, conn)
        return success(row)


@api.get("/fit/coach/consultations")
@login_required
def fit_my_consultations():
    rows = query_all(
        """
        SELECT * FROM coach_consultation
        WHERE user_id = :uid AND is_delete = 0
        ORDER BY create_time DESC
        """,
        {"uid": int(g.login_user["id"])},
    )
    return success(rows)


@api.get("/fit/coach/consultation/todo")
@login_required
def fit_todo_consultations():
    rows = query_all(
        """
        SELECT * FROM coach_consultation
        WHERE coach_user_id = :uid AND status = 'pending' AND is_delete = 0
        ORDER BY create_time ASC
        """,
        {"uid": int(g.login_user["id"])},
    )
    return success(rows)


@api.post("/fit/coach/consultation/<int:consultation_id>/reply")
@login_required
def fit_reply_consultation(consultation_id: int):
    payload = request.get_json(silent=True) or {}
    reply = get_string(payload, "reply")
    if not reply:
        raise BusinessException(ERR_PARAMS, "回复内容不能为空")

    with engine.begin() as conn:
        consultation = query_one(
            "SELECT * FROM coach_consultation WHERE id = :id LIMIT 1",
            {"id": consultation_id},
            conn,
        )
        if not consultation or consultation.get("is_delete") == 1:
            raise BusinessException(ERR_NOT_FOUND, "咨询不存在")
        if consultation.get("coach_user_id") != int(g.login_user["id"]):
            raise BusinessException(ERR_NO_AUTH, "仅指派教练可以回复")
        execute_sql(
            """
            UPDATE coach_consultation
            SET reply = :reply,
                status = 'replied',
                reply_time = NOW(),
                update_time = NOW()
            WHERE id = :id
            """,
            {"reply": reply, "id": consultation_id},
            conn,
        )
        return success(True)


@api.get("/fit/admin/coach/pending")
@admin_required
def fit_admin_pending_coach_applications():
    rows = query_all(
        """
        SELECT * FROM coach_profile
        WHERE status = 'pending' AND is_delete = 0
        ORDER BY create_time ASC
        """
    )
    return success(rows)


@api.post("/fit/admin/coach/<int:profile_id>/approve")
@admin_required
def fit_admin_approve_coach(profile_id: int):
    with engine.begin() as conn:
        profile = query_one("SELECT * FROM coach_profile WHERE id = :id LIMIT 1", {"id": profile_id}, conn)
        if not profile or profile.get("is_delete") == 1:
            raise BusinessException(ERR_NOT_FOUND, "认证申请不存在")
        execute_sql(
            """
            UPDATE coach_profile
            SET status = 'approved', passed_time = NOW(), reject_reason = NULL, update_time = NOW()
            WHERE id = :id
            """,
            {"id": profile_id},
            conn,
        )
        execute_sql(
            "UPDATE user SET user_role = 'coach', update_time = NOW() WHERE id = :id",
            {"id": profile.get("user_id")},
            conn,
        )
        save_audit(conn, int(g.login_user["id"]), "coach_profile", profile_id, "approve", "教练认证审核通过")
        return success(True)


@api.post("/fit/admin/coach/<int:profile_id>/reject")
@admin_required
def fit_admin_reject_coach(profile_id: int):
    reason = request.args.get("reason", "资质材料不符合要求")
    with engine.begin() as conn:
        profile = query_one("SELECT * FROM coach_profile WHERE id = :id LIMIT 1", {"id": profile_id}, conn)
        if not profile or profile.get("is_delete") == 1:
            raise BusinessException(ERR_NOT_FOUND, "认证申请不存在")
        execute_sql(
            """
            UPDATE coach_profile
            SET status = 'rejected', reject_reason = :reason, update_time = NOW()
            WHERE id = :id
            """,
            {"reason": reason, "id": profile_id},
            conn,
        )
        save_audit(conn, int(g.login_user["id"]), "coach_profile", profile_id, "reject", reason)
        return success(True)


@api.get("/fit/admin/dashboard")
@admin_required
def fit_admin_dashboard():
    with engine.connect() as conn:
        user_count = int((query_one("SELECT COUNT(1) AS cnt FROM user WHERE is_delete = 0", conn=conn) or {}).get("cnt", 0))
        coach_count = int((query_one("SELECT COUNT(1) AS cnt FROM user WHERE is_delete = 0 AND user_role = 'coach'", conn=conn) or {}).get("cnt", 0))
        health_log_count = int((query_one("SELECT COUNT(1) AS cnt FROM health_record WHERE is_delete = 0", conn=conn) or {}).get("cnt", 0))
        community_post_count = int((query_one("SELECT COUNT(1) AS cnt FROM community_post WHERE is_delete = 0", conn=conn) or {}).get("cnt", 0))

        coach_application_stats = {
            "pending": int((query_one("SELECT COUNT(1) AS cnt FROM coach_profile WHERE is_delete = 0 AND status = 'pending'", conn=conn) or {}).get("cnt", 0)),
            "approved": int((query_one("SELECT COUNT(1) AS cnt FROM coach_profile WHERE is_delete = 0 AND status = 'approved'", conn=conn) or {}).get("cnt", 0)),
            "rejected": int((query_one("SELECT COUNT(1) AS cnt FROM coach_profile WHERE is_delete = 0 AND status = 'rejected'", conn=conn) or {}).get("cnt", 0)),
        }
        content_stats = {
            "draft": int((query_one("SELECT COUNT(1) AS cnt FROM recommendation_content WHERE is_delete = 0 AND publish_status = 'draft'", conn=conn) or {}).get("cnt", 0)),
            "published": int((query_one("SELECT COUNT(1) AS cnt FROM recommendation_content WHERE is_delete = 0 AND publish_status = 'published'", conn=conn) or {}).get("cnt", 0)),
            "rejected": int((query_one("SELECT COUNT(1) AS cnt FROM recommendation_content WHERE is_delete = 0 AND publish_status = 'rejected'", conn=conn) or {}).get("cnt", 0)),
        }

        return success(
            {
                "userCount": user_count,
                "coachCount": coach_count,
                "healthLogCount": health_log_count,
                "communityPostCount": community_post_count,
                "coachApplicationStats": coach_application_stats,
                "contentStats": content_stats,
            }
        )


@api.get("/fit/admin/coach/applications")
@admin_required
def fit_admin_coach_applications_list():
    status = request.args.get("status")
    current = request.args.get("current", default=1, type=int)
    size = request.args.get("size", default=20, type=int)
    current = max(current, 1)
    size = max(size, 1)
    offset = (current - 1) * size

    conditions = ["is_delete = 0"]
    params: Dict[str, Any] = {"limit": size, "offset": offset}
    if status:
        conditions.append("status = :status")
        params["status"] = status
    where_clause = " AND ".join(conditions)

    total = int((query_one(f"SELECT COUNT(1) AS cnt FROM coach_profile WHERE {where_clause}", params) or {}).get("cnt", 0))
    rows = query_all(
        f"SELECT * FROM coach_profile WHERE {where_clause} ORDER BY create_time DESC LIMIT :limit OFFSET :offset",
        params,
    )
    return success(gen_page(rows, total, current, size))


@api.post("/fit/admin/coach/applications/add")
@admin_required
def fit_admin_coach_application_add():
    payload = request.get_json(silent=True) or {}
    user_id = get_required_long(payload, "userId", "用户ID不能为空")
    real_name = get_required_string(payload, "realName", "姓名不能为空")
    certificate_type = get_required_string(payload, "certificateType", "证书类型不能为空")
    certificate_no = get_required_string(payload, "certificateNo", "证书编号不能为空")
    status = get_string(payload, "status") or "pending"
    if status not in {"pending", "approved", "rejected"}:
        raise BusinessException(ERR_PARAMS, "状态不合法")

    with engine.begin() as conn:
        user = query_one("SELECT * FROM user WHERE id = :id LIMIT 1", {"id": user_id}, conn)
        if not user or user.get("is_delete") == 1:
            raise BusinessException(ERR_NOT_FOUND, "用户不存在")

        passed_time = now() if status == "approved" else None
        reject_reason = get_string(payload, "rejectReason") if status == "rejected" else None
        result = execute_sql(
            """
            INSERT INTO coach_profile (
                user_id, real_name, certificate_type, certificate_no,
                specialties, introduction, status,
                passed_time, reject_reason, is_delete
            ) VALUES (
                :user_id, :real_name, :certificate_type, :certificate_no,
                :specialties, :introduction, :status,
                :passed_time, :reject_reason, 0
            )
            """,
            {
                "user_id": user_id,
                "real_name": real_name,
                "certificate_type": certificate_type,
                "certificate_no": certificate_no,
                "specialties": get_string(payload, "specialties"),
                "introduction": get_string(payload, "introduction"),
                "status": status,
                "passed_time": passed_time,
                "reject_reason": reject_reason,
            },
            conn,
        )
        if status == "approved":
            execute_sql("UPDATE user SET user_role = 'coach', update_time = NOW() WHERE id = :id", {"id": user_id}, conn)

        profile_id = int(result.lastrowid)
        save_audit(conn, int(g.login_user["id"]), "coach_profile", profile_id, "add", "新增教练认证申请")
        return success(profile_id)


@api.post("/fit/admin/coach/applications/update")
@admin_required
def fit_admin_coach_application_update():
    payload = request.get_json(silent=True) or {}
    profile_id = get_required_long(payload, "id", "ID不能为空")

    with engine.begin() as conn:
        profile = query_one("SELECT * FROM coach_profile WHERE id = :id LIMIT 1", {"id": profile_id}, conn)
        if not profile or profile.get("is_delete") == 1:
            raise BusinessException(ERR_NOT_FOUND, "认证申请不存在")

        update_fields: Dict[str, Any] = {}
        if payload.get("userId") is not None:
            target_user_id = get_required_long(payload, "userId", "用户ID不能为空")
            target_user = query_one("SELECT * FROM user WHERE id = :id LIMIT 1", {"id": target_user_id}, conn)
            if not target_user or target_user.get("is_delete") == 1:
                raise BusinessException(ERR_NOT_FOUND, "用户不存在")
            update_fields["user_id"] = target_user_id

        if payload.get("realName") is not None:
            update_fields["real_name"] = get_required_string(payload, "realName", "姓名不能为空")
        if payload.get("certificateType") is not None:
            update_fields["certificate_type"] = get_required_string(payload, "certificateType", "证书类型不能为空")
        if payload.get("certificateNo") is not None:
            update_fields["certificate_no"] = get_required_string(payload, "certificateNo", "证书编号不能为空")
        if payload.get("specialties") is not None:
            update_fields["specialties"] = get_string(payload, "specialties")
        if payload.get("introduction") is not None:
            update_fields["introduction"] = get_string(payload, "introduction")
        if payload.get("rejectReason") is not None:
            update_fields["reject_reason"] = get_string(payload, "rejectReason")

        if payload.get("status") is not None:
            status = get_string(payload, "status")
            if status not in {"pending", "approved", "rejected"}:
                raise BusinessException(ERR_PARAMS, "状态不合法")
            update_fields["status"] = status
            if status == "approved":
                update_fields["passed_time"] = now()
                update_fields["reject_reason"] = None
                target_uid = int(update_fields.get("user_id") or profile.get("user_id"))
                execute_sql("UPDATE user SET user_role = 'coach', update_time = NOW() WHERE id = :id", {"id": target_uid}, conn)
            elif status == "pending":
                update_fields["passed_time"] = None
                update_fields["reject_reason"] = None
            else:
                update_fields["passed_time"] = None

        if update_fields:
            set_clause = ", ".join([f"{key} = :{key}" for key in update_fields.keys()])
            execute_sql(
                f"UPDATE coach_profile SET {set_clause}, update_time = NOW() WHERE id = :id",
                {**update_fields, "id": profile_id},
                conn,
            )
        save_audit(conn, int(g.login_user["id"]), "coach_profile", profile_id, "update", "更新教练认证申请")
        return success(True)


@api.post("/fit/admin/coach/applications/delete")
@admin_required
def fit_admin_coach_application_delete():
    payload = request.get_json(silent=True) or {}
    profile_id = get_required_long(payload, "id", "ID不能为空")

    with engine.begin() as conn:
        profile = query_one("SELECT * FROM coach_profile WHERE id = :id LIMIT 1", {"id": profile_id}, conn)
        if not profile or profile.get("is_delete") == 1:
            raise BusinessException(ERR_NOT_FOUND, "认证申请不存在")
        execute_sql(
            "UPDATE coach_profile SET is_delete = 1, update_time = NOW() WHERE id = :id",
            {"id": profile_id},
            conn,
        )
        save_audit(conn, int(g.login_user["id"]), "coach_profile", profile_id, "delete", "删除教练认证申请")
        return success(True)


@api.post("/fit/admin/coach/<int:profile_id>/review")
@admin_required
def fit_admin_coach_review(profile_id: int):
    payload = request.get_json(silent=True) or {}
    action = get_string(payload, "action")
    if not action:
        raise BusinessException(ERR_PARAMS, "审核动作不能为空")

    with engine.begin() as conn:
        profile = query_one("SELECT * FROM coach_profile WHERE id = :id LIMIT 1", {"id": profile_id}, conn)
        if not profile or profile.get("is_delete") == 1:
            raise BusinessException(ERR_NOT_FOUND, "认证申请不存在")

        if action == "approve":
            execute_sql(
                """
                UPDATE coach_profile
                SET status = 'approved', passed_time = NOW(), reject_reason = NULL, update_time = NOW()
                WHERE id = :id
                """,
                {"id": profile_id},
                conn,
            )
            execute_sql("UPDATE user SET user_role = 'coach', update_time = NOW() WHERE id = :id", {"id": profile.get("user_id")}, conn)
            save_audit(conn, int(g.login_user["id"]), "coach_profile", profile_id, "approve", "教练认证审核通过")
            return success(True)

        if action == "reject":
            reason = get_string(payload, "reason") or "资质材料不符合要求"
            execute_sql(
                """
                UPDATE coach_profile
                SET status = 'rejected', reject_reason = :reason, update_time = NOW()
                WHERE id = :id
                """,
                {"reason": reason, "id": profile_id},
                conn,
            )
            save_audit(conn, int(g.login_user["id"]), "coach_profile", profile_id, "reject", reason)
            return success(True)

        if action == "reopen":
            execute_sql(
                """
                UPDATE coach_profile
                SET status = 'pending', passed_time = NULL, reject_reason = NULL, update_time = NOW()
                WHERE id = :id
                """,
                {"id": profile_id},
                conn,
            )
            save_audit(conn, int(g.login_user["id"]), "coach_profile", profile_id, "reopen", "重新打开认证审核")
            return success(True)

        raise BusinessException(ERR_PARAMS, "不支持的审核动作")


@api.get("/fit/admin/contents")
@admin_required
def fit_admin_contents_list():
    status = request.args.get("status")
    current = request.args.get("current", default=1, type=int)
    size = request.args.get("size", default=20, type=int)
    current = max(current, 1)
    size = max(size, 1)
    offset = (current - 1) * size

    conditions = ["is_delete = 0"]
    params: Dict[str, Any] = {"limit": size, "offset": offset}
    if status:
        conditions.append("publish_status = :status")
        params["status"] = status
    where_clause = " AND ".join(conditions)

    total = int((query_one(f"SELECT COUNT(1) AS cnt FROM recommendation_content WHERE {where_clause}", params) or {}).get("cnt", 0))
    rows = query_all(
        f"SELECT * FROM recommendation_content WHERE {where_clause} ORDER BY create_time DESC LIMIT :limit OFFSET :offset",
        params,
    )
    return success(gen_page(rows, total, current, size))


@api.post("/fit/admin/contents/add")
@admin_required
def fit_admin_contents_add():
    payload = request.get_json(silent=True) or {}
    title = get_required_string(payload, "title", "标题不能为空")
    content_type = get_string(payload, "contentType") or "article"
    publish_status = get_string(payload, "publishStatus") or "draft"
    if publish_status not in {"draft", "published", "rejected"}:
        raise BusinessException(ERR_PARAMS, "发布状态不合法")

    with engine.begin() as conn:
        result = execute_sql(
            """
            INSERT INTO recommendation_content (
                title, content_type, stage_tag, body_tag,
                summary, content_url, content_body, tags,
                publish_status, is_delete
            ) VALUES (
                :title, :content_type, :stage_tag, :body_tag,
                :summary, :content_url, :content_body, :tags,
                :publish_status, 0
            )
            """,
            {
                "title": title,
                "content_type": content_type,
                "stage_tag": get_string(payload, "stageTag"),
                "body_tag": get_string(payload, "bodyTag"),
                "summary": get_string(payload, "summary"),
                "content_url": get_string(payload, "contentUrl"),
                "content_body": get_string(payload, "contentBody"),
                "tags": get_string(payload, "tags"),
                "publish_status": publish_status,
            },
            conn,
        )
        content_id = int(result.lastrowid)
        save_audit(conn, int(g.login_user["id"]), "recommendation_content", content_id, "add", "新增内容")
        return success(content_id)


@api.post("/fit/admin/contents/update")
@admin_required
def fit_admin_contents_update():
    payload = request.get_json(silent=True) or {}
    content_id = get_required_long(payload, "id", "ID不能为空")

    with engine.begin() as conn:
        content = query_one("SELECT * FROM recommendation_content WHERE id = :id LIMIT 1", {"id": content_id}, conn)
        if not content or content.get("is_delete") == 1:
            raise BusinessException(ERR_NOT_FOUND, "内容不存在")

        updates = {}
        mapping = {
            "title": "title",
            "contentType": "content_type",
            "stageTag": "stage_tag",
            "bodyTag": "body_tag",
            "summary": "summary",
            "contentUrl": "content_url",
            "contentBody": "content_body",
            "tags": "tags",
        }
        for src, dst in mapping.items():
            if src in payload:
                updates[dst] = get_string(payload, src)

        if "publishStatus" in payload:
            publish_status = get_string(payload, "publishStatus")
            if publish_status not in {"draft", "published", "rejected"}:
                raise BusinessException(ERR_PARAMS, "发布状态不合法")
            updates["publish_status"] = publish_status

        if updates:
            set_clause = ", ".join([f"{key} = :{key}" for key in updates.keys()])
            execute_sql(
                f"UPDATE recommendation_content SET {set_clause}, update_time = NOW() WHERE id = :id",
                {**updates, "id": content_id},
                conn,
            )
        save_audit(conn, int(g.login_user["id"]), "recommendation_content", content_id, "update", "更新内容")
        return success(True)


@api.post("/fit/admin/contents/delete")
@admin_required
def fit_admin_contents_delete():
    payload = request.get_json(silent=True) or {}
    content_id = get_required_long(payload, "id", "ID不能为空")
    with engine.begin() as conn:
        content = query_one("SELECT * FROM recommendation_content WHERE id = :id LIMIT 1", {"id": content_id}, conn)
        if not content or content.get("is_delete") == 1:
            raise BusinessException(ERR_NOT_FOUND, "内容不存在")
        execute_sql(
            "UPDATE recommendation_content SET is_delete = 1, update_time = NOW() WHERE id = :id",
            {"id": content_id},
            conn,
        )
        save_audit(conn, int(g.login_user["id"]), "recommendation_content", content_id, "delete", "删除内容")
        return success(True)


@api.post("/fit/admin/contents/<int:content_id>/review")
@admin_required
def fit_admin_contents_review(content_id: int):
    payload = request.get_json(silent=True) or {}
    action = get_string(payload, "action")
    if not action:
        raise BusinessException(ERR_PARAMS, "审核动作不能为空")

    status_mapping = {"publish": "published", "reject": "rejected", "reset": "draft"}
    if action not in status_mapping:
        raise BusinessException(ERR_PARAMS, "不支持的审核动作")

    with engine.begin() as conn:
        content = query_one("SELECT * FROM recommendation_content WHERE id = :id LIMIT 1", {"id": content_id}, conn)
        if not content or content.get("is_delete") == 1:
            raise BusinessException(ERR_NOT_FOUND, "内容不存在")

        execute_sql(
            "UPDATE recommendation_content SET publish_status = :status, update_time = NOW() WHERE id = :id",
            {"status": status_mapping[action], "id": content_id},
            conn,
        )
        save_audit(
            conn,
            int(g.login_user["id"]),
            "recommendation_content",
            content_id,
            action,
            get_string(payload, "reason") or "",
        )
        return success(True)


@api.get("/fit/coach/plans")
@coach_or_admin_required
def fit_coach_plans():
    status = request.args.get("status")
    user_id = request.args.get("userId", type=int)
    current = request.args.get("current", default=1, type=int)
    size = request.args.get("size", default=10, type=int)
    current = max(current, 1)
    size = max(size, 1)
    offset = (current - 1) * size

    conditions = ["is_delete = 0"]
    params: Dict[str, Any] = {"limit": size, "offset": offset}
    if user_id:
        conditions.append("user_id = :user_id")
        params["user_id"] = user_id
    if status == "coached":
        conditions.append("source = 'coach-optimize'")
    elif status == "system":
        conditions.append("source <> 'coach-optimize'")

    where_clause = " AND ".join(conditions)
    total = int((query_one(f"SELECT COUNT(1) AS cnt FROM personalized_plan WHERE {where_clause}", params) or {}).get("cnt", 0))

    with engine.connect() as conn:
        plans = query_all(
            f"SELECT * FROM personalized_plan WHERE {where_clause} ORDER BY create_time DESC LIMIT :limit OFFSET :offset",
            params,
            conn,
        )
        records = []
        for plan in plans:
            plan_user = query_one("SELECT * FROM user WHERE id = :id LIMIT 1", {"id": plan.get("user_id")}, conn)
            user_nickname = (
                plan_user.get("user_name")
                if plan_user and plan_user.get("user_name")
                else (plan_user.get("user_account") if plan_user else f"用户#{plan.get('user_id')}")
            )
            plan_status = "coached" if plan.get("source") == "coach-optimize" else "system"
            records.append(
                {
                    "id": plan.get("id"),
                    "userId": plan.get("user_id"),
                    "userNickname": user_nickname,
                    "targetCalories": plan.get("daily_calorie_target"),
                    "status": plan_status,
                    "createdAt": plan.get("create_time"),
                    "dietPlan": plan.get("diet_suggestion"),
                    "exercisePlan": plan.get("workout_suggestion"),
                    "lifestyleTips": plan.get("season_tips"),
                    "coachNote": "",
                }
            )

    return success({"records": records, "total": total, "current": current, "size": size})


@api.post("/fit/admin/plans/add")
@admin_required
def fit_admin_plans_add():
    payload = request.get_json(silent=True) or {}
    user_id = get_required_long(payload, "userId", "用户ID不能为空")

    with engine.begin() as conn:
        target_user = query_one("SELECT * FROM user WHERE id = :id LIMIT 1", {"id": user_id}, conn)
        if not target_user or target_user.get("is_delete") == 1:
            raise BusinessException(ERR_NOT_FOUND, "用户不存在")

        result = execute_sql(
            """
            INSERT INTO personalized_plan (
                user_id, questionnaire_id, plan_type, daily_calorie_target,
                diet_suggestion, workout_suggestion, season_tips,
                source, effective_from, effective_to, is_delete
            ) VALUES (
                :user_id, :questionnaire_id, :plan_type, :daily_calorie_target,
                :diet_suggestion, :workout_suggestion, :season_tips,
                :source, :effective_from, :effective_to, 0
            )
            """,
            {
                "user_id": user_id,
                "questionnaire_id": get_long(payload, "questionnaireId"),
                "plan_type": get_string(payload, "planType") or "fat_loss",
                "daily_calorie_target": get_int(payload, "targetCalories"),
                "diet_suggestion": get_string(payload, "dietPlan"),
                "workout_suggestion": get_string(payload, "exercisePlan"),
                "season_tips": get_string(payload, "lifestyleTips"),
                "source": get_string(payload, "source") or "admin-manual",
                "effective_from": parse_date(get_string(payload, "effectiveFrom"), "effectiveFrom"),
                "effective_to": parse_date(get_string(payload, "effectiveTo"), "effectiveTo"),
            },
            conn,
        )
        plan_id = int(result.lastrowid)
        save_audit(conn, int(g.login_user["id"]), "personalized_plan", plan_id, "add", "新增方案")
        return success(plan_id)


@api.post("/fit/admin/plans/update")
@admin_required
def fit_admin_plans_update():
    payload = request.get_json(silent=True) or {}
    plan_id = get_required_long(payload, "id", "ID不能为空")

    with engine.begin() as conn:
        plan = query_one("SELECT * FROM personalized_plan WHERE id = :id LIMIT 1", {"id": plan_id}, conn)
        if not plan or plan.get("is_delete") == 1:
            raise BusinessException(ERR_NOT_FOUND, "方案不存在")

        updates: Dict[str, Any] = {}
        if "userId" in payload:
            new_user_id = get_required_long(payload, "userId", "用户ID不能为空")
            target_user = query_one("SELECT * FROM user WHERE id = :id LIMIT 1", {"id": new_user_id}, conn)
            if not target_user or target_user.get("is_delete") == 1:
                raise BusinessException(ERR_NOT_FOUND, "用户不存在")
            updates["user_id"] = new_user_id
        if "questionnaireId" in payload:
            updates["questionnaire_id"] = get_long(payload, "questionnaireId")
        if "planType" in payload:
            updates["plan_type"] = get_string(payload, "planType")
        if "targetCalories" in payload:
            updates["daily_calorie_target"] = get_int(payload, "targetCalories")
        if "dietPlan" in payload:
            updates["diet_suggestion"] = get_string(payload, "dietPlan")
        if "exercisePlan" in payload:
            updates["workout_suggestion"] = get_string(payload, "exercisePlan")
        if "lifestyleTips" in payload:
            updates["season_tips"] = get_string(payload, "lifestyleTips")
        if "source" in payload:
            updates["source"] = get_string(payload, "source")
        if "effectiveFrom" in payload:
            updates["effective_from"] = parse_date(get_string(payload, "effectiveFrom"), "effectiveFrom")
        if "effectiveTo" in payload:
            updates["effective_to"] = parse_date(get_string(payload, "effectiveTo"), "effectiveTo")

        if updates:
            set_clause = ", ".join([f"{k} = :{k}" for k in updates.keys()])
            execute_sql(
                f"UPDATE personalized_plan SET {set_clause}, update_time = NOW() WHERE id = :id",
                {**updates, "id": plan_id},
                conn,
            )
        save_audit(conn, int(g.login_user["id"]), "personalized_plan", plan_id, "update", "更新方案")
        return success(True)


@api.post("/fit/admin/plans/delete")
@admin_required
def fit_admin_plans_delete():
    payload = request.get_json(silent=True) or {}
    plan_id = get_required_long(payload, "id", "ID不能为空")

    with engine.begin() as conn:
        plan = query_one("SELECT * FROM personalized_plan WHERE id = :id LIMIT 1", {"id": plan_id}, conn)
        if not plan or plan.get("is_delete") == 1:
            raise BusinessException(ERR_NOT_FOUND, "方案不存在")
        execute_sql(
            "UPDATE personalized_plan SET is_delete = 1, update_time = NOW() WHERE id = :id",
            {"id": plan_id},
            conn,
        )
        save_audit(conn, int(g.login_user["id"]), "personalized_plan", plan_id, "delete", "删除方案")
        return success(True)


@api.put("/fit/coach/plans/<int:plan_id>/optimize")
@coach_or_admin_required
def fit_optimize_plan(plan_id: int):
    payload = request.get_json(silent=True) or {}
    with engine.begin() as conn:
        plan = query_one("SELECT * FROM personalized_plan WHERE id = :id LIMIT 1", {"id": plan_id}, conn)
        if not plan or plan.get("is_delete") == 1:
            raise BusinessException(ERR_NOT_FOUND, "方案不存在")

        updates: Dict[str, Any] = {}
        diet_plan = get_string(payload, "dietPlan")
        exercise_plan = get_string(payload, "exercisePlan")
        lifestyle_tips = get_string(payload, "lifestyleTips")
        coach_note = get_string(payload, "coachNote")

        if diet_plan:
            updates["diet_suggestion"] = diet_plan
        if exercise_plan:
            updates["workout_suggestion"] = exercise_plan

        season_tips = lifestyle_tips if lifestyle_tips else plan.get("season_tips")
        if coach_note:
            season_tips = f"{season_tips}\n教练备注：{coach_note}" if season_tips else f"教练备注：{coach_note}"
        updates["season_tips"] = season_tips
        updates["source"] = "coach-optimize"

        set_clause = ", ".join([f"{k} = :{k}" for k in updates.keys()])
        execute_sql(
            f"UPDATE personalized_plan SET {set_clause}, update_time = NOW() WHERE id = :id",
            {**updates, "id": plan_id},
            conn,
        )
        save_audit(
            conn,
            int(g.login_user["id"]),
            "personalized_plan",
            plan_id,
            "coach_optimize",
            coach_note or "",
        )
        return success(True)
