from ..common import *

@api.post("/points/rule/list/page")
@admin_required
def points_rule_list_page():
    payload = request.get_json(silent=True) or {}
    current = int(payload.get("current", 1) or 1)
    page_size = int(payload.get("pageSize", 10) or 10)
    offset = (current - 1) * page_size

    conditions = ["is_delete = 0"]
    params: Dict[str, Any] = {"limit": page_size, "offset": offset}
    rule_type = get_string(payload, "ruleType")
    if rule_type:
        conditions.append("rule_type = :rule_type")
        params["rule_type"] = rule_type
    where_clause = " AND ".join(conditions)

    total_row = query_one(f"SELECT COUNT(1) AS cnt FROM points_rule WHERE {where_clause}", params)
    total = int((total_row or {}).get("cnt", 0))
    records = query_all(
        f"SELECT * FROM points_rule WHERE {where_clause} ORDER BY id DESC LIMIT :limit OFFSET :offset",
        params,
    )
    return success({"records": records, "total": total})


@api.post("/points/rule/add")
@admin_required
def points_rule_add():
    payload = request.get_json(silent=True) or {}
    rule_name = get_string(payload, "ruleName")
    if not rule_name:
        raise BusinessException(ERR_PARAMS, "请求参数错误")

    with engine.begin() as conn:
        result = execute_sql(
            """
            INSERT INTO points_rule (
                rule_name, rule_description, points, rule_type,
                enabled, created_at, updated_at, is_delete
            ) VALUES (
                :rule_name, :rule_description, :points, :rule_type,
                :enabled, NOW(), NOW(), 0
            )
            """,
            {
                "rule_name": rule_name,
                "rule_description": get_string(payload, "ruleDescription"),
                "points": get_int(payload, "points") or 0,
                "rule_type": get_string(payload, "ruleType"),
                "enabled": 1 if get_bool(payload, "enabled", True) else 0,
            },
            conn,
        )
        return success(result.lastrowid)


@api.post("/points/rule/update")
@admin_required
def points_rule_update():
    payload = request.get_json(silent=True) or {}
    rule_id = get_required_long(payload, "id", "请求参数错误")

    updates = {}
    if get_string(payload, "ruleName") is not None:
        updates["rule_name"] = get_string(payload, "ruleName")
    if get_string(payload, "ruleDescription") is not None:
        updates["rule_description"] = get_string(payload, "ruleDescription")
    if payload.get("points") is not None:
        updates["points"] = int(payload.get("points"))
    if get_string(payload, "ruleType") is not None:
        updates["rule_type"] = get_string(payload, "ruleType")
    if payload.get("enabled") is not None:
        updates["enabled"] = 1 if bool(payload.get("enabled")) else 0

    if not updates:
        return success(True)

    set_clause = ", ".join([f"{k} = :{k}" for k in updates])
    params = {**updates, "id": rule_id}
    with engine.begin() as conn:
        result = execute_sql(f"UPDATE points_rule SET {set_clause}, updated_at = NOW() WHERE id = :id", params, conn)
        if result.rowcount <= 0:
            raise BusinessException(ERR_OPERATION, "操作失败")
        return success(True)


@api.post("/points/rule/delete")
@admin_required
def points_rule_delete():
    payload = request.get_json(silent=True) or {}
    rule_id = get_required_long(payload, "id", "请求参数错误")
    with engine.begin() as conn:
        result = execute_sql(
            "UPDATE points_rule SET is_delete = 1, updated_at = NOW() WHERE id = :id",
            {"id": rule_id},
            conn,
        )
        if result.rowcount <= 0:
            raise BusinessException(ERR_OPERATION, "操作失败")
        return success(True)


@api.post("/points/user/list/page")
@admin_required
def user_points_list_page():
    payload = request.get_json(silent=True) or {}
    current = int(payload.get("current", 1) or 1)
    page_size = int(payload.get("pageSize", 10) or 10)
    offset = (current - 1) * page_size

    conditions = ["is_delete = 0"]
    params: Dict[str, Any] = {"limit": page_size, "offset": offset}
    if payload.get("userId") is not None:
        conditions.append("user_id = :user_id")
        params["user_id"] = int(payload.get("userId"))
    user_name = get_string(payload, "userName")
    if user_name:
        conditions.append("user_name LIKE :user_name")
        params["user_name"] = f"%{user_name}%"
    where_clause = " AND ".join(conditions)

    total = int((query_one(f"SELECT COUNT(1) AS cnt FROM user_points WHERE {where_clause}", params) or {}).get("cnt", 0))
    records = query_all(
        f"SELECT * FROM user_points WHERE {where_clause} ORDER BY total_points DESC LIMIT :limit OFFSET :offset",
        params,
    )
    return success({"records": records, "total": total})


@api.post("/points/user/adjust")
@admin_required
def adjust_user_points():
    payload = request.get_json(silent=True) or {}
    user_id = get_required_long(payload, "userId", "请求参数错误")
    adjust_points = get_int(payload, "adjustPoints")
    reason = get_string(payload, "reason")
    if adjust_points is None or not reason:
        raise BusinessException(ERR_PARAMS, "请求参数错误")

    with engine.begin() as conn:
        record = query_one(
            "SELECT * FROM user_points WHERE user_id = :user_id AND is_delete = 0 LIMIT 1",
            {"user_id": user_id},
            conn,
        )
        if not record:
            raise BusinessException(ERR_NOT_FOUND, "用户积分记录不存在")
        execute_sql(
            """
            UPDATE user_points
            SET total_points = :total_points, updated_at = NOW()
            WHERE id = :id
            """,
            {
                "total_points": int(record.get("total_points") or 0) + adjust_points,
                "id": record.get("id"),
            },
            conn,
        )
        return success(True)


@api.post("/content/list/page")
@admin_required
def content_list_page():
    payload = request.get_json(silent=True) or {}
    current = int(payload.get("current", 1) or 1)
    page_size = int(payload.get("pageSize", 10) or 10)
    offset = (current - 1) * page_size

    conditions = ["is_delete = 0"]
    params: Dict[str, Any] = {"limit": page_size, "offset": offset}
    content_type = get_string(payload, "contentType")
    status = get_string(payload, "status")
    title = get_string(payload, "title")
    if content_type:
        conditions.append("content_type = :content_type")
        params["content_type"] = content_type
    if status:
        conditions.append("status = :status")
        params["status"] = status
    if title:
        conditions.append("title LIKE :title")
        params["title"] = f"%{title}%"
    where_clause = " AND ".join(conditions)

    total = int((query_one(f"SELECT COUNT(1) AS cnt FROM content WHERE {where_clause}", params) or {}).get("cnt", 0))
    records = query_all(
        f"SELECT * FROM content WHERE {where_clause} ORDER BY created_at DESC LIMIT :limit OFFSET :offset",
        params,
    )
    return success({"records": records, "total": total})


@api.get("/content/get")
@admin_required
def content_get():
    content_id = request.args.get("id", type=int)
    if not content_id or content_id <= 0:
        raise BusinessException(ERR_PARAMS, "请求参数错误")
    row = query_one("SELECT * FROM content WHERE id = :id LIMIT 1", {"id": content_id})
    if not row or row.get("is_delete") == 1:
        raise BusinessException(ERR_NOT_FOUND, "请求数据不存在")
    return success(row)


@api.post("/content/add")
@admin_required
def content_add():
    payload = request.get_json(silent=True) or {}
    if not get_string(payload, "title"):
        raise BusinessException(ERR_PARAMS, "请求参数错误")
    with engine.begin() as conn:
        result = execute_sql(
            """
            INSERT INTO content (
                content_type, title, description, content, target_audience,
                tags, cover_image, status, recommend_score,
                created_at, updated_at, is_delete
            ) VALUES (
                :content_type, :title, :description, :content, :target_audience,
                :tags, :cover_image, :status, :recommend_score,
                NOW(), NOW(), 0
            )
            """,
            {
                "content_type": get_string(payload, "contentType") or "article",
                "title": get_string(payload, "title"),
                "description": get_string(payload, "description"),
                "content": get_string(payload, "content"),
                "target_audience": get_string(payload, "targetAudience"),
                "tags": get_string(payload, "tags"),
                "cover_image": get_string(payload, "coverImage"),
                "status": get_string(payload, "status") or "draft",
                "recommend_score": get_int(payload, "recommendScore") or 0,
            },
            conn,
        )
        return success(result.lastrowid)


@api.post("/content/update")
@admin_required
def content_update():
    payload = request.get_json(silent=True) or {}
    content_id = get_required_long(payload, "id", "请求参数错误")
    fields = {
        "content_type": get_string(payload, "contentType"),
        "title": get_string(payload, "title"),
        "description": get_string(payload, "description"),
        "content": get_string(payload, "content"),
        "target_audience": get_string(payload, "targetAudience"),
        "tags": get_string(payload, "tags"),
        "cover_image": get_string(payload, "coverImage"),
        "status": get_string(payload, "status"),
    }
    if payload.get("recommendScore") is not None:
        fields["recommend_score"] = int(payload.get("recommendScore"))
    update_fields = {k: v for k, v in fields.items() if v is not None}
    if not update_fields:
        return success(True)

    set_clause = ", ".join([f"{k} = :{k}" for k in update_fields])
    with engine.begin() as conn:
        result = execute_sql(
            f"UPDATE content SET {set_clause}, updated_at = NOW() WHERE id = :id",
            {**update_fields, "id": content_id},
            conn,
        )
        if result.rowcount <= 0:
            raise BusinessException(ERR_OPERATION, "操作失败")
        return success(True)


@api.post("/content/delete")
@admin_required
def content_delete():
    payload = request.get_json(silent=True) or {}
    content_id = get_required_long(payload, "id", "请求参数错误")
    with engine.begin() as conn:
        result = execute_sql(
            "UPDATE content SET is_delete = 1, updated_at = NOW() WHERE id = :id",
            {"id": content_id},
            conn,
        )
        if result.rowcount <= 0:
            raise BusinessException(ERR_OPERATION, "操作失败")
        return success(True)


@api.post("/content/publish")
@admin_required
def content_publish():
    payload = request.get_json(silent=True) or {}
    content_id = get_required_long(payload, "id", "请求参数错误")
    with engine.begin() as conn:
        result = execute_sql(
            "UPDATE content SET status = 'published', updated_at = NOW() WHERE id = :id",
            {"id": content_id},
            conn,
        )
        if result.rowcount <= 0:
            raise BusinessException(ERR_OPERATION, "操作失败")
        return success(True)


@api.post("/content/archive")
@admin_required
def content_archive():
    payload = request.get_json(silent=True) or {}
    content_id = get_required_long(payload, "id", "请求参数错误")
    with engine.begin() as conn:
        result = execute_sql(
            "UPDATE content SET status = 'archived', updated_at = NOW() WHERE id = :id",
            {"id": content_id},
            conn,
        )
        if result.rowcount <= 0:
            raise BusinessException(ERR_OPERATION, "操作失败")
        return success(True)


@api.post("/content/batch-delete")
@admin_required
def content_batch_delete():
    payload = request.get_json(silent=True) or {}
    ids = payload.get("ids") or []
    if not isinstance(ids, list) or not ids:
        raise BusinessException(ERR_PARAMS, "请求参数错误")
    valid_ids = [int(item) for item in ids if int(item) > 0]
    if not valid_ids:
        raise BusinessException(ERR_PARAMS, "请求参数错误")

    placeholders, in_params = build_in_clause(valid_ids, "cid")
    with engine.begin() as conn:
        result = execute_sql(
            f"UPDATE content SET is_delete = 1, updated_at = NOW() WHERE id IN ({placeholders})",
            in_params,
            conn,
        )
        return success(int(result.rowcount))


@api.post("/solar-term/list/page")
@admin_required
def solar_term_list_page():
    payload = request.get_json(silent=True) or {}
    current = int(payload.get("current", 1) or 1)
    page_size = int(payload.get("pageSize", 10) or 10)
    offset = (current - 1) * page_size

    conditions = ["is_delete = 0"]
    params: Dict[str, Any] = {"limit": page_size, "offset": offset}
    status = get_string(payload, "status")
    if status:
        conditions.append("status = :status")
        params["status"] = status
    where_clause = " AND ".join(conditions)

    total = int((query_one(f"SELECT COUNT(1) AS cnt FROM solar_term WHERE {where_clause}", params) or {}).get("cnt", 0))
    records = query_all(
        f"SELECT * FROM solar_term WHERE {where_clause} ORDER BY created_at DESC LIMIT :limit OFFSET :offset",
        params,
    )
    return success({"records": records, "total": total})


@api.get("/solar-term/get")
@admin_required
def solar_term_get():
    term_id = request.args.get("id", type=int)
    if not term_id or term_id <= 0:
        raise BusinessException(ERR_PARAMS, "请求参数错误")
    row = query_one("SELECT * FROM solar_term WHERE id = :id LIMIT 1", {"id": term_id})
    if not row or row.get("is_delete") == 1:
        raise BusinessException(ERR_NOT_FOUND, "请求数据不存在")
    return success(row)


@api.post("/solar-term/add")
@admin_required
def solar_term_add():
    payload = request.get_json(silent=True) or {}
    if not get_string(payload, "title"):
        raise BusinessException(ERR_PARAMS, "请求参数错误")
    start_date_text = get_string(payload, "startDate")
    end_date_text = get_string(payload, "endDate")
    with engine.begin() as conn:
        result = execute_sql(
            """
            INSERT INTO solar_term (
                solar_term_name, title, description,
                day1_recipe, day2_recipe, day3_recipe,
                exercise_guide, lifestyle_advice, health_knowledge,
                cover_image, status, created_at, updated_at, is_delete
            ) VALUES (
                :solar_term_name, :title, :description,
                :day1_recipe, :day2_recipe, :day3_recipe,
                :exercise_guide, :lifestyle_advice, :health_knowledge,
                :cover_image, :status, NOW(), NOW(), 0
            )
            """,
            {
                "solar_term_name": get_string(payload, "solarTermName"),
                "title": get_string(payload, "title"),
                "description": get_string(payload, "description"),
                "day1_recipe": get_string(payload, "day1Recipe"),
                "day2_recipe": get_string(payload, "day2Recipe"),
                "day3_recipe": get_string(payload, "day3Recipe"),
                "exercise_guide": get_string(payload, "exerciseGuide"),
                "lifestyle_advice": get_string(payload, "lifestyleAdvice"),
                "health_knowledge": get_string(payload, "healthKnowledge"),
                "cover_image": get_string(payload, "coverImage"),
                "status": get_string(payload, "status") or "draft",
            },
            conn,
        )
        term_id = int(result.lastrowid)
        sync_solar_term_topic(conn, term_id, start_date_text=start_date_text, end_date_text=end_date_text)
        return success(term_id)


@api.post("/solar-term/update")
@admin_required
def solar_term_update():
    payload = request.get_json(silent=True) or {}
    term_id = get_required_long(payload, "id", "请求参数错误")
    start_date_text = get_string(payload, "startDate")
    end_date_text = get_string(payload, "endDate")
    fields = {
        "solar_term_name": get_string(payload, "solarTermName"),
        "title": get_string(payload, "title"),
        "description": get_string(payload, "description"),
        "day1_recipe": get_string(payload, "day1Recipe"),
        "day2_recipe": get_string(payload, "day2Recipe"),
        "day3_recipe": get_string(payload, "day3Recipe"),
        "exercise_guide": get_string(payload, "exerciseGuide"),
        "lifestyle_advice": get_string(payload, "lifestyleAdvice"),
        "health_knowledge": get_string(payload, "healthKnowledge"),
        "cover_image": get_string(payload, "coverImage"),
        "status": get_string(payload, "status"),
    }
    update_fields = {k: v for k, v in fields.items() if v is not None}
    if not update_fields:
        return success(True)

    set_clause = ", ".join([f"{k} = :{k}" for k in update_fields])
    with engine.begin() as conn:
        result = execute_sql(
            f"UPDATE solar_term SET {set_clause}, updated_at = NOW() WHERE id = :id",
            {**update_fields, "id": term_id},
            conn,
        )
        if result.rowcount <= 0:
            raise BusinessException(ERR_OPERATION, "操作失败")
        sync_solar_term_topic(conn, term_id, start_date_text=start_date_text, end_date_text=end_date_text)
        return success(True)


@api.post("/solar-term/delete")
@admin_required
def solar_term_delete():
    payload = request.get_json(silent=True) or {}
    term_id = get_required_long(payload, "id", "请求参数错误")
    with engine.begin() as conn:
        result = execute_sql(
            "UPDATE solar_term SET is_delete = 1, updated_at = NOW() WHERE id = :id",
            {"id": term_id},
            conn,
        )
        if result.rowcount <= 0:
            raise BusinessException(ERR_OPERATION, "操作失败")
        sync_solar_term_topic(conn, term_id, force_delete=True)
        return success(True)


@api.post("/solar-term/publish")
@admin_required
def solar_term_publish():
    payload = request.get_json(silent=True) or {}
    term_id = get_required_long(payload, "id", "请求参数错误")
    start_date_text = get_string(payload, "startDate")
    end_date_text = get_string(payload, "endDate")
    with engine.begin() as conn:
        result = execute_sql(
            "UPDATE solar_term SET status = 'published', updated_at = NOW() WHERE id = :id",
            {"id": term_id},
            conn,
        )
        if result.rowcount <= 0:
            raise BusinessException(ERR_OPERATION, "操作失败")
        sync_solar_term_topic(conn, term_id, start_date_text=start_date_text, end_date_text=end_date_text)
        return success(True)


def get_user_settings_record(conn: Connection, user_id: int) -> Dict[str, Any]:
    row = query_one(
        "SELECT * FROM user_settings WHERE user_id = :user_id AND is_delete = 0 LIMIT 1",
        {"user_id": user_id},
        conn,
    )
    if row:
        return row
    execute_sql(
        """
        INSERT INTO user_settings (
            user_id,
            checkin_reminder_enabled,
            community_notification_enabled,
            weekly_report_notification_enabled,
            coach_reply_notification_enabled,
            health_data_visible,
            profile_visible,
            consultation_data_retention_days,
            create_time,
            update_time,
            is_delete
        ) VALUES (
            :user_id,
            1, 1, 1, 1,
            0, 1, 30,
            NOW(), NOW(), 0
        )
        """,
        {"user_id": user_id},
        conn,
    )
    return (
        query_one(
            "SELECT * FROM user_settings WHERE user_id = :user_id AND is_delete = 0 LIMIT 1",
            {"user_id": user_id},
            conn,
        )
        or {}
    )


@api.get("/user-settings/get")
def user_settings_get():
    user_id = request.args.get("userId", type=int)
    if not user_id:
        return error(ERR_PARAMS, "查询失败")
    try:
        with engine.begin() as conn:
            settings = get_user_settings_record(conn, user_id)
            return success(settings)
    except Exception:
        return error(ERR_PARAMS, "查询失败")


@api.post("/user-settings/notification/update")
def user_settings_notification_update():
    user_id = request.args.get("userId", type=int)
    payload = request.get_json(silent=True) or {}
    if not user_id:
        return error(ERR_PARAMS, "更新失败")
    try:
        with engine.begin() as conn:
            settings = get_user_settings_record(conn, user_id)
            execute_sql(
                """
                UPDATE user_settings
                SET checkin_reminder_enabled = :checkin,
                    community_notification_enabled = :community,
                    weekly_report_notification_enabled = :weekly,
                    coach_reply_notification_enabled = :coach,
                    update_time = NOW()
                WHERE id = :id
                """,
                {
                    "checkin": int(payload.get("checkinReminderEnabled", settings.get("checkin_reminder_enabled", 1))),
                    "community": int(payload.get("communityNotificationEnabled", settings.get("community_notification_enabled", 1))),
                    "weekly": int(payload.get("weeklyReportNotificationEnabled", settings.get("weekly_report_notification_enabled", 1))),
                    "coach": int(payload.get("coachReplyNotificationEnabled", settings.get("coach_reply_notification_enabled", 1))),
                    "id": settings.get("id"),
                },
                conn,
            )
            return success("更新成功")
    except Exception:
        return error(ERR_PARAMS, "更新失败")


@api.post("/user-settings/privacy/update")
def user_settings_privacy_update():
    user_id = request.args.get("userId", type=int)
    payload = request.get_json(silent=True) or {}
    if not user_id:
        return error(ERR_PARAMS, "更新失败")
    try:
        with engine.begin() as conn:
            settings = get_user_settings_record(conn, user_id)
            execute_sql(
                """
                UPDATE user_settings
                SET health_data_visible = :health,
                    profile_visible = :profile,
                    consultation_data_retention_days = :retention,
                    update_time = NOW()
                WHERE id = :id
                """,
                {
                    "health": int(payload.get("healthDataVisible", settings.get("health_data_visible", 0))),
                    "profile": int(payload.get("profileVisible", settings.get("profile_visible", 1))),
                    "retention": int(payload.get("consultationDataRetentionDays", settings.get("consultation_data_retention_days", 30))),
                    "id": settings.get("id"),
                },
                conn,
            )
            return success("更新成功")
    except Exception:
        return error(ERR_PARAMS, "更新失败")


@api.post("/file/upload")
@login_required
def upload_file():
    file = request.files.get("file")
    biz = request.form.get("biz", "user_avatar")
    if biz not in ("user_avatar", "community_post", "content_cover"):
        raise BusinessException(ERR_PARAMS, "业务类型错误")
    if not file:
        raise BusinessException(ERR_PARAMS, "文件不能为空")
    validate_upload_file(file, biz)

    original_name = sanitize_filename(file.filename or "unknown")
    random_name = "".join(random.choices(string.ascii_letters + string.digits, k=8)) + "-" + original_name

    user_id = int(g.login_user["id"])
    minio = ensure_minio_ready()
    bucket_name, _ = get_bucket_and_prefix_by_biz(biz)
    object_name = build_minio_object_name(biz, user_id, random_name)
    file.stream.seek(0, os.SEEK_END)
    file_size = file.stream.tell()
    file.stream.seek(0)

    content_type = file.content_type or "application/octet-stream"
    try:
        minio.put_object(
            bucket_name,
            object_name,
            file.stream,
            length=file_size,
            content_type=content_type,
        )
    except S3Error as exc:
        logger.error("minio upload failed: %s", exc)
        raise BusinessException(ERR_SYSTEM, "文件上传失败") from exc

    file_url = f"/api/file/preview/{biz}/{user_id}/{random_name}"
    return success(file_url)


@api.get("/file/download/<biz>/<int:user_id>/<path:filename>")
def download_file(biz: str, user_id: int, filename: str):
    safe_name = sanitize_filename(filename)
    minio = ensure_minio_ready()
    bucket_name, _ = get_bucket_and_prefix_by_biz(biz)
    object_name = build_minio_object_name(biz, user_id, safe_name)
    obj = None
    try:
        obj = minio.get_object(bucket_name, object_name)
        file_bytes = obj.read()
        content_type = obj.headers.get("Content-Type", "application/octet-stream")
    except S3Error as exc:
        if exc.code in ("NoSuchKey", "NoSuchObject", "NoSuchBucket"):
            raise BusinessException(ERR_NOT_FOUND, "文件未找到") from exc
        logger.error("minio download failed: %s", exc)
        raise BusinessException(ERR_SYSTEM, "文件下载失败") from exc
    finally:
        if obj is not None:
            try:
                obj.close()
                obj.release_conn()
            except Exception:
                pass
    return send_file(
        io.BytesIO(file_bytes),
        mimetype=content_type,
        as_attachment=True,
        download_name=safe_name,
    )


@api.get("/file/preview/<biz>/<int:user_id>/<path:filename>")
def preview_file(biz: str, user_id: int, filename: str):
    safe_name = sanitize_filename(filename)
    minio = ensure_minio_ready()
    bucket_name, _ = get_bucket_and_prefix_by_biz(biz)
    object_name = build_minio_object_name(biz, user_id, safe_name)
    obj = None
    try:
        obj = minio.get_object(bucket_name, object_name)
        file_bytes = obj.read()
        content_type = obj.headers.get("Content-Type", "application/octet-stream")
    except S3Error as exc:
        if exc.code in ("NoSuchKey", "NoSuchObject", "NoSuchBucket"):
            raise BusinessException(ERR_NOT_FOUND, "文件未找到") from exc
        logger.error("minio preview failed: %s", exc)
        raise BusinessException(ERR_SYSTEM, "文件预览失败") from exc
    finally:
        if obj is not None:
            try:
                obj.close()
                obj.release_conn()
            except Exception:
                pass
    return send_file(io.BytesIO(file_bytes), mimetype=content_type)

