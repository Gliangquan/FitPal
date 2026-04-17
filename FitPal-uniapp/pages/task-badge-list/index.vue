<template>
  <view class="page-content badge-task-page">
    <view class="hero-section">
      <text class="text-lg font-bold text-primary">任务勋章说明</text>
      <text class="text-sm text-secondary" style="display:block;margin-top:6rpx;">
        完成指定任务后可直接获得勋章，不需要再兑换。
      </text>
    </view>

    <view class="card task-card">
      <view class="task-item" v-for="item in tasks" :key="item.badgeCode">
        <view class="task-main">
          <text class="task-title">{{ item.taskName }}</text>
          <text class="task-desc">{{ item.taskDesc }}</text>
          <text class="task-reward">奖励：{{ item.badgeName }}</text>
        </view>
        <view class="task-badge">自动获得</view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      tasks: [
        {
          badgeCode: 'BADGE_001',
          taskName: '每日健康打卡',
          taskDesc: '首次完成每日健康打卡后，自动发放任务勋章。',
          badgeName: '自律打卡勋章'
        },
        {
          badgeCode: 'BADGE_002',
          taskName: '每周完成3次运动',
          taskDesc: '一周内累计完成3次有效运动记录后，自动发放任务勋章。',
          badgeName: '运动达标勋章'
        },
        {
          badgeCode: 'BADGE_003',
          taskName: '完成减脂评估',
          taskDesc: '首次提交减脂问卷并生成方案后，自动发放任务勋章。',
          badgeName: '评估启程勋章'
        },
        {
          badgeCode: 'BADGE_004',
          taskName: '发布社区内容',
          taskDesc: '首次发布社区动态后，自动发放任务勋章。',
          badgeName: '社区分享勋章'
        }
      ]
    };
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.badge-task-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.task-card {
  margin-top: 16rpx;
}

.task-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16rpx;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #edf1f7;
}

.task-item:last-child {
  border-bottom: none;
}

.task-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}

.task-title {
  font-size: 27rpx;
  font-weight: 600;
  color: $text-primary;
}

.task-desc {
  font-size: 22rpx;
  line-height: 1.6;
  color: $text-secondary;
}

.task-reward {
  font-size: 22rpx;
  color: $primary-color;
}

.task-badge {
  flex-shrink: 0;
  padding: 10rpx 18rpx;
  border-radius: 999rpx;
  background: #edf3ff;
  color: $primary-color;
  font-size: 22rpx;
  font-weight: 600;
}
</style>
