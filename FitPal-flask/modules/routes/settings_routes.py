from ..common import *

@api.get("/settings/basic")
@admin_required
def get_basic_settings():
    with engine.begin() as conn:
        settings = get_system_setting(conn, "basic", DEFAULT_BASIC_SETTINGS)
        return success(settings)


@api.post("/settings/basic/update")
@admin_required
def update_basic_settings():
    payload = request.get_json(silent=True) or {}
    with engine.begin() as conn:
        current = get_system_setting(conn, "basic", DEFAULT_BASIC_SETTINGS)
        merged = {**current, **payload}
        save_system_setting(conn, "basic", merged)
    return success(True)


@api.get("/settings/features")
@admin_required
def get_feature_settings():
    with engine.begin() as conn:
        settings = get_system_setting(conn, "features", DEFAULT_FEATURE_SETTINGS)
        return success(settings)


@api.post("/settings/features/update")
@admin_required
def update_feature_settings():
    payload = request.get_json(silent=True) or {}
    with engine.begin() as conn:
        current = get_system_setting(conn, "features", DEFAULT_FEATURE_SETTINGS)
        merged = {**current, **payload}
        save_system_setting(conn, "features", merged)
    return success(True)


@api.get("/settings/review")
@admin_required
def get_review_settings():
    with engine.begin() as conn:
        settings = get_system_setting(conn, "review", DEFAULT_REVIEW_SETTINGS)
        return success(settings)


@api.post("/settings/review/update")
@admin_required
def update_review_settings():
    payload = request.get_json(silent=True) or {}
    with engine.begin() as conn:
        current = get_system_setting(conn, "review", DEFAULT_REVIEW_SETTINGS)
        merged = {**current, **payload}
        save_system_setting(conn, "review", merged)
    return success(True)


@api.get("/settings/points")
@admin_required
def get_points_settings():
    with engine.begin() as conn:
        settings = get_system_setting(conn, "points", DEFAULT_POINTS_SETTINGS)
        return success(settings)


@api.post("/settings/points/update")
@admin_required
def update_points_settings():
    payload = request.get_json(silent=True) or {}
    with engine.begin() as conn:
        current = get_system_setting(conn, "points", DEFAULT_POINTS_SETTINGS)
        merged = {**current, **payload}
        save_system_setting(conn, "points", merged)
    return success(True)


@api.get("/settings/email")
@admin_required
def get_email_settings():
    with engine.begin() as conn:
        settings = get_system_setting(conn, "email", DEFAULT_EMAIL_SETTINGS)
        return success(settings)


@api.post("/settings/email/update")
@admin_required
def update_email_settings():
    payload = request.get_json(silent=True) or {}
    with engine.begin() as conn:
        current = get_system_setting(conn, "email", DEFAULT_EMAIL_SETTINGS)
        merged = {**current, **payload}
        save_system_setting(conn, "email", merged)
    return success(True)


@api.post("/settings/email/test")
@admin_required
def send_test_email():
    payload = request.get_json(silent=True) or {}
    target_email = get_string(payload, "email")
    if not target_email:
        raise BusinessException(ERR_PARAMS, "请求参数错误")

    with engine.begin() as conn:
        current_settings = get_system_setting(conn, "email", DEFAULT_EMAIL_SETTINGS)
    merged = dict(current_settings)
    for key in ("smtpServer", "smtpPort", "senderEmail", "senderPassword"):
        if key in payload and payload.get(key) is not None:
            merged[key] = payload.get(key)

    smtp_server = str(merged.get("smtpServer") or "").strip()
    sender_email = str(merged.get("senderEmail") or "").strip()
    sender_password = str(merged.get("senderPassword") or "").strip()
    try:
        smtp_port = int(str(merged.get("smtpPort") or "587").strip())
    except Exception as exc:
        raise BusinessException(ERR_PARAMS, "SMTP 端口格式错误") from exc
    if not smtp_server or not sender_email or not sender_password:
        raise BusinessException(ERR_CONFIG, "邮件配置不完整，请先配置 SMTP 服务与发件人账号")

    message = EmailMessage()
    message["Subject"] = get_string(payload, "subject") or "FitPal 邮件配置测试"
    message["From"] = sender_email
    message["To"] = target_email
    message.set_content(
        f"这是一封来自 FitPal 的测试邮件。\n发送时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )

    use_ssl = get_bool(payload, "ssl", smtp_port == 465)
    start_tls = get_bool(payload, "startTls", not bool(use_ssl) and smtp_port in (25, 587))
    try:
        if use_ssl:
            with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10) as smtp:
                smtp.login(sender_email, sender_password)
                smtp.send_message(message)
        else:
            with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as smtp:
                smtp.ehlo()
                if start_tls:
                    smtp.starttls()
                    smtp.ehlo()
                smtp.login(sender_email, sender_password)
                smtp.send_message(message)
    except Exception as exc:
        logger.error("send test email failed: %s", exc)
        raise BusinessException(ERR_SYSTEM, "测试邮件发送失败，请检查 SMTP 配置") from exc
    return success(True)


@api.post("/settings/logs")
@admin_required
def list_system_logs():
    payload = request.get_json(silent=True) or {}
    current = int(payload.get("current", 1) or 1)
    page_size = int(payload.get("pageSize", 20) or 20)
    current = max(current, 1)
    page_size = max(page_size, 1)
    offset = (current - 1) * page_size

    conditions = ["1=1"]
    params: Dict[str, Any] = {"limit": page_size, "offset": offset}
    biz_type = get_string(payload, "bizType")
    action = get_string(payload, "action")
    admin_user_id = get_long(payload, "adminUserId")
    if biz_type:
        conditions.append("biz_type = :biz_type")
        params["biz_type"] = biz_type
    if action:
        conditions.append("action = :action")
        params["action"] = action
    if admin_user_id:
        conditions.append("admin_user_id = :admin_user_id")
        params["admin_user_id"] = admin_user_id
    where_clause = " AND ".join(conditions)

    total = int((query_one(f"SELECT COUNT(1) AS cnt FROM admin_audit_log WHERE {where_clause}", params) or {}).get("cnt", 0))
    records = query_all(
        f"""
        SELECT * FROM admin_audit_log
        WHERE {where_clause}
        ORDER BY create_time DESC
        LIMIT :limit OFFSET :offset
        """,
        params,
    )
    return success({"records": records, "total": total})


@api.post("/settings/logs/export")
@admin_required
def export_system_logs():
    payload = request.get_json(silent=True) or {}
    conditions = ["1=1"]
    params: Dict[str, Any] = {}
    biz_type = get_string(payload, "bizType")
    action = get_string(payload, "action")
    admin_user_id = get_long(payload, "adminUserId")
    if biz_type:
        conditions.append("biz_type = :biz_type")
        params["biz_type"] = biz_type
    if action:
        conditions.append("action = :action")
        params["action"] = action
    if admin_user_id:
        conditions.append("admin_user_id = :admin_user_id")
        params["admin_user_id"] = admin_user_id
    where_clause = " AND ".join(conditions)

    rows = query_all(
        f"""
        SELECT * FROM admin_audit_log
        WHERE {where_clause}
        ORDER BY create_time DESC
        """,
        params,
    )
    filename = f"admin_audit_logs_{int(time.time())}.csv"
    filepath = EXPORT_ROOT / filename
    with filepath.open("w", encoding="utf-8", newline="") as fp:
        fp.write("id,admin_user_id,biz_type,biz_id,action,remark,create_time\n")
        for row in rows:
            remark = str(row.get("remark") or "").replace('"', '""')
            line = (
                f"{row.get('id')},{row.get('admin_user_id')},{row.get('biz_type')},"
                f"{row.get('biz_id')},{row.get('action')},\"{remark}\",{row.get('create_time')}\n"
            )
            fp.write(line)
    return success(str(filepath))


@api.post("/settings/logs/clear")
@admin_required
def clear_system_logs():
    with engine.begin() as conn:
        execute_sql("DELETE FROM admin_audit_log", conn=conn)
        return success(True)
