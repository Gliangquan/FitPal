#!/usr/bin/env python3
filepath = '/Users/liangquan/Desktop/server/githubagentwork/repos/ch-bak/FitPal/docs/paper2/4-4  系统详细设计.md'
with open(filepath, 'r', encoding='utf-8') as f:
    c = f.read()

# 替换残留
c = c.replace('积分兑换实体E-R图', '积分账户实体E-R图')
c = c.replace('积分兑换实体ER图', '积分账户实体ER图')
c = c.replace('用户问卷表', '健康问卷表')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(c)

# 验证
with open(filepath, 'r', encoding='utf-8') as f:
    c = f.read()
print('积分兑换实体:', c.count('积分兑换实体'))
print('用户问卷表:', c.count('用户问卷表'))
print('积分账户实体:', c.count('积分账户实体'))
print('健康问卷表:', c.count('健康问卷表'))
