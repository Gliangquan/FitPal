from ..common import *

@api.post("/user/register")
def user_register():
    payload = request.get_json(silent=True) or {}
    user_account = get_string(payload, "userAccount")
    user_password = get_string(payload, "userPassword")
    check_password = get_string(payload, "checkPassword")
    user_phone = get_string(payload, "userPhone")
    if not user_account or not user_password or not check_password or not user_phone:
        raise BusinessException(ERR_PARAMS, "请求参数错误")
    if len(user_account) < 4:
        raise BusinessException(ERR_PARAMS, "用户账号过短")
    if len(user_password) < 6 or len(check_password) < 6:
        raise BusinessException(ERR_PARAMS, "用户密码过短")
    if len(user_phone) != 11:
        raise BusinessException(ERR_PARAMS, "手机号格式错误")
    if user_password != check_password:
        raise BusinessException(ERR_PARAMS, "两次输入的密码不一致")

    with engine.begin() as conn:
        exists = query_one("SELECT COUNT(1) AS cnt FROM user WHERE user_account = :ua", {"ua": user_account}, conn)
        if (exists or {}).get("cnt", 0) > 0:
            raise BusinessException(ERR_PARAMS, "账号重复")
        phone_exists = query_one("SELECT COUNT(1) AS cnt FROM user WHERE user_phone = :up", {"up": user_phone}, conn)
        if (phone_exists or {}).get("cnt", 0) > 0:
            raise BusinessException(ERR_PARAMS, "手机号已被注册")
        result = execute_sql(
            """
            INSERT INTO user (user_account, user_password, user_phone, user_role, status, is_delete)
            VALUES (:user_account, :user_password, :user_phone, 'user', 1, 0)
            """,
            {
                "user_account": user_account,
                "user_password": md5_password(user_password),
                "user_phone": user_phone,
            },
            conn,
        )
        return success(result.lastrowid)


@api.post("/user/login")
def user_login():
    payload = request.get_json(silent=True) or {}
    login_type = get_string(payload, "loginType")
    user_password = get_string(payload, "userPassword")
    if not login_type or not user_password:
        raise BusinessException(ERR_PARAMS, "登录类型和密码不能为空")

    encrypted_password = md5_password(user_password)
    if login_type == "phone":
        user_phone = get_string(payload, "userPhone")
        if not user_phone:
            raise BusinessException(ERR_PARAMS, "手机号不能为空")
        user = query_one(
            """
            SELECT * FROM user
            WHERE user_phone = :user_phone AND user_password = :user_password
            LIMIT 1
            """,
            {"user_phone": user_phone, "user_password": encrypted_password},
        )
        if not user:
            raise BusinessException(ERR_PARAMS, "手机号或密码错误")
    elif login_type == "account":
        user_account = get_string(payload, "userAccount")
        if not user_account:
            raise BusinessException(ERR_PARAMS, "账号不能为空")
        user = query_one(
            """
            SELECT * FROM user
            WHERE user_account = :user_account AND user_password = :user_password
            LIMIT 1
            """,
            {"user_account": user_account, "user_password": encrypted_password},
        )
        if not user:
            raise BusinessException(ERR_PARAMS, "账号或密码错误")
    else:
        raise BusinessException(ERR_PARAMS, "登录类型不支持")

    token = create_token(int(user["id"]), str(user.get("user_account") or ""))
    return success(login_user_vo(user, token=token))


@api.post("/user/logout")
def user_logout():
    user = get_login_user(required=False)
    if not user:
        raise BusinessException(ERR_OPERATION, "未登录")
    return success(True)


@api.post("/user/login/wechat")
def user_login_wechat():
    payload = request.get_json(silent=True) or {}
    code = get_string(payload, "code")
    nick_name = get_string(payload, "nickName")
    avatar_url = get_string(payload, "avatarUrl")
    if not code:
        raise BusinessException(ERR_PARAMS, "微信登录凭证不能为空")
    openid, unionid = wechat_session_by_code(code)

    with engine.begin() as conn:
        user = query_one("SELECT * FROM user WHERE mp_open_id = :openid LIMIT 1", {"openid": openid}, conn)
        is_new_user = False
        if not user:
            account = "wechat_" + openid[:8]
            result = execute_sql(
                """
                INSERT INTO user (
                    user_account, user_password, user_name, user_avatar,
                    user_role, status, union_id, mp_open_id, is_delete
                )
                VALUES (
                    :user_account, :user_password, :user_name, :user_avatar,
                    'user', 1, :union_id, :mp_open_id, 0
                )
                """,
                {
                    "user_account": account,
                    "user_password": md5_password(openid),
                    "user_name": nick_name or "微信用户",
                    "user_avatar": avatar_url,
                    "union_id": unionid,
                    "mp_open_id": openid,
                },
                conn,
            )
            user = query_one("SELECT * FROM user WHERE id = :id", {"id": result.lastrowid}, conn)
            is_new_user = True
        else:
            updates = {}
            if nick_name and not user.get("user_name"):
                updates["user_name"] = nick_name
            if avatar_url and not user.get("user_avatar"):
                updates["user_avatar"] = avatar_url
            if not user.get("user_name") and not updates.get("user_name"):
                updates["user_name"] = "微信用户"
            if updates:
                set_clause = ", ".join([f"{k} = :{k}" for k in updates.keys()])
                params = {**updates, "id": user["id"]}
                execute_sql(f"UPDATE user SET {set_clause}, update_time = NOW() WHERE id = :id", params, conn)
                user = query_one("SELECT * FROM user WHERE id = :id", {"id": user["id"]}, conn)

        token = create_token(int(user["id"]), str(user.get("user_account") or ""))
        return success(login_user_vo(user, token=token, is_new_user=is_new_user))


@api.get("/user/get/login")
@login_required
def get_login_user_api():
    return success(login_user_vo(g.login_user))


@api.post("/user/add")
@admin_required
def add_user():
    payload = request.get_json(silent=True) or {}
    user_account = get_string(payload, "userAccount")
    if not user_account:
        raise BusinessException(ERR_PARAMS, "请求参数错误")

    with engine.begin() as conn:
        result = execute_sql(
            """
            INSERT INTO user (user_name, user_account, user_avatar, user_role, user_password, status, is_delete)
            VALUES (:user_name, :user_account, :user_avatar, :user_role, :user_password, 1, 0)
            """,
            {
                "user_name": get_string(payload, "userName"),
                "user_account": user_account,
                "user_avatar": get_string(payload, "userAvatar"),
                "user_role": normalize_role(get_string(payload, "userRole"), "user"),
                "user_password": md5_password("12345678"),
            },
            conn,
        )
        return success(result.lastrowid)


@api.post("/user/delete")
@admin_required
def delete_user():
    payload = request.get_json(silent=True) or {}
    user_id = get_required_long(payload, "id", "请求参数错误")
    with engine.begin() as conn:
        result = execute_sql("DELETE FROM user WHERE id = :id", {"id": user_id}, conn)
        return success(result.rowcount > 0)


@api.post("/user/update")
@admin_required
def update_user():
    payload = request.get_json(silent=True) or {}
    user_id = get_required_long(payload, "id", "请求参数错误")

    fields = {
        "user_name": get_string(payload, "userName"),
        "user_avatar": get_string(payload, "userAvatar"),
        "user_profile": get_string(payload, "userProfile"),
        "user_role": get_string(payload, "userRole"),
    }
    update_fields = {k: v for k, v in fields.items() if v is not None}
    if not update_fields:
        return success(True)

    set_clause = ", ".join([f"{k} = :{k}" for k in update_fields.keys()])
    params = {**update_fields, "id": user_id}
    with engine.begin() as conn:
        result = execute_sql(f"UPDATE user SET {set_clause}, update_time = NOW() WHERE id = :id", params, conn)
        if result.rowcount <= 0:
            raise BusinessException(ERR_OPERATION, "操作失败")
        return success(True)


@api.get("/user/get")
@admin_required
def get_user_by_id():
    user_id = request.args.get("id", type=int)
    if not user_id or user_id <= 0:
        raise BusinessException(ERR_PARAMS, "请求参数错误")
    user = query_one("SELECT * FROM user WHERE id = :id LIMIT 1", {"id": user_id})
    if not user:
        raise BusinessException(ERR_NOT_FOUND, "请求数据不存在")
    return success(user)


@api.get("/user/get/vo")
@admin_required
def get_user_vo_by_id():
    user_id = request.args.get("id", type=int)
    if not user_id or user_id <= 0:
        raise BusinessException(ERR_PARAMS, "请求参数错误")
    user = query_one("SELECT * FROM user WHERE id = :id LIMIT 1", {"id": user_id})
    if not user:
        raise BusinessException(ERR_NOT_FOUND, "请求数据不存在")
    return success(user_vo(user))


def list_users_with_filters(payload: Dict[str, Any], limit_size: Optional[int] = None) -> Tuple[List[Dict[str, Any]], int, int, int]:
    current = int(payload.get("current", 1) or 1)
    size = int(payload.get("pageSize", 10) or 10)
    if size <= 0:
        size = 10
    if current <= 0:
        current = 1
    if limit_size and size > limit_size:
        raise BusinessException(ERR_PARAMS, "请求参数错误")

    conditions = ["1=1"]
    params: Dict[str, Any] = {}
    if get_long(payload, "id"):
        conditions.append("id = :id")
        params["id"] = int(payload["id"])
    if get_string(payload, "unionId"):
        conditions.append("union_id = :union_id")
        params["union_id"] = get_string(payload, "unionId")
    if get_string(payload, "mpOpenId"):
        conditions.append("mp_open_id = :mp_open_id")
        params["mp_open_id"] = get_string(payload, "mpOpenId")
    if get_string(payload, "userRole"):
        conditions.append("user_role = :user_role")
        params["user_role"] = get_string(payload, "userRole")
    if get_string(payload, "userProfile"):
        conditions.append("user_profile LIKE :user_profile")
        params["user_profile"] = f"%{get_string(payload, 'userProfile')}%"
    if get_string(payload, "userName"):
        conditions.append("user_name LIKE :user_name")
        params["user_name"] = f"%{get_string(payload, 'userName')}%"

    where_clause = " AND ".join(conditions)

    sort_field = get_string(payload, "sortField")
    sort_order = get_string(payload, "sortOrder") or "ascend"
    allowed_sort_fields = {
        "id",
        "user_account",
        "user_name",
        "user_profile",
        "user_role",
        "status",
        "create_time",
        "update_time",
    }
    order_clause = ""
    if sort_field and sort_field in allowed_sort_fields:
        direction = "ASC" if sort_order == "ascend" else "DESC"
        order_clause = f" ORDER BY {sort_field} {direction}"

    total_row = query_one(f"SELECT COUNT(1) AS cnt FROM user WHERE {where_clause}", params)
    total = int((total_row or {}).get("cnt", 0))
    offset = (current - 1) * size
    records = query_all(
        f"SELECT * FROM user WHERE {where_clause}{order_clause} LIMIT :limit OFFSET :offset",
        {**params, "limit": size, "offset": offset},
    )
    return records, total, current, size


@api.post("/user/list/page")
@admin_required
def list_user_page():
    payload = request.get_json(silent=True) or {}
    records, total, current, size = list_users_with_filters(payload)
    return success(gen_page(records, total, current, size))


@api.post("/user/list/page/vo")
def list_user_vo_page():
    payload = request.get_json(silent=True) or {}
    records, total, current, size = list_users_with_filters(payload, limit_size=20)
    vo_records = [user_vo(item) for item in records]
    return success(gen_page(vo_records, total, current, size))


@api.post("/user/update/my")
@login_required
def update_my_user():
    payload = request.get_json(silent=True) or {}
    update_fields = {
        "user_name": get_string(payload, "userName"),
        "user_avatar": get_string(payload, "userAvatar"),
        "user_profile": get_string(payload, "userProfile"),
    }
    update_fields = {k: v for k, v in update_fields.items() if v is not None}
    if not update_fields:
        return success(True)

    set_clause = ", ".join([f"{k} = :{k}" for k in update_fields.keys()])
    params = {**update_fields, "id": g.login_user["id"]}
    with engine.begin() as conn:
        result = execute_sql(f"UPDATE user SET {set_clause}, update_time = NOW() WHERE id = :id", params, conn)
        if result.rowcount <= 0:
            raise BusinessException(ERR_OPERATION, "操作失败")
        return success(True)


@api.post("/user/batch-delete")
@admin_required
def batch_delete_user():
    payload = request.get_json(silent=True) or {}
    ids = payload.get("ids") or []
    if not isinstance(ids, list) or not ids:
        raise BusinessException(ERR_PARAMS, "请求参数错误")
    ids = [int(item) for item in ids if int(item) > 0]
    if not ids:
        raise BusinessException(ERR_PARAMS, "请求参数错误")
    soft_delete = get_bool(payload, "softDelete", True)

    placeholders, in_params = build_in_clause(ids, "id")
    with engine.begin() as conn:
        if soft_delete:
            result = execute_sql(
                f"UPDATE user SET is_delete = 1, update_time = NOW() WHERE id IN ({placeholders})",
                in_params,
                conn,
            )
        else:
            result = execute_sql(f"DELETE FROM user WHERE id IN ({placeholders})", in_params, conn)
        return success(int(result.rowcount))


@api.post("/user/batch-update")
@admin_required
def batch_update_user():
    payload = request.get_json(silent=True) or {}
    ids = payload.get("ids") or []
    if not isinstance(ids, list) or not ids:
        raise BusinessException(ERR_PARAMS, "请求参数错误")
    ids = [int(item) for item in ids if int(item) > 0]
    if not ids:
        raise BusinessException(ERR_PARAMS, "请求参数错误")

    update_fields = {}
    if get_string(payload, "userName") is not None:
        update_fields["user_name"] = get_string(payload, "userName")
    if get_string(payload, "userRole") is not None:
        update_fields["user_role"] = get_string(payload, "userRole")
    if payload.get("status") is not None:
        update_fields["status"] = int(payload.get("status"))
    if get_string(payload, "userProfile") is not None:
        update_fields["user_profile"] = get_string(payload, "userProfile")

    if not update_fields:
        return success(0)

    set_clause = ", ".join([f"{k} = :{k}" for k in update_fields.keys()])
    placeholders, in_params = build_in_clause(ids, "id")
    params = {**update_fields, **in_params}
    with engine.begin() as conn:
        result = execute_sql(
            f"UPDATE user SET {set_clause}, update_time = NOW() WHERE id IN ({placeholders})",
            params,
            conn,
        )
        return success(int(result.rowcount))


@api.post("/user/export")
@admin_required
def export_user():
    payload = request.get_json(silent=True) or {}
    if not isinstance(payload, dict):
        raise BusinessException(ERR_PARAMS, "请求参数错误")
    export_payload = dict(payload)
    export_payload["current"] = 1
    export_payload["pageSize"] = min(max(int(payload.get("pageSize", 20000) or 20000), 1), 50000)
    records, _, _, _ = list_users_with_filters(export_payload, limit_size=50000)

    file_name = f"user_export_{int(time.time())}.csv"
    file_path = EXPORT_ROOT / file_name
    headers = [
        "id",
        "user_account",
        "user_name",
        "user_phone",
        "user_email",
        "user_role",
        "status",
        "create_time",
        "update_time",
    ]
    with file_path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=headers)
        writer.writeheader()
        for row in records:
            writer.writerow({key: row.get(key) for key in headers})
    return success(str(file_path))


@api.post("/user/import")
@admin_required
def import_user():
    payload = request.get_json(silent=True) or {}
    if not isinstance(payload, dict):
        raise BusinessException(ERR_PARAMS, "请求参数错误")

    rows = payload.get("users")
    if not isinstance(rows, list):
        rows = payload.get("records")
    if not isinstance(rows, list):
        rows = []
        file_path_text = get_string(payload, "filePath")
        if file_path_text:
            file_path = Path(file_path_text).expanduser().resolve()
            if not file_path.exists():
                raise BusinessException(ERR_NOT_FOUND, "导入文件不存在")
            if file_path.suffix.lower() != ".csv":
                raise BusinessException(ERR_PARAMS, "仅支持 CSV 导入")
            with file_path.open("r", encoding="utf-8") as fp:
                reader = csv.DictReader(fp)
                rows = list(reader)

    if not rows:
        raise BusinessException(ERR_PARAMS, "导入数据不能为空")

    imported = 0
    with engine.begin() as conn:
        for raw in rows:
            if not isinstance(raw, dict):
                continue
            user_account = str(raw.get("userAccount") or raw.get("user_account") or "").strip()
            if not user_account:
                continue
            user_phone = str(raw.get("userPhone") or raw.get("user_phone") or "").strip() or None
            user_email = str(raw.get("userEmail") or raw.get("user_email") or "").strip() or None
            user_name = str(raw.get("userName") or raw.get("user_name") or "").strip() or None
            user_avatar = str(raw.get("userAvatar") or raw.get("user_avatar") or "").strip() or None
            user_profile = str(raw.get("userProfile") or raw.get("user_profile") or "").strip() or None
            user_role = str(raw.get("userRole") or raw.get("user_role") or "user").strip() or "user"
            status_raw = raw.get("status")
            status: Optional[int] = None
            if status_raw is not None and str(status_raw).strip():
                try:
                    status = 1 if int(str(status_raw).strip()) != 0 else 0
                except Exception:
                    status = None
            password_raw = str(raw.get("userPassword") or raw.get("user_password") or "").strip()

            exists = query_one(
                "SELECT * FROM user WHERE user_account = :ua LIMIT 1",
                {"ua": user_account},
                conn,
            )
            if not exists and user_phone:
                exists = query_one("SELECT * FROM user WHERE user_phone = :up LIMIT 1", {"up": user_phone}, conn)

            if exists:
                update_fields: Dict[str, Any] = {
                    "user_name": user_name,
                    "user_avatar": user_avatar,
                    "user_profile": user_profile,
                    "user_role": user_role,
                }
                if status is not None:
                    update_fields["status"] = status
                if user_phone:
                    phone_owner = query_one(
                        "SELECT id FROM user WHERE user_phone = :up LIMIT 1",
                        {"up": user_phone},
                        conn,
                    )
                    if not phone_owner or int(phone_owner.get("id")) == int(exists.get("id")):
                        update_fields["user_phone"] = user_phone
                if user_email:
                    email_owner = query_one(
                        "SELECT id FROM user WHERE user_email = :ue LIMIT 1",
                        {"ue": user_email},
                        conn,
                    )
                    if not email_owner or int(email_owner.get("id")) == int(exists.get("id")):
                        update_fields["user_email"] = user_email
                if password_raw:
                    update_fields["user_password"] = md5_password(password_raw)

                update_fields = {k: v for k, v in update_fields.items() if v is not None}
                if update_fields:
                    set_clause = ", ".join([f"{key} = :{key}" for key in update_fields.keys()])
                    execute_sql(
                        f"UPDATE user SET {set_clause}, update_time = NOW() WHERE id = :id",
                        {**update_fields, "id": int(exists.get("id"))},
                        conn,
                    )
                    imported += 1
                continue

            execute_sql(
                """
                INSERT INTO user (
                    user_account, user_password, user_phone, user_email,
                    user_name, user_avatar, user_profile, user_role, status, is_delete
                ) VALUES (
                    :user_account, :user_password, :user_phone, :user_email,
                    :user_name, :user_avatar, :user_profile, :user_role, :status, 0
                )
                """,
                {
                    "user_account": user_account,
                    "user_password": md5_password(password_raw or "111111"),
                    "user_phone": user_phone,
                    "user_email": user_email,
                    "user_name": user_name,
                    "user_avatar": user_avatar,
                    "user_profile": user_profile,
                    "user_role": user_role,
                    "status": 1 if status is None else status,
                },
                conn,
            )
            imported += 1
    return success(imported)


@api.get("/user/statistics")
@admin_required
def user_statistics():
    return success(get_user_statistics_data())
