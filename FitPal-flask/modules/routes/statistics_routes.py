from ..common import *

@api.get("/statistics/overview")
@admin_required
def statistics_overview():
    with engine.connect() as conn:
        stats = get_user_statistics_data(conn)
        certified_coaches = int(
            (
                query_one(
                    """
                    SELECT COUNT(1) AS cnt FROM coach_profile
                    WHERE status = 'approved' AND is_delete = 0
                    """,
                    conn=conn,
                )
                or {}
            ).get("cnt", 0)
        )
        recommendation_count = int(
            (
                query_one(
                    """
                    SELECT COUNT(1) AS cnt FROM recommendation_content
                    WHERE is_delete = 0 AND publish_status = 'published'
                    """,
                    conn=conn,
                )
                or {}
            ).get("cnt", 0)
        )
        community_count = int(
            (
                query_one(
                    """
                    SELECT COUNT(1) AS cnt FROM community_post
                    WHERE is_delete = 0 AND status = 'published'
                    """,
                    conn=conn,
                )
                or {}
            ).get("cnt", 0)
        )
        return success(
            {
                "totalUsers": stats["totalUsers"],
                "activeUsers": stats["activeUsers"],
                "certifiedCoaches": certified_coaches,
                "communityContent": recommendation_count + community_count,
            }
        )


@api.post("/statistics/user-growth")
@admin_required
def statistics_user_growth():
    days = recent_days(7)
    start_day = days[0]
    with engine.connect() as conn:
        base_total = int(
            (
                query_one(
                    """
                    SELECT COUNT(1) AS cnt FROM user
                    WHERE is_delete = 0 AND DATE(create_time) < :start_day
                    """,
                    {"start_day": start_day},
                    conn,
                )
                or {}
            ).get("cnt", 0)
        )
        increments = query_all(
            """
            SELECT DATE(create_time) AS day, COUNT(1) AS cnt
            FROM user
            WHERE is_delete = 0
              AND DATE(create_time) >= :start_day
              AND DATE(create_time) <= :end_day
            GROUP BY DATE(create_time)
            """,
            {"start_day": start_day, "end_day": days[-1]},
            conn,
        )
        inc_map = {(row["day"].isoformat() if isinstance(row["day"], date) else str(row["day"])): int(row["cnt"]) for row in increments}
        running = base_total
        result = []
        for item in days:
            day_text = item.isoformat()
            running += inc_map.get(day_text, 0)
            result.append({"date": day_text, "totalUsers": running})
        return success(result)


@api.get("/statistics/user-role-distribution")
@admin_required
def statistics_user_role_distribution():
    with engine.connect() as conn:
        rows = query_all(
            """
            SELECT user_role, COUNT(1) AS cnt
            FROM user
            WHERE is_delete = 0
            GROUP BY user_role
            """,
            conn=conn,
        )
        label_map = {"user": "普通用户", "coach": "认证教练", "admin": "管理员", "ban": "封禁用户"}
        result = []
        for row in rows:
            role_value = str(row.get("user_role") or "unknown")
            result.append({"role": label_map.get(role_value, role_value), "count": int(row.get("cnt") or 0)})
        return success(result)


@api.post("/statistics/daily-active")
@admin_required
def statistics_daily_active():
    days = recent_days(7)
    with engine.connect() as conn:
        active_map = load_daily_active_user_counts(conn, days)
        result = [{"date": item.isoformat(), "activeUsers": int(active_map.get(item.isoformat(), 0))} for item in days]
        return success(result)


@api.post("/statistics/content-review")
@admin_required
def statistics_content_review():
    days = recent_days(7)
    with engine.connect() as conn:
        rows = query_all(
            """
            SELECT DATE(create_time) AS day,
                   COUNT(1) AS new_content,
                   SUM(CASE WHEN publish_status IN ('draft', 'pending') THEN 1 ELSE 0 END) AS pending_count,
                   SUM(CASE WHEN publish_status = 'published' THEN 1 ELSE 0 END) AS approved_count,
                   SUM(CASE WHEN publish_status = 'rejected' THEN 1 ELSE 0 END) AS rejected_count
            FROM recommendation_content
            WHERE is_delete = 0
              AND DATE(create_time) >= :start_day
              AND DATE(create_time) <= :end_day
            GROUP BY DATE(create_time)
            """,
            {"start_day": days[0], "end_day": days[-1]},
            conn,
        )
        data_map: Dict[str, Dict[str, int]] = {}
        for row in rows:
            key = row["day"].isoformat() if isinstance(row["day"], date) else str(row["day"])
            data_map[key] = {
                "newContent": int(row.get("new_content") or 0),
                "pending": int(row.get("pending_count") or 0),
                "approved": int(row.get("approved_count") or 0),
                "rejected": int(row.get("rejected_count") or 0),
            }
        result = []
        for item in days:
            key = item.isoformat()
            current = data_map.get(key, {"newContent": 0, "pending": 0, "approved": 0, "rejected": 0})
            result.append({"date": key, **current})
        return success(result)


@api.post("/statistics/user-stats")
@admin_required
def statistics_user_stats():
    days = recent_days(7)
    with engine.connect() as conn:
        created_rows = query_all(
            """
            SELECT DATE(create_time) AS day, COUNT(1) AS cnt
            FROM user
            WHERE is_delete = 0
              AND DATE(create_time) >= :start_day
              AND DATE(create_time) <= :end_day
            GROUP BY DATE(create_time)
            """,
            {"start_day": days[0], "end_day": days[-1]},
            conn,
        )
        new_user_map = {
            (row["day"].isoformat() if isinstance(row["day"], date) else str(row["day"])): int(row["cnt"])
            for row in created_rows
        }
        active_map = load_daily_active_user_counts(conn, days)
        total_users = int((query_one("SELECT COUNT(1) AS cnt FROM user WHERE is_delete = 0", conn=conn) or {}).get("cnt", 0))

        result = []
        for item in days:
            key = item.isoformat()
            active_users = int(active_map.get(key, 0))
            retention = f"{round((active_users / total_users) * 100, 2)}%" if total_users > 0 else "0%"
            result.append(
                {
                    "date": key,
                    "newUsers": int(new_user_map.get(key, 0)),
                    "activeUsers": active_users,
                    "retentionRate": retention,
                }
            )
        return success(result)


@api.post("/statistics/content-stats")
@admin_required
def statistics_content_stats():
    return statistics_content_review()


@api.post("/statistics/coach-stats")
@admin_required
def statistics_coach_stats():
    days = recent_days(7)
    with engine.connect() as conn:
        new_rows = query_all(
            """
            SELECT DATE(create_time) AS day, COUNT(1) AS cnt
            FROM coach_profile
            WHERE is_delete = 0
              AND DATE(create_time) >= :start_day
              AND DATE(create_time) <= :end_day
            GROUP BY DATE(create_time)
            """,
            {"start_day": days[0], "end_day": days[-1]},
            conn,
        )
        new_map = {(row["day"].isoformat() if isinstance(row["day"], date) else str(row["day"])): int(row["cnt"]) for row in new_rows}

        certified_rows = query_all(
            """
            SELECT DATE(passed_time) AS day, COUNT(1) AS cnt
            FROM coach_profile
            WHERE is_delete = 0
              AND status = 'approved'
              AND passed_time IS NOT NULL
              AND DATE(passed_time) >= :start_day
              AND DATE(passed_time) <= :end_day
            GROUP BY DATE(passed_time)
            """,
            {"start_day": days[0], "end_day": days[-1]},
            conn,
        )
        certified_map = {
            (row["day"].isoformat() if isinstance(row["day"], date) else str(row["day"])): int(row["cnt"])
            for row in certified_rows
        }

        pending_rows = query_all(
            """
            SELECT DATE(create_time) AS day, COUNT(1) AS cnt
            FROM coach_profile
            WHERE is_delete = 0
              AND status = 'pending'
              AND DATE(create_time) >= :start_day
              AND DATE(create_time) <= :end_day
            GROUP BY DATE(create_time)
            """,
            {"start_day": days[0], "end_day": days[-1]},
            conn,
        )
        pending_map = {(row["day"].isoformat() if isinstance(row["day"], date) else str(row["day"])): int(row["cnt"]) for row in pending_rows}

        result = []
        for item in days:
            key = item.isoformat()
            result.append(
                {
                    "date": key,
                    "newApplications": int(new_map.get(key, 0)),
                    "certified": int(certified_map.get(key, 0)),
                    "pending": int(pending_map.get(key, 0)),
                }
            )
        return success(result)
