#!/usr/bin/env python3
filepath = '/Users/liangquan/Desktop/server/githubagentwork/repos/ch-bak/FitPal/docs/paper2/4-4  系统详细设计.md'
with open(filepath, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. 修改描述文本
c = c.replace("主要包括用户、教练认证、健康记录、健康问卷、个性化方案、社区动态、积分账户、在线咨询和系统设置等。", "主要包括用户、教练、管理员、健康记录、健康问卷、个性化方案、社区动态、积分账户、在线咨询、教练认证、服务评价和会员订单等。")
c = c.replace("用户、教练、管理员、健康数据、减脂方案、积分、社区动态、评价反馈等实体", "用户、教练、管理员、健康记录、健康问卷、个性化方案、社区动态、积分账户、在线咨询、教练认证、服务评价、会员订单等十二个核心实体")

# 2. 补充4个实体ER图描述
er_add = "\n9. 教练：教练ID，关联用户ID，真实姓名，证书类型，证书编号，擅长领域，从业年限，审核状态，创建时间。教练实体ER图如图4-33所示：\n\n图4-33  教练实体E-R图\n\n10. 管理员：管理员ID，用户名，密码，真实姓名，手机号，状态，创建时间，更新时间。管理员实体ER图如图4-34所示：\n\n图4-34  管理员实体E-R图\n\n11. 服务评价：评价ID，用户ID，教练ID，咨询ID，评分，评价内容，是否匿名，创建时间。服务评价实体ER图如图4-35所示：\n\n图4-35  服务评价实体E-R图\n\n12. 会员订单：订单ID，用户ID，教练ID，订单编号，会员类型，金额，状态，起始日期，结束日期，创建时间。会员订单实体ER图如图4-36所示：\n\n图4-36  会员订单实体E-R图\n"
c = c.replace("图4-32  在线咨询实体E-R图", "图4-32  在线咨询实体E-R图" + er_add)

# 3. 补充4个数据表
tbl_add = '\n教练表用于存储教练的资质与专业信息，与用户表通过user_id关联，是教练服务模块的核心数据表。具体字段如表4.9所示：\n\n表4.9  教练表\n\n| 序号 | 字段名 | 类型 | 条件 | 说明 |\n|---|---|---|---|---|\n| 1 | id | bigint(20) | primary key not null | 教练ID |\n| 2 | user_id | bigint(20) | unique not null | 关联用户ID |\n| 3 | real_name | varchar(64) | not null | 真实姓名 |\n| 4 | cert_type | varchar(64) | not null | 证书类型 |\n| 5 | cert_no | varchar(128) | not null | 证书编号 |\n| 6 | expertise | varchar(256) | not null | 擅长领域 |\n| 7 | cert_image | varchar(512) |  | 证书照片 |\n| 8 | years_experience | int(11) |  | 从业年限 |\n| 9 | status | varchar(16) | not null | 审核状态 |\n| 10 | create_time | datetime | not null | 创建时间 |\n| 11 | update_time | datetime | not null | 更新时间 |\n\n管理员表用于存储后台管理员账号信息，是后台管理模块的身份认证基础。具体字段如表4.10所示：\n\n表4.10  管理员表\n\n| 序号 | 字段名 | 类型 | 条件 | 说明 |\n|---|---|---|---|---|\n| 1 | id | bigint(20) | primary key not null | 管理员ID |\n| 2 | username | varchar(64) | unique not null | 管理员账号 |\n| 3 | password | varchar(256) | not null | 登录密码 |\n| 4 | real_name | varchar(64) |  | 真实姓名 |\n| 5 | phone | varchar(32) |  | 手机号 |\n| 6 | status | tinyint(4) | not null | 启用状态 |\n| 7 | create_time | datetime | not null | 创建时间 |\n| 8 | update_time | datetime | not null | 更新时间 |\n\n服务评价表用于存储用户对教练服务的评分与反馈，是教练服务质量评估的重要依据。具体字段如表4.11所示：\n\n表4.11  服务评价表\n\n| 序号 | 字段名 | 类型 | 条件 | 说明 |\n|---|---|---|---|---|\n| 1 | id | bigint(20) | primary key not null | 评价ID |\n| 2 | user_id | bigint(20) | not null | 用户ID |\n| 3 | coach_id | bigint(20) | not null | 教练ID |\n| 4 | consult_id | bigint(20) |  | 咨询ID |\n| 5 | rating | tinyint(4) | not null | 评分(1-5) |\n| 6 | content | text |  | 评价内容 |\n| 7 | is_anonymous | tinyint(4) | not null | 是否匿名 |\n| 8 | create_time | datetime | not null | 创建时间 |\n\n会员订单表用于存储用户购买会员服务的订单信息，是会员服务模块的核心数据表。具体字段如表4.12所示：\n\n表4.12  会员订单表\n\n| 序号 | 字段名 | 类型 | 条件 | 说明 |\n|---|---|---|---|---|\n| 1 | id | bigint(20) | primary key not null | 订单ID |\n| 2 | user_id | bigint(20) | not null | 用户ID |\n| 3 | coach_id | bigint(20) |  | 教练ID |\n| 4 | order_no | varchar(64) | unique not null | 订单编号 |\n| 5 | vip_type | varchar(32) | not null | 会员类型 |\n| 6 | amount | decimal(10,2) | not null | 金额 |\n| 7 | status | varchar(16) | not null | 订单状态 |\n| 8 | start_date | date |  | 起始日期 |\n| 9 | end_date | date |  | 结束日期 |\n| 10 | create_time | datetime | not null | 创建时间 |\n'
c = c.replace("表4.8  在线咨询表", "表4.8  在线咨询表")
# 在表4.8最后一行后插入
lines = c.split('\n')
insert_idx = None
for i, line in enumerate(lines):
    if 'reply_time' in line and 'datetime' in line and '|' in line:
        insert_idx = i + 1
        break
if insert_idx:
    lines.insert(insert_idx, tbl_add)
c = '\n'.join(lines)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(c)
print('完成')
