# FitPal Docker 部署说明

## 端口映射
- 后端 API：`http://127.0.0.1:9030`
- 管理端前端：`http://127.0.0.1:9031`
- UniApp H5：`http://127.0.0.1:9032`

## 使用的公共基础设施
后端容器已改为直接连接宿主机公共组件：
- MySQL：`127.0.0.1:3307` → 容器内通过 `host.docker.internal:3307`
- Redis：`127.0.0.1:6379` → 容器内通过 `host.docker.internal:6379`
- RabbitMQ：`127.0.0.1:5672` → 容器内通过 `host.docker.internal:5672`
- MinIO：`http://127.0.0.1:9000` → 容器内通过 `http://host.docker.internal:9000`

## 启动前准备
1. 确保宿主机公共组件已启动：MySQL / Redis / RabbitMQ / MinIO。
2. 确保 MySQL 中已存在数据库：`fit`
3. 初始化数据库：
   ```bash
   mysql -h 127.0.0.1 -P 3307 -uroot -proot fit < sql/fit2.sql
   ```

## 启动命令
```bash
docker compose up -d --build
```

## 查看状态
```bash
docker compose ps
```

## 查看后端日志
```bash
docker compose logs -f fitpal-backend
```

## 停止服务
```bash
docker compose down
```

## 说明
- `docker-compose.yml` 不再依赖项目内 MySQL/MinIO 容器，也不再依赖 `shared-infra` 网络。
- 后端导出目录已挂载到本地：`./data/exports`
- 当前代码中未实际使用 Redis / RabbitMQ，但已预留环境变量，后续接入时可直接复用。
- 若 Docker Hub 拉取超时，项目 Dockerfile 已切换为 `docker.1ms.run/library/*` 镜像源。
