# Tasks

- [x] 梳理 uniapp 与 PC 端现有角色/功能入口及命名差异
- [x] 实现统一功能权限定义并接入 uniapp 端展示/跳转控制
- [x] 实现 PC 管理端菜单/路由权限与功能命名收敛
- [x] 验证关键文件变更并总结影响范围

## Review
- 已新增 uniapp 统一权限定义 `FitPal-uniapp/utils/permissions.js`，并按用户/教练角色收敛首页与个人页能力入口。
- 已新增教练侧 `查看用户数据`、`查看服务评价`、`会员定制服务` 页面，并补齐后端接口 `/fit/coach/users-data`、`/fit/coach/reviews/received`。
- 已将 PC 管理端主导航命名收敛为“后台登录 / 审核教练资质 / 用户账号管理 / 社区内容审核 / 数据统计”。
- 已验证 `pages.json` JSON 结构、Flask 路由语法、Vue 管理端构建、uniapp 相关页面脚本语法。
