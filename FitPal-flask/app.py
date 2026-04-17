import os

from sqlalchemy.exc import IntegrityError

from modules.common import (
    ERR_PARAMS,
    ERR_SYSTEM,
    BusinessException,
    api,
    app,
    error,
    logger,
)

# 按功能模块加载路由（仅用于触发装饰器注册）
from modules.routes import admin_ops_routes, fit_routes, settings_routes, statistics_routes, user_routes  # noqa: F401


@app.errorhandler(BusinessException)
def handle_business_error(exc: BusinessException):
    return error(exc.code, exc.message), 200


@app.errorhandler(IntegrityError)
def handle_integrity_error(exc: IntegrityError):
    logger.error("database integrity error: %s", exc)
    return error(ERR_PARAMS, "数据冲突"), 200


@app.errorhandler(Exception)
def handle_generic_error(exc: Exception):
    logger.exception("unhandled error: %s", exc)
    return error(ERR_SYSTEM, "系统内部异常"), 200


app.register_blueprint(api)


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "9903"))
    app.run(host=host, port=port, debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
