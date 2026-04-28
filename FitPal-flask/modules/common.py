import hashlib
import io
import json
import logging
import math
import os
import random
import smtplib
import string
import time
import csv
from email.message import EmailMessage
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from functools import wraps
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import jwt
import requests
from flask import Blueprint, Flask, Response, g, jsonify, request, send_file
from flask_cors import CORS
from minio import Minio
from minio.error import S3Error
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.exc import IntegrityError


SALT = "jcenLeung"
DEFAULT_JWT_SECRET = "your-secret-key-must-be-at-least-256-bits-long-for-hs256-algorithm-jcenLeung"
DEFAULT_JWT_EXPIRATION_MS = 86400000

ERR_PARAMS = 40000
ERR_NOT_LOGIN = 40100
ERR_NO_AUTH = 40101
ERR_INVALID_PASSWORD = 40102
ERR_FORBIDDEN = 40300
ERR_OPERATION_NOT_ALLOWED = 40301
ERR_NOT_FOUND = 40400
ERR_OPERATION = 50001
ERR_SYSTEM = 50000
ERR_CONFIG = 50003


class BusinessException(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("fitpal-flask")


def build_database_url() -> str:
    if os.getenv("DATABASE_URL"):
        return os.getenv("DATABASE_URL")
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "liangquan0302")
    name = os.getenv("DB_NAME", "fit")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset=utf8mb4"


def make_engine() -> Engine:
    return create_engine(build_database_url(), future=True, pool_pre_ping=True)


engine = make_engine()
JWT_SECRET = os.getenv("JWT_SECRET", DEFAULT_JWT_SECRET)
JWT_EXPIRATION_MS = int(os.getenv("JWT_EXPIRATION_MS", str(DEFAULT_JWT_EXPIRATION_MS)))
EXPORT_ROOT = Path(os.getenv("EXPORT_PATH", "./exports")).resolve()
EXPORT_ROOT.mkdir(parents=True, exist_ok=True)

_MINIO_ENDPOINT_RAW = os.getenv("MINIO_ENDPOINT", "http://85.137.247.55:9000").strip()
_minio_url = urlparse(_MINIO_ENDPOINT_RAW) if "://" in _MINIO_ENDPOINT_RAW else None
if _minio_url:
    _minio_host = (_minio_url.netloc or "").strip()
    _minio_secure_default = _minio_url.scheme == "https"
else:
    _minio_host = _MINIO_ENDPOINT_RAW
    _minio_secure_default = False

MINIO_ENDPOINT = _minio_host
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin").strip()
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin").strip()
MINIO_SECURE = os.getenv("MINIO_SECURE", str(_minio_secure_default).lower()).strip().lower() in ("1", "true", "yes", "y")
MINIO_USER_AVATAR_BUCKET = os.getenv("MINIO_USER_AVATAR_BUCKET", "fitpal-user-avatar").strip()
MINIO_COMMUNITY_POST_BUCKET = os.getenv("MINIO_COMMUNITY_POST_BUCKET", "fitpal-community-post").strip()
MINIO_USER_AVATAR_PREFIX = os.getenv("MINIO_USER_AVATAR_PREFIX", "avatars").strip()
MINIO_COMMUNITY_POST_PREFIX = os.getenv("MINIO_COMMUNITY_POST_PREFIX", "posts").strip()

WECHAT_APP_ID = os.getenv("WECHAT_APP_ID", "your_wechat_appid").strip()
WECHAT_SECRET = os.getenv("WECHAT_SECRET", "your_wechat_secret").strip()
WECHAT_LOGIN_URL = os.getenv("WECHAT_LOGIN_URL", "https://api.weixin.qq.com/sns/jscode2session").strip()

MINIO_ENABLED = bool(MINIO_ENDPOINT and MINIO_ACCESS_KEY and MINIO_SECRET_KEY)
minio_client: Optional[Minio] = None
if MINIO_ENABLED:
    minio_client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_SECURE,
    )


DEFAULT_BASIC_SETTINGS = {
    "platformName": "FitPal",
    "platformDescription": "基于微信小程序的轻体云管家",
    "contactPhone": "400-123-4567",
    "contactEmail": "support@fitpal.com",
    "termsUrl": "https://fitpal.com/terms",
    "privacyUrl": "https://fitpal.com/privacy",
}
DEFAULT_FEATURE_SETTINGS = {
    "communityEnabled": True,
    "coachEnabled": True,
    "pointsEnabled": True,
    "solarTermEnabled": True,
    "analyticsEnabled": True,
    "registrationEnabled": True,
}
DEFAULT_REVIEW_SETTINGS = {
    "autoReviewSensitiveWords": True,
    "sensitiveWords": "违禁词1\n违禁词2\n违禁词3",
    "maxContentLength": 5000,
    "maxImageCount": 9,
    "autoApproveThreshold": 80,
}
DEFAULT_POINTS_SETTINGS = {
    "dailyCheckInPoints": 10,
    "postContentPoints": 50,
    "contentLikePoints": 5,
    "completeTaskPoints": 100,
    "inviteFriendPoints": 200,
    "pointsExpireDays": 365,
}
DEFAULT_EMAIL_SETTINGS = {
    "smtpServer": "smtp.gmail.com",
    "smtpPort": 587,
    "senderEmail": "noreply@fitpal.com",
    "senderPassword": "",
    "enabled": False,
}

TASK_POINT_RULE_NAMES: Dict[str, List[str]] = {
    "DAILY_CHECKIN": ["每日签到", "每日打卡", "每日健康打卡"],
    "WEEKLY_EXERCISE_3": ["每周3次运动记录"],
    "ASSESSMENT_COMPLETE": ["完成减脂评估"],
    "COMMUNITY_POST": ["发布社区内容", "发布社区帖子"],
    "POST_LIKED": ["内容被赞"],
    "COMMUNITY_LIKE": ["点赞内容", "社区点赞"],
    "COMMUNITY_COMMENT": ["社区评论", "评论互动"],
}

TASK_BADGE_RULES: Dict[str, Dict[str, str]] = {
    "DAILY_CHECKIN": {
        "badge_code": "BADGE_001",
        "badge_name": "自律打卡勋章",
        "badge_desc": "首次完成每日健康打卡，代表你正式开启轻体计划。",
        "icon_url": "/static/icon_fit/jiangbei.png",
        "task_name": "每日健康打卡",
        "task_desc": "首次完成健康打卡后自动获得任务勋章。",
    },
    "WEEKLY_EXERCISE_3": {
        "badge_code": "BADGE_002",
        "badge_name": "运动达标勋章",
        "badge_desc": "同一周累计完成3次有效运动记录，代表训练执行达标。",
        "icon_url": "/static/icon_fit/jiangbei.png",
        "task_name": "每周完成3次运动",
        "task_desc": "同一周累计完成3次有效运动记录后自动获得任务勋章。",
    },
    "ASSESSMENT_COMPLETE": {
        "badge_code": "BADGE_003",
        "badge_name": "评估启程勋章",
        "badge_desc": "首次完成减脂评估并生成方案，代表你已进入科学减脂阶段。",
        "icon_url": "/static/icon_fit/jiangbei.png",
        "task_name": "完成减脂评估",
        "task_desc": "首次提交减脂问卷并生成方案后自动获得任务勋章。",
    },
    "COMMUNITY_POST": {
        "badge_code": "BADGE_004",
        "badge_name": "社区分享勋章",
        "badge_desc": "首次发布减脂相关社区内容，代表你开始主动分享成长过程。",
        "icon_url": "/static/icon_fit/jiangbei.png",
        "task_name": "发布社区内容",
        "task_desc": "首次发布减脂相关社区内容后自动获得任务勋章。",
    },
}


def parse_keyword_tokens(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    text_value = str(raw).strip()
    if not text_value:
        return []
    candidates: List[str] = []
    if text_value.startswith("[") and text_value.endswith("]"):
        try:
            parsed = json.loads(text_value)
            if isinstance(parsed, list):
                candidates = [str(item) for item in parsed]
        except Exception:
            candidates = []
    if not candidates:
        for sep in [",", "，", ";", "；", "|", "/", "\n", "\t"]:
            text_value = text_value.replace(sep, " ")
        candidates = text_value.split(" ")
    tokens: List[str] = []
    for item in candidates:
        token = str(item).strip().lower()
        if token:
            tokens.append(token)
    return tokens


def safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except Exception:
        return None


def fit_linear_regression(points: List[Tuple[float, float]]) -> Optional[Dict[str, float]]:
    if len(points) < 2:
        return None
    x_sum = 0.0
    y_sum = 0.0
    xx_sum = 0.0
    xy_sum = 0.0
    for x, y in points:
        x_sum += x
        y_sum += y
        xx_sum += x * x
        xy_sum += x * y
    n = float(len(points))
    denominator = n * xx_sum - x_sum * x_sum
    if abs(denominator) < 1e-8:
        return None
    slope = (n * xy_sum - x_sum * y_sum) / denominator
    intercept = (y_sum - slope * x_sum) / n

    y_mean = y_sum / n
    ss_tot = 0.0
    ss_res = 0.0
    for x, y in points:
        pred = slope * x + intercept
        ss_tot += (y - y_mean) ** 2
        ss_res += (y - pred) ** 2
    r2 = 0.0 if ss_tot <= 1e-8 else max(0.0, min(1.0, 1.0 - ss_res / ss_tot))
    return {"slope": slope, "intercept": intercept, "r2": r2}


def build_weight_trend(rows: List[Dict[str, Any]], horizon_days: int = 7) -> Optional[Dict[str, Any]]:
    points: List[Tuple[float, float]] = []
    start_day: Optional[date] = None
    for row in rows:
        day_value = row.get("record_date")
        weight_value = safe_float(row.get("weight_kg"))
        if weight_value is None:
            continue
        if isinstance(day_value, datetime):
            day_value = day_value.date()
        if not isinstance(day_value, date):
            try:
                day_value = date.fromisoformat(str(day_value))
            except Exception:
                continue
        if start_day is None:
            start_day = day_value
        x = float((day_value - start_day).days)
        points.append((x, weight_value))

    model = fit_linear_regression(points)
    if not model or start_day is None:
        return None

    future: List[Dict[str, Any]] = []
    max_x = max((item[0] for item in points), default=0.0)
    for step in range(1, max(horizon_days, 1) + 1):
        future_x = max_x + step
        future_day = start_day + timedelta(days=int(future_x))
        predict_weight = model["slope"] * future_x + model["intercept"]
        future.append(
            {
                "date": future_day,
                "predictWeightKg": Decimal(str(predict_weight)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            }
        )

    slope = model["slope"]
    if slope <= -0.12:
        trend_text = "down_fast"
    elif slope <= -0.03:
        trend_text = "down"
    elif slope >= 0.03:
        trend_text = "up"
    else:
        trend_text = "stable"

    return {
        "model": "linear_regression",
        "sampleSize": len(points),
        "slopePerDayKg": Decimal(str(slope)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP),
        "confidence": Decimal(str(model["r2"])).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP),
        "trend": trend_text,
        "next7Days": future,
    }


def build_health_suggestions(rows: List[Dict[str, Any]], trend_data: Optional[Dict[str, Any]]) -> List[str]:
    suggestions: List[str] = []
    if trend_data:
        trend = trend_data.get("trend")
        if trend == "up":
            suggestions.append("近阶段体重呈上升趋势，建议适度降低每日热量摄入并增加有氧训练。")
        elif trend == "down_fast":
            suggestions.append("体重下降偏快，建议增加优质蛋白和睡眠时长，避免过度节食。")
        elif trend == "stable":
            suggestions.append("体重波动较小，可维持当前节奏并逐步提高力量训练占比。")
        else:
            suggestions.append("体重趋势良好，建议继续保持规律饮食与运动习惯。")

    intake_values = [int(item.get("calorie_intake")) for item in rows if item.get("calorie_intake") is not None]
    burn_values = [int(item.get("calorie_burn")) for item in rows if item.get("calorie_burn") is not None]
    sleep_values = [safe_float(item.get("sleep_hours")) for item in rows if safe_float(item.get("sleep_hours")) is not None]
    if intake_values and burn_values:
        avg_intake = sum(intake_values) / len(intake_values)
        avg_burn = sum(burn_values) / len(burn_values)
        if avg_intake - avg_burn > 450:
            suggestions.append("当前热量摄入明显高于消耗，建议优先减少精制碳水和含糖饮料。")
        elif avg_burn - avg_intake > 800:
            suggestions.append("热量赤字较大，建议提升恢复营养，降低训练过载风险。")
    if sleep_values:
        avg_sleep = sum(sleep_values) / len(sleep_values)
        if avg_sleep < 7:
            suggestions.append("平均睡眠不足 7 小时，建议优先稳定作息以提升减脂效率。")
    if not suggestions:
        suggestions.append("继续保持每周至少 4 次运动和稳定打卡，逐步优化体脂率。")
    return suggestions


def resolve_task_points(conn: Connection, task_code: str, default_point: int) -> int:
    candidates = TASK_POINT_RULE_NAMES.get(task_code) or []
    if not candidates:
        return default_point
    placeholders, params = build_in_clause(candidates, "rule_name")
    try:
        row = query_one(
            f"""
            SELECT points FROM points_rule
            WHERE is_delete = 0
              AND enabled = 1
              AND rule_name IN ({placeholders})
            ORDER BY id DESC
            LIMIT 1
            """,
            params,
            conn,
        )
    except Exception:
        return default_point
    if not row or row.get("points") is None:
        return default_point
    try:
        return int(row.get("points"))
    except Exception:
        return default_point


def exists_point_log(conn: Connection, user_id: int, task_code: str, biz_date_value: date) -> bool:
    row = query_one(
        """
        SELECT COUNT(1) AS cnt FROM user_point_log
        WHERE user_id = :uid AND task_code = :task_code AND biz_date = :biz_date
        """,
        {"uid": user_id, "task_code": task_code, "biz_date": biz_date_value},
        conn,
    )
    return int((row or {}).get("cnt", 0)) > 0


def award_task_badge(conn: Connection, user_id: int, task_code: str) -> Optional[Dict[str, Any]]:
    rule = TASK_BADGE_RULES.get(task_code)
    if not rule:
        return None
    badge_code = str(rule.get("badge_code") or "").strip()
    if not badge_code:
        return None
    badge = query_one(
        """
        SELECT * FROM point_badge
        WHERE badge_code = :badge_code AND is_delete = 0 AND status = 1
        LIMIT 1
        """,
        {"badge_code": badge_code},
        conn,
    )
    if not badge or badge.get("id") is None:
        return None
    exists = query_one(
        """
        SELECT id FROM user_badge
        WHERE user_id = :user_id AND badge_id = :badge_id AND is_delete = 0
        LIMIT 1
        """,
        {"user_id": user_id, "badge_id": int(badge.get("id"))},
        conn,
    )
    if exists:
        return None
    execute_sql(
        """
        INSERT INTO user_badge (user_id, badge_id, cost_point, source, obtain_time, is_delete)
        VALUES (:user_id, :badge_id, 0, 'task_reward', NOW(), 0)
        """,
        {"user_id": user_id, "badge_id": int(badge.get("id"))},
        conn,
    )
    return {
        "badgeId": int(badge.get("id")),
        "badgeCode": badge.get("badge_code"),
        "badgeName": rule.get("badge_name") or badge.get("badge_name"),
        "badgeDesc": rule.get("badge_desc") or badge.get("badge_desc"),
        "iconUrl": rule.get("icon_url") or badge.get("icon_url"),
        "taskName": rule.get("task_name"),
        "taskDesc": rule.get("task_desc"),
    }


def add_task_points(
    conn: Connection,
    user_id: int,
    task_code: str,
    task_name: str,
    default_point: int,
    biz_date_value: date,
    remark: str,
    unique_per_day: bool = False,
) -> Dict[str, Any]:
    if unique_per_day and exists_point_log(conn, user_id, task_code, biz_date_value):
        return {"granted": False, "point": 0, "badge": None}
    final_point = resolve_task_points(conn, task_code, default_point)
    if final_point <= 0:
        return {"granted": False, "point": 0, "badge": None}
    add_point(conn, user_id, task_code, task_name, final_point, biz_date_value, remark)
    badge = award_task_badge(conn, user_id, task_code)
    return {"granted": True, "point": final_point, "badge": badge}


def build_solar_term_recipe_text(item: Dict[str, Any]) -> str:
    rows: List[str] = []
    day1 = str(item.get("day1_recipe") or "").strip()
    day2 = str(item.get("day2_recipe") or "").strip()
    day3 = str(item.get("day3_recipe") or "").strip()
    if day1:
        rows.append(f"第1天：{day1}")
    if day2:
        rows.append(f"第2天：{day2}")
    if day3:
        rows.append(f"第3天：{day3}")
    if not rows:
        description = str(item.get("description") or "").strip()
        if description:
            rows.append(description)
    return "\n".join(rows)


def build_solar_term_routine_text(item: Dict[str, Any]) -> str:
    rows: List[str] = []
    lifestyle = str(item.get("lifestyle_advice") or "").strip()
    health = str(item.get("health_knowledge") or "").strip()
    if lifestyle:
        rows.append(lifestyle)
    if health:
        rows.append(health)
    return "\n".join(rows)


def normalize_solar_term_topic_row(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": item.get("id"),
        "term_name": item.get("term_name") or item.get("solar_term_name") or "节气专题",
        "title": item.get("title") or item.get("solar_term_name") or "节气减脂专题",
        "recipe_text": item.get("recipe_text") or build_solar_term_recipe_text(item),
        "sport_guide": item.get("sport_guide") or item.get("exercise_guide"),
        "routine_advice": item.get("routine_advice") or build_solar_term_routine_text(item),
        "start_date": item.get("start_date"),
        "end_date": item.get("end_date"),
        "status": item.get("status") or "published",
        "is_delete": item.get("is_delete") or 0,
        "create_time": item.get("create_time") or item.get("created_at"),
        "update_time": item.get("update_time") or item.get("updated_at"),
    }


def resolve_topic_dates(
    start_date_text: Optional[str],
    end_date_text: Optional[str],
    existing_row: Optional[Dict[str, Any]] = None,
) -> Tuple[date, date]:
    start_day = parse_date(start_date_text, "startDate")
    end_day = parse_date(end_date_text, "endDate")
    if start_day is None and existing_row is not None:
        raw = existing_row.get("start_date")
        if isinstance(raw, date):
            start_day = raw
    if end_day is None and existing_row is not None:
        raw = existing_row.get("end_date")
        if isinstance(raw, date):
            end_day = raw
    if start_day is None:
        start_day = date.today()
    if end_day is None:
        end_day = start_day + timedelta(days=14)
    if end_day < start_day:
        end_day = start_day + timedelta(days=14)
    return start_day, end_day


def sync_solar_term_topic(
    conn: Connection,
    solar_term_id: int,
    start_date_text: Optional[str] = None,
    end_date_text: Optional[str] = None,
    force_delete: bool = False,
) -> None:
    solar_term = query_one("SELECT * FROM solar_term WHERE id = :id LIMIT 1", {"id": solar_term_id}, conn)
    if not solar_term:
        return
    topic_id: Optional[int] = None
    topic_row: Optional[Dict[str, Any]] = None
    try:
        link = query_one(
            "SELECT topic_id FROM solar_term_topic_link WHERE solar_term_id = :solar_term_id LIMIT 1",
            {"solar_term_id": solar_term_id},
            conn,
        )
        topic_id = int(link["topic_id"]) if link and link.get("topic_id") is not None else None
        topic_row = query_one("SELECT * FROM solar_term_topic WHERE id = :id LIMIT 1", {"id": topic_id}, conn) if topic_id else None
    except Exception:
        topic_id = None
        topic_row = None
    if topic_row is None:
        topic_row = query_one(
            """
            SELECT * FROM solar_term_topic
            WHERE term_name = :term_name
              AND is_delete = 0
            ORDER BY id DESC
            LIMIT 1
            """,
            {"term_name": solar_term.get("solar_term_name")},
            conn,
        )
        if topic_row and topic_row.get("id") is not None:
            topic_id = int(topic_row.get("id"))

    if force_delete or int(solar_term.get("is_delete") or 0) == 1:
        if topic_id:
            execute_sql(
                """
                UPDATE solar_term_topic
                SET is_delete = 1, status = 'draft', update_time = NOW()
                WHERE id = :id
                """,
                {"id": topic_id},
                conn,
            )
        return

    status = str(solar_term.get("status") or "draft").strip().lower()
    if status != "published":
        if topic_id:
            execute_sql(
                """
                UPDATE solar_term_topic
                SET status = 'draft', is_delete = 0, update_time = NOW()
                WHERE id = :id
                """,
                {"id": topic_id},
                conn,
            )
        return

    start_day, end_day = resolve_topic_dates(start_date_text, end_date_text, topic_row)
    topic_data = normalize_solar_term_topic_row(solar_term)
    topic_data["start_date"] = start_day
    topic_data["end_date"] = end_day
    topic_data["status"] = "published"
    topic_data["is_delete"] = 0
    if topic_id and topic_row:
        execute_sql(
            """
            UPDATE solar_term_topic
            SET term_name = :term_name,
                title = :title,
                recipe_text = :recipe_text,
                sport_guide = :sport_guide,
                routine_advice = :routine_advice,
                start_date = :start_date,
                end_date = :end_date,
                status = :status,
                is_delete = :is_delete,
                update_time = NOW()
            WHERE id = :id
            """,
            {**topic_data, "id": topic_id},
            conn,
        )
        return

    result = execute_sql(
        """
        INSERT INTO solar_term_topic (
            term_name, title, recipe_text, sport_guide,
            routine_advice, start_date, end_date, status, is_delete
        ) VALUES (
            :term_name, :title, :recipe_text, :sport_guide,
            :routine_advice, :start_date, :end_date, :status, :is_delete
        )
        """,
        topic_data,
        conn,
    )
    new_topic_id = int(result.lastrowid)
    try:
        execute_sql(
            """
            INSERT INTO solar_term_topic_link (solar_term_id, topic_id)
            VALUES (:solar_term_id, :topic_id)
            ON DUPLICATE KEY UPDATE topic_id = VALUES(topic_id), update_time = NOW()
            """,
            {"solar_term_id": solar_term_id, "topic_id": new_topic_id},
            conn,
        )
    except Exception:
        pass


def find_current_or_recent_topic(conn: Connection) -> Optional[Dict[str, Any]]:
    today = date.today()
    current = query_one(
        """
        SELECT * FROM solar_term_topic
        WHERE status = 'published' AND is_delete = 0
          AND start_date <= :today AND end_date >= :today
        ORDER BY update_time DESC
        LIMIT 1
        """,
        {"today": today},
        conn,
    )
    if current:
        return current
    recent = query_one(
        """
        SELECT * FROM solar_term_topic
        WHERE status = 'published' AND is_delete = 0
        ORDER BY update_time DESC
        LIMIT 1
        """,
        conn=conn,
    )
    if recent:
        return recent
    fallback_term = query_one(
        """
        SELECT * FROM solar_term
        WHERE status = 'published' AND is_delete = 0
        ORDER BY updated_at DESC, id DESC
        LIMIT 1
        """,
        conn=conn,
    )
    return normalize_solar_term_topic_row(fallback_term) if fallback_term else None


def infer_stage_tags(
    questionnaire: Optional[Dict[str, Any]],
    recent_records: List[Dict[str, Any]],
) -> List[str]:
    if questionnaire:
        current_weight = safe_float(questionnaire.get("current_weight_kg"))
        target_weight = safe_float(questionnaire.get("target_weight_kg"))
        if current_weight is not None and target_weight is not None:
            gap = current_weight - target_weight
            if gap >= 8:
                return ["beginner", "fat-loss", "starter"]
            if gap >= 3:
                return ["intermediate", "fat-loss"]
            return ["advanced", "maintenance"]
    if len(recent_records) < 7:
        return ["beginner"]
    return ["intermediate"]


def infer_body_tags(questionnaire: Optional[Dict[str, Any]], recent_records: List[Dict[str, Any]]) -> List[str]:
    height = safe_float(questionnaire.get("height_cm")) if questionnaire else None
    weight = safe_float(questionnaire.get("current_weight_kg")) if questionnaire else None
    if weight is None and recent_records:
        weight = safe_float(recent_records[-1].get("weight_kg"))
    if not height or not weight or height <= 0:
        return []
    bmi = weight / ((height / 100.0) ** 2)
    if bmi >= 28:
        return ["obese", "high-fat", "overweight"]
    if bmi >= 24:
        return ["overweight", "high-fat"]
    if bmi < 18.5:
        return ["lean", "underweight"]
    return ["normal"]


def collect_user_interest_tokens(
    user_row: Dict[str, Any],
    questionnaire: Optional[Dict[str, Any]],
    recent_posts: List[Dict[str, Any]],
) -> List[str]:
    tokens: List[str] = []
    for value in [user_row.get("user_profile"), user_row.get("user_name"), user_row.get("user_account")]:
        tokens.extend(parse_keyword_tokens(str(value) if value is not None else None))
    if questionnaire:
        for value in [
            questionnaire.get("diet_preference"),
            questionnaire.get("sport_preference"),
            questionnaire.get("intensity"),
            questionnaire.get("health_condition"),
        ]:
            tokens.extend(parse_keyword_tokens(str(value) if value is not None else None))
    for post in recent_posts:
        tokens.extend(parse_keyword_tokens(str(post.get("category") if post.get("category") is not None else "")))
    dedup: List[str] = []
    seen = set()
    for token in tokens:
        if token and token not in seen:
            seen.add(token)
            dedup.append(token)
    return dedup[:60]


def score_recommendation_content(
    item: Dict[str, Any],
    stage_filter: Optional[str],
    user_stage_tags: List[str],
    user_body_tags: List[str],
    interest_tokens: List[str],
) -> float:
    score = 0.0
    stage_tag = str(item.get("stage_tag") or "").strip().lower()
    body_tag = str(item.get("body_tag") or "").strip().lower()
    if stage_filter:
        if stage_tag == stage_filter:
            score += 80.0
        elif stage_tag in ("all", "general", "通用"):
            score += 10.0
    else:
        if stage_tag in user_stage_tags:
            score += 45.0
        elif stage_tag in ("all", "general", "通用"):
            score += 15.0
    if body_tag and body_tag in user_body_tags:
        score += 25.0

    item_tokens: List[str] = []
    item_tokens.extend(parse_keyword_tokens(str(item.get("tags") if item.get("tags") is not None else "")))
    item_tokens.extend(parse_keyword_tokens(str(item.get("title") if item.get("title") is not None else "")))
    item_tokens.extend(parse_keyword_tokens(str(item.get("summary") if item.get("summary") is not None else "")))
    item_tokens.extend(parse_keyword_tokens(str(item.get("content_type") if item.get("content_type") is not None else "")))
    overlap = len(set(item_tokens).intersection(set(interest_tokens)))
    score += min(30.0, overlap * 6.0)

    create_time = item.get("create_time")
    if isinstance(create_time, datetime):
        days = (datetime.now() - create_time).days
        score += max(0.0, 20.0 - min(float(days), 20.0))
    return score


def ensure_minio_ready() -> Minio:
    if not minio_client:
        raise BusinessException(ERR_CONFIG, "MinIO 未配置，请设置 MINIO_ENDPOINT/MINIO_ACCESS_KEY/MINIO_SECRET_KEY")
    for bucket_name in (MINIO_USER_AVATAR_BUCKET, MINIO_COMMUNITY_POST_BUCKET):
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
    return minio_client


def get_bucket_and_prefix_by_biz(biz: str) -> Tuple[str, str]:
    if biz == "user_avatar":
        return MINIO_USER_AVATAR_BUCKET, MINIO_USER_AVATAR_PREFIX
    if biz == "community_post":
        return MINIO_COMMUNITY_POST_BUCKET, MINIO_COMMUNITY_POST_PREFIX
    raise BusinessException(ERR_PARAMS, "业务类型错误")


def build_minio_object_name(biz: str, user_id: int, filename: str) -> str:
    _, prefix = get_bucket_and_prefix_by_biz(biz)
    normalized_prefix = prefix.strip("/") if prefix else ""
    if normalized_prefix:
        return f"{normalized_prefix}/{user_id}/{filename}"
    return f"{user_id}/{filename}"


def wechat_session_by_code(code: str) -> Tuple[str, Optional[str]]:
    if not WECHAT_APP_ID or not WECHAT_SECRET:
        raise BusinessException(ERR_CONFIG, "微信登录配置未完成，请设置 WECHAT_APP_ID 和 WECHAT_SECRET")
    try:
        resp = requests.get(
            WECHAT_LOGIN_URL,
            params={
                "appid": WECHAT_APP_ID,
                "secret": WECHAT_SECRET,
                "js_code": code,
                "grant_type": "authorization_code",
            },
            timeout=8,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as exc:
        raise BusinessException(ERR_SYSTEM, "微信登录服务不可用") from exc

    errcode = data.get("errcode")
    if errcode:
        errmsg = str(data.get("errmsg") or "微信登录失败")
        raise BusinessException(ERR_SYSTEM, f"微信登录失败: {errmsg}")
    openid = data.get("openid")
    unionid = data.get("unionid")
    if not openid:
        raise BusinessException(ERR_SYSTEM, "获取微信用户信息失败")
    return str(openid), str(unionid) if unionid else None


def init_runtime_tables() -> None:
    try:
        with engine.begin() as conn:
            execute_sql(
                """
                CREATE TABLE IF NOT EXISTS system_setting (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    setting_group VARCHAR(64) NOT NULL UNIQUE,
                    setting_json JSON NOT NULL,
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """,
                conn=conn,
            )
            execute_sql(
                """
                CREATE TABLE IF NOT EXISTS community_post_like (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    post_id BIGINT NOT NULL,
                    user_id BIGINT NOT NULL,
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE KEY uniq_post_user (post_id, user_id),
                    KEY idx_like_user_time (user_id, create_time)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """,
                conn=conn,
            )
            execute_sql(
                """
                CREATE TABLE IF NOT EXISTS solar_term_topic_link (
                    solar_term_id BIGINT NOT NULL PRIMARY KEY,
                    topic_id BIGINT NOT NULL,
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    KEY idx_topic_id (topic_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """,
                conn=conn,
            )
            execute_sql(
                """
                CREATE TABLE IF NOT EXISTS user_profile_ext (
                    user_id BIGINT NOT NULL PRIMARY KEY,
                    gender VARCHAR(16) NULL,
                    birth_date DATE NULL,
                    province VARCHAR(64) NULL,
                    city VARCHAR(64) NULL,
                    district VARCHAR(64) NULL,
                    address VARCHAR(255) NULL,
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """,
                conn=conn,
            )
            execute_sql(
                """
                CREATE TABLE IF NOT EXISTS user_membership (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    plan_code VARCHAR(32) NOT NULL,
                    plan_name VARCHAR(64) NOT NULL,
                    start_time DATETIME NOT NULL,
                    end_time DATETIME NOT NULL,
                    status VARCHAR(16) NOT NULL DEFAULT 'active',
                    source VARCHAR(32) NOT NULL DEFAULT 'demo',
                    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    KEY idx_membership_user (user_id),
                    KEY idx_membership_status_end (status, end_time)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """,
                conn=conn,
            )
    except Exception as exc:
        logger.warning("init runtime tables failed: %s", exc)


def snake_to_camel(key: str) -> str:
    if "_" not in key:
        return key
    parts = key.split("_")
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])


def to_jsonable(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {snake_to_camel(str(k)): to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_jsonable(v) for v in obj]
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        if obj == obj.to_integral_value():
            return int(obj)
        return float(obj)
    return obj


def success(data: Any) -> Response:
    return jsonify({"code": 0, "data": to_jsonable(data), "message": "ok"})


def error(code: int, message: str) -> Response:
    return jsonify({"code": code, "data": None, "message": message})


def md5_password(raw_password: str) -> str:
    return hashlib.md5((SALT + raw_password).encode("utf-8")).hexdigest()


def now() -> datetime:
    return datetime.now()


def parse_date(value: Optional[str], field_name: str = "date") -> Optional[date]:
    if value is None:
        return None
    text_value = str(value).strip()
    if not text_value:
        return None
    try:
        return date.fromisoformat(text_value)
    except Exception as exc:
        raise BusinessException(ERR_PARAMS, f"{field_name} 日期格式错误") from exc


def query_all(sql: str, params: Optional[Dict[str, Any]] = None, conn: Optional[Connection] = None) -> List[Dict[str, Any]]:
    params = params or {}
    if conn is not None:
        rows = conn.execute(text(sql), params).mappings().all()
        return [dict(row) for row in rows]
    with engine.connect() as local_conn:
        rows = local_conn.execute(text(sql), params).mappings().all()
        return [dict(row) for row in rows]


def query_one(sql: str, params: Optional[Dict[str, Any]] = None, conn: Optional[Connection] = None) -> Optional[Dict[str, Any]]:
    params = params or {}
    if conn is not None:
        row = conn.execute(text(sql), params).mappings().first()
        return dict(row) if row else None
    with engine.connect() as local_conn:
        row = local_conn.execute(text(sql), params).mappings().first()
        return dict(row) if row else None


def execute_sql(sql: str, params: Optional[Dict[str, Any]] = None, conn: Optional[Connection] = None):
    params = params or {}
    if conn is not None:
        return conn.execute(text(sql), params)
    with engine.begin() as local_conn:
        return local_conn.execute(text(sql), params)


def build_in_clause(values: List[Any], prefix: str) -> Tuple[str, Dict[str, Any]]:
    params: Dict[str, Any] = {}
    placeholders: List[str] = []
    for idx, value in enumerate(values):
        key = f"{prefix}{idx}"
        placeholders.append(f":{key}")
        params[key] = value
    return ", ".join(placeholders), params


def gen_page(records: List[Dict[str, Any]], total: int, current: int, size: int) -> Dict[str, Any]:
    pages = math.ceil(total / size) if size > 0 else 0
    return {
        "records": records,
        "total": total,
        "size": size,
        "current": current,
        "pages": pages,
    }


def create_token(user_id: int, user_account: str) -> str:
    issued_at = datetime.utcnow()
    expires_at = issued_at + timedelta(milliseconds=JWT_EXPIRATION_MS)
    payload = {
        "userId": user_id,
        "userAccount": user_account,
        "sub": str(user_id),
        "iat": issued_at,
        "exp": expires_at,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def extract_bearer_token() -> Optional[str]:
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:].strip()
    return None


def get_login_user(required: bool = True) -> Optional[Dict[str, Any]]:
    token = extract_bearer_token()
    if not token:
        if required:
            raise BusinessException(ERR_NOT_LOGIN, "未登录")
        return None
    try:
        claims = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except Exception:
        if required:
            raise BusinessException(ERR_NOT_LOGIN, "未登录")
        return None
    user_id = claims.get("userId")
    if not user_id:
        if required:
            raise BusinessException(ERR_NOT_LOGIN, "未登录")
        return None
    user = query_one(
        """
        SELECT * FROM user
        WHERE id = :id
        LIMIT 1
        """,
        {"id": int(user_id)},
    )
    if not user or (user.get("is_delete") == 1):
        if required:
            raise BusinessException(ERR_NOT_LOGIN, "未登录")
        return None
    return user


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        g.login_user = get_login_user(required=True)
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = get_login_user(required=True)
        if user.get("user_role") != "admin":
            raise BusinessException(ERR_NO_AUTH, "无权限")
        g.login_user = user
        return func(*args, **kwargs)

    return wrapper


def coach_or_admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = get_login_user(required=True)
        if user.get("user_role") not in ("coach", "admin"):
            raise BusinessException(ERR_NO_AUTH, "仅教练或管理员可操作")
        g.login_user = user
        return func(*args, **kwargs)

    return wrapper


def user_vo(user: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": user.get("id"),
        "userName": user.get("user_name"),
        "userAvatar": user.get("user_avatar"),
        "userProfile": user.get("user_profile"),
        "userRole": user.get("user_role"),
        "createTime": user.get("create_time"),
    }


def get_user_profile_ext(user_id: int, conn: Optional[Connection] = None) -> Dict[str, Any]:
    own_conn = conn is None
    local_conn = conn or engine.connect()
    try:
        row = query_one(
            "SELECT * FROM user_profile_ext WHERE user_id = :uid LIMIT 1",
            {"uid": int(user_id)},
            local_conn,
        )
        return row or {}
    finally:
        if own_conn:
            local_conn.close()


def get_active_membership(user_id: int, conn: Optional[Connection] = None) -> Dict[str, Any]:
    own_conn = conn is None
    local_conn = conn or engine.connect()
    try:
        row = query_one(
            """
            SELECT * FROM user_membership
            WHERE user_id = :uid AND status = 'active' AND end_time >= NOW()
            ORDER BY end_time DESC, id DESC
            LIMIT 1
            """,
            {"uid": int(user_id)},
            local_conn,
        )
        return row or {}
    finally:
        if own_conn:
            local_conn.close()


def login_user_vo(user: Dict[str, Any], token: Optional[str] = None, is_new_user: Optional[bool] = None) -> Dict[str, Any]:
    ext = get_user_profile_ext(int(user.get("id") or 0)) if user.get("id") else {}
    membership = get_active_membership(int(user.get("id") or 0)) if user.get("id") else {}
    result = {
        "id": user.get("id"),
        "userAccount": user.get("user_account"),
        "userName": user.get("user_name"),
        "userAvatar": user.get("user_avatar"),
        "userProfile": user.get("user_profile"),
        "userPhone": user.get("user_phone"),
        "userEmail": user.get("user_email"),
        "gender": ext.get("gender"),
        "birthDate": ext.get("birth_date"),
        "province": ext.get("province"),
        "city": ext.get("city"),
        "district": ext.get("district"),
        "address": ext.get("address"),
        "membershipActive": bool(membership),
        "membershipPlanCode": membership.get("plan_code"),
        "membershipPlanName": membership.get("plan_name"),
        "membershipEndTime": membership.get("end_time"),
        "userRole": user.get("user_role"),
        "createTime": user.get("create_time"),
        "updateTime": user.get("update_time"),
    }
    if token is not None:
        result["token"] = token
    if is_new_user is not None:
        result["isNewUser"] = is_new_user
    return result


def safe_user_name(user: Optional[Dict[str, Any]], user_id: Any) -> str:
    if not user:
        return f"用户#{user_id}"
    if user.get("user_name"):
        return user["user_name"]
    if user.get("user_account"):
        return user["user_account"]
    return f"用户#{user_id}"


def parse_image_urls(image_urls: Optional[str]) -> List[str]:
    if not image_urls:
        return []
    raw = image_urls.strip()
    if not raw:
        return []
    if raw.startswith("[") and raw.endswith("]"):
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                return [str(item) for item in data if str(item).strip()]
        except Exception:
            pass
    return [item.strip() for item in raw.split(",") if item.strip()]


def get_string(payload: Dict[str, Any], key: str) -> Optional[str]:
    if key not in payload or payload.get(key) is None:
        return None
    value = str(payload.get(key)).strip()
    return value if value else None


def get_required_string(payload: Dict[str, Any], key: str, message: str) -> str:
    value = get_string(payload, key)
    if not value:
        raise BusinessException(ERR_PARAMS, message)
    return value


def get_long(payload: Dict[str, Any], key: str) -> Optional[int]:
    if key not in payload or payload.get(key) is None:
        return None
    try:
        return int(str(payload.get(key)).strip())
    except Exception as exc:
        raise BusinessException(ERR_PARAMS, f"{key} 格式错误") from exc


def get_required_long(payload: Dict[str, Any], key: str, message: str) -> int:
    value = get_long(payload, key)
    if value is None or value <= 0:
        raise BusinessException(ERR_PARAMS, message)
    return value


def get_int(payload: Dict[str, Any], key: str) -> Optional[int]:
    if key not in payload or payload.get(key) is None:
        return None
    try:
        return int(str(payload.get(key)).strip())
    except Exception as exc:
        raise BusinessException(ERR_PARAMS, f"{key} 格式错误") from exc


def get_bool(payload: Dict[str, Any], key: str, default: Optional[bool] = None) -> Optional[bool]:
    if key not in payload or payload.get(key) is None:
        return default
    value = payload.get(key)
    if isinstance(value, bool):
        return value
    text_value = str(value).strip().lower()
    return text_value in ("1", "true", "yes", "y")


def ensure_point_account(user_id: int, conn: Connection) -> Dict[str, Any]:
    account = query_one("SELECT * FROM user_point_account WHERE user_id = :uid LIMIT 1", {"uid": user_id}, conn)
    if account:
        return account
    result = execute_sql(
        """
        INSERT INTO user_point_account (user_id, total_point, available_point, level_name)
        VALUES (:uid, 0, 0, '青铜')
        """,
        {"uid": user_id},
        conn,
    )
    account_id = result.lastrowid
    return query_one("SELECT * FROM user_point_account WHERE id = :id", {"id": account_id}, conn) or {}


def resolve_level(total_point: Optional[int]) -> str:
    value = total_point or 0
    if value < 100:
        return "青铜"
    if value < 300:
        return "白银"
    if value < 800:
        return "黄金"
    return "钻石"


def add_point(
    conn: Connection,
    user_id: int,
    task_code: str,
    task_name: str,
    point: int,
    biz_date: date,
    remark: str,
) -> None:
    account = ensure_point_account(user_id, conn)
    total_point = int(account.get("total_point") or 0) + point
    available_point = int(account.get("available_point") or 0) + point
    level_name = resolve_level(total_point)
    execute_sql(
        """
        UPDATE user_point_account
        SET total_point = :total_point,
            available_point = :available_point,
            level_name = :level_name,
            update_time = NOW()
        WHERE id = :id
        """,
        {
            "total_point": total_point,
            "available_point": available_point,
            "level_name": level_name,
            "id": account.get("id"),
        },
        conn,
    )
    execute_sql(
        """
        INSERT INTO user_point_log (user_id, task_code, task_name, point_change, biz_date, remark)
        VALUES (:user_id, :task_code, :task_name, :point_change, :biz_date, :remark)
        """,
        {
            "user_id": user_id,
            "task_code": task_code,
            "task_name": task_name,
            "point_change": point,
            "biz_date": biz_date,
            "remark": remark,
        },
        conn,
    )


def save_audit(conn: Connection, admin_user_id: int, biz_type: str, biz_id: int, action: str, remark: str) -> None:
    execute_sql(
        """
        INSERT INTO admin_audit_log (admin_user_id, biz_type, biz_id, action, remark)
        VALUES (:admin_user_id, :biz_type, :biz_id, :action, :remark)
        """,
        {
            "admin_user_id": admin_user_id,
            "biz_type": biz_type,
            "biz_id": biz_id,
            "action": action,
            "remark": remark,
        },
        conn,
    )


def to_community_post_view(conn: Connection, post: Dict[str, Any]) -> Dict[str, Any]:
    author = query_one("SELECT * FROM user WHERE id = :id LIMIT 1", {"id": post.get("user_id")}, conn)
    name = safe_user_name(author, post.get("user_id"))
    avatar = author.get("user_avatar") if author else None
    return {
        "id": post.get("id"),
        "userId": post.get("user_id"),
        "title": post.get("title"),
        "content": post.get("content"),
        "category": post.get("category"),
        "imageUrls": post.get("image_urls"),
        "imageList": parse_image_urls(post.get("image_urls")),
        "likeCount": post.get("like_count") or 0,
        "commentCount": post.get("comment_count") or 0,
        "viewCount": post.get("view_count") or 0,
        "status": post.get("status"),
        "createTime": post.get("create_time"),
        "updateTime": post.get("update_time"),
        "authorName": name,
        "authorAvatar": avatar,
        "userName": name,
        "userAvatar": avatar,
    }


def validate_upload_file(file_storage, biz: str) -> None:
    suffix = ""
    if file_storage.filename:
        if "." in file_storage.filename:
            suffix = file_storage.filename.rsplit(".", 1)[1].lower()
    file_storage.stream.seek(0, os.SEEK_END)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)
    one_mb = 1024 * 1024

    if biz == "user_avatar":
        if size > one_mb:
            raise BusinessException(ERR_PARAMS, "文件大小不能超过 1M")
        if suffix not in {"jpeg", "jpg", "svg", "png", "webp"}:
            raise BusinessException(ERR_PARAMS, "文件类型错误")
    elif biz == "community_post":
        if size > 5 * one_mb:
            raise BusinessException(ERR_PARAMS, "图片大小不能超过 5M")
        if suffix not in {"jpeg", "jpg", "png", "webp"}:
            raise BusinessException(ERR_PARAMS, "仅支持 jpg/png/webp")


def sanitize_filename(filename: str) -> str:
    safe_name = (filename or "unknown").strip()
    safe_name = safe_name.replace("..", "")
    safe_name = safe_name.replace("/", "_")
    safe_name = safe_name.replace("\\", "_")
    return safe_name or "unknown"


def normalize_role(value: Optional[str], default: str = "user") -> str:
    if not value:
        return default
    text_value = str(value).strip()
    return text_value if text_value else default


def get_system_setting(conn: Connection, setting_group: str, default_value: Dict[str, Any]) -> Dict[str, Any]:
    row = query_one(
        "SELECT * FROM system_setting WHERE setting_group = :setting_group LIMIT 1",
        {"setting_group": setting_group},
        conn,
    )
    if not row:
        execute_sql(
            """
            INSERT INTO system_setting (setting_group, setting_json)
            VALUES (:setting_group, :setting_json)
            """,
            {"setting_group": setting_group, "setting_json": json.dumps(default_value, ensure_ascii=False)},
            conn,
        )
        return dict(default_value)
    raw = row.get("setting_json")
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
    return dict(default_value)


def save_system_setting(conn: Connection, setting_group: str, setting_value: Dict[str, Any]) -> None:
    current = query_one(
        "SELECT id FROM system_setting WHERE setting_group = :setting_group LIMIT 1",
        {"setting_group": setting_group},
        conn,
    )
    payload = json.dumps(setting_value, ensure_ascii=False)
    if current:
        execute_sql(
            """
            UPDATE system_setting
            SET setting_json = :setting_json, update_time = NOW()
            WHERE setting_group = :setting_group
            """,
            {"setting_json": payload, "setting_group": setting_group},
            conn,
        )
    else:
        execute_sql(
            """
            INSERT INTO system_setting (setting_group, setting_json)
            VALUES (:setting_group, :setting_json)
            """,
            {"setting_group": setting_group, "setting_json": payload},
            conn,
        )


def recent_days(day_count: int = 7) -> List[date]:
    day_count = max(day_count, 1)
    today = date.today()
    start = today - timedelta(days=day_count - 1)
    return [start + timedelta(days=i) for i in range(day_count)]


def load_daily_active_user_counts(conn: Connection, days: List[date]) -> Dict[str, int]:
    if not days:
        return {}
    start_day = days[0]
    end_day = days[-1]
    rows = query_all(
        """
        SELECT activity_date, COUNT(DISTINCT user_id) AS active_users
        FROM (
            SELECT DATE(create_time) AS activity_date, id AS user_id
            FROM user
            WHERE is_delete = 0
            UNION ALL
            SELECT record_date AS activity_date, user_id
            FROM health_record
            WHERE is_delete = 0
            UNION ALL
            SELECT DATE(create_time) AS activity_date, user_id
            FROM community_post
            WHERE is_delete = 0
            UNION ALL
            SELECT DATE(create_time) AS activity_date, user_id
            FROM community_comment
            WHERE is_delete = 0
            UNION ALL
            SELECT DATE(create_time) AS activity_date, user_id
            FROM coach_consultation
            WHERE is_delete = 0
            UNION ALL
            SELECT biz_date AS activity_date, user_id
            FROM user_point_log
            WHERE biz_date IS NOT NULL
        ) t
        WHERE activity_date >= :start_day
          AND activity_date <= :end_day
        GROUP BY activity_date
        """,
        {"start_day": start_day, "end_day": end_day},
        conn,
    )
    result: Dict[str, int] = {}
    for row in rows:
        activity_day = row.get("activity_date")
        day_text = activity_day.isoformat() if isinstance(activity_day, date) else str(activity_day)
        result[day_text] = int(row.get("active_users") or 0)
    return result


def get_user_statistics_data(conn: Optional[Connection] = None) -> Dict[str, Any]:
    if conn is not None:
        active_rows = load_daily_active_user_counts(conn, recent_days(7))
        total_users = int((query_one("SELECT COUNT(1) AS cnt FROM user", conn=conn) or {}).get("cnt", 0))
        admin_count = int((query_one("SELECT COUNT(1) AS cnt FROM user WHERE user_role = 'admin'", conn=conn) or {}).get("cnt", 0))
        user_count = int((query_one("SELECT COUNT(1) AS cnt FROM user WHERE user_role = 'user'", conn=conn) or {}).get("cnt", 0))
        ban_count = int((query_one("SELECT COUNT(1) AS cnt FROM user WHERE user_role = 'ban'", conn=conn) or {}).get("cnt", 0))
        enabled_count = int((query_one("SELECT COUNT(1) AS cnt FROM user WHERE status = 1", conn=conn) or {}).get("cnt", 0))
        disabled_count = int((query_one("SELECT COUNT(1) AS cnt FROM user WHERE status = 0", conn=conn) or {}).get("cnt", 0))
        new_users = int(
            (
                query_one(
                    """
                    SELECT COUNT(1) AS cnt FROM user
                    WHERE create_time >= :seven_days_ago
                    """,
                    {"seven_days_ago": datetime.now() - timedelta(days=7)},
                    conn,
                )
                or {}
            ).get("cnt", 0)
        )
        active_users = sum(active_rows.values())
        return {
            "totalUsers": total_users,
            "activeUsers": active_users,
            "newUsers": new_users,
            "adminCount": admin_count,
            "userCount": user_count,
            "banCount": ban_count,
            "enabledCount": enabled_count,
            "disabledCount": disabled_count,
            "todayLoginCount": active_rows.get(date.today().isoformat(), 0),
            "weekLoginCount": active_users,
            "monthLoginCount": sum(load_daily_active_user_counts(conn, recent_days(30)).values()),
        }

    with engine.connect() as local_conn:
        return get_user_statistics_data(local_conn)


init_runtime_tables()
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
api = Blueprint("api", __name__, url_prefix="/api")
