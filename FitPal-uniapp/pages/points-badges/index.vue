<template>
  <view class="page-content badges-page">
    <view class="hero-section">
      <text class="text-lg font-bold text-primary">积分兑换</text>
      <text class="text-sm text-secondary" style="display:block;margin-top:6rpx;">
        当前可用积分：{{ availablePoint }}
      </text>
    </view>

    <view class="card section-card">
      <text class="section-title">任务奖励说明</text>
      <view class="task-guide-list">
        <view class="task-guide-item" v-for="item in taskGuides" :key="item.title">
          <view class="task-guide-main">
            <text class="task-guide-title">{{ item.title }}</text>
            <text class="task-guide-desc">{{ item.desc }}</text>
          </view>
          <text class="task-guide-point">+{{ item.point }}积分</text>
        </view>
      </view>
      <text class="task-guide-tip">先完成运动、打卡、问卷、社区互动积累积分，再到下方兑换勋章。</text>
    </view>

    <view class="card section-card">
      <text class="section-title">可兑换勋章</text>
      <view v-if="badges.length">
        <view class="badge-item" v-for="item in badges" :key="item.id">
          <view class="badge-left">
            <image class="badge-icon" :src="resolveIcon(item.iconUrl)" mode="aspectFit" />
            <view class="badge-text">
              <text class="badge-name">{{ item.badgeName }}</text>
              <text class="badge-desc">{{ item.badgeDesc || '坚持打卡，兑换专属勋章' }}</text>
              <text class="badge-point">需要积分：{{ item.requiredPoint || 0 }}</text>
            </view>
          </view>
          <button
            class="btn-exchange"
            :disabled="item.owned || !item.canExchange"
            @tap="exchange(item)"
          >
            {{ item.owned ? '已拥有' : (item.canExchange ? '兑换' : '积分不足') }}
          </button>
        </view>
      </view>
      <text v-else class="text-sm text-muted">暂无可兑换勋章</text>
    </view>

    <view class="card section-card">
      <text class="section-title">任务完成后自动获得</text>
      <view v-if="taskBadges.length">
        <view class="my-badge-item" v-for="item in taskBadges" :key="`task-${item.id}`">
          <image class="my-badge-icon" :src="resolveIcon(item.iconUrl)" mode="aspectFit" />
          <view class="my-badge-text">
            <text class="my-badge-name">{{ item.badgeName }}</text>
            <text class="task-badge-desc">{{ item.taskName }} · {{ item.taskDesc }}</text>
            <text class="my-badge-time">{{ formatTime(item.obtainTime) }}</text>
          </view>
        </view>
      </view>
      <text v-else class="text-sm text-muted">暂未获得自动任务勋章，先去完成打卡、运动、问卷或社区任务吧</text>
    </view>

    <view class="card section-card">
      <text class="section-title">积分兑换勋章</text>
      <view v-if="myBadges.length">
        <view class="my-badge-item" v-for="item in myBadges" :key="item.id">
          <image class="my-badge-icon" :src="resolveIcon(item.iconUrl)" mode="aspectFit" />
          <view class="my-badge-text">
            <text class="my-badge-name">{{ item.badgeName }}</text>
            <text class="my-badge-time">{{ formatTime(item.obtainTime) }}</text>
          </view>
        </view>
      </view>
      <text v-else class="text-sm text-muted">还没有兑换勋章，先去积攒积分吧</text>
    </view>
  </view>
</template>

<script>
import { fitApi } from '@/utils/api.js';
import { resolveFileUrl } from '@/utils/request.js';

export default {
  data() {
    return {
      availablePoint: 0,
      badges: [],
      myBadges: [],
      taskBadges: [],
      taskGuides: [
        { title: '每日健康打卡', desc: '完成当天打卡可获得基础积分奖励', point: 10 },
        { title: '每周完成3次运动', desc: '记录运动消耗并达成周目标，可额外获得奖励', point: 50 },
        { title: '完成减脂评估', desc: '提交问卷后自动发放任务积分', point: 100 },
        { title: '发布社区内容', desc: '分享减脂心得、饮食或训练内容', point: 30 },
        { title: '社区互动', desc: '点赞、评论被系统记录后可累计积分', point: 1 }
      ]
    };
  },
  onShow() {
    this.loadData();
  },
  methods: {
    resolveIcon(url) {
      const value = String(url || '').trim();
      if (!value) return '/static/icon_fit/jiangbei.png';
      if (value.startsWith('/static/')) return value;
      return resolveFileUrl(value);
    },
    formatTime(value) {
      if (!value) return '';
      return String(value).replace('T', ' ').slice(0, 16);
    },
    async loadData() {
      try {
        const [pointInfo, badges, myBadges] = await Promise.all([
          fitApi.myPoints(),
          fitApi.listPointBadges(),
          fitApi.myPointBadges()
        ]);
        this.availablePoint = pointInfo?.account?.availablePoint || 0;
        this.badges = badges || [];
        this.myBadges = myBadges || [];
        this.taskBadges = pointInfo?.taskBadges || [];
      } catch (error) {
        uni.showToast({ title: error.message || '加载失败', icon: 'none' });
      }
    },
    async exchange(item) {
      if (!item || item.owned || !item.canExchange) return;
      try {
        await fitApi.exchangePointBadge(item.id);
        uni.showToast({ title: '兑换成功', icon: 'success' });
        this.loadData();
      } catch (error) {
        uni.showToast({ title: error.message || '兑换失败', icon: 'none' });
      }
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.badges-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.section-card {
  margin-top: 16rpx;
}

.task-guide-list {
  display: flex;
  flex-direction: column;
  gap: 14rpx;
}

.task-guide-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16rpx;
  padding: 18rpx 20rpx;
  border-radius: 18rpx;
  background: #f6f9ff;
}

.task-guide-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}

.task-guide-title {
  font-size: 26rpx;
  font-weight: 600;
  color: $text-primary;
}

.task-guide-desc {
  font-size: 22rpx;
  line-height: 1.5;
  color: $text-secondary;
}

.task-guide-point {
  flex-shrink: 0;
  font-size: 24rpx;
  font-weight: 700;
  color: #2f65f9;
}

.task-guide-tip {
  display: block;
  margin-top: 14rpx;
  font-size: 22rpx;
  line-height: 1.6;
  color: $text-muted;
}

.section-title {
  display: block;
  font-size: 30rpx;
  font-weight: 600;
  color: $text-primary;
  margin-bottom: 14rpx;
}

.badge-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16rpx;
  padding: 16rpx 0;
  border-bottom: 1rpx solid #edf1f7;
}

.badge-item:last-child {
  border-bottom: none;
}

.badge-left {
  display: flex;
  align-items: center;
  gap: 14rpx;
  min-width: 0;
  flex: 1;
}

.badge-icon {
  width: 74rpx;
  height: 74rpx;
  flex-shrink: 0;
}

.badge-text {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.badge-name {
  font-size: 27rpx;
  font-weight: 600;
  color: $text-primary;
}

.badge-desc {
  font-size: 22rpx;
  color: $text-secondary;
  line-height: 1.5;
}

.badge-point {
  font-size: 22rpx;
  color: #2f65f9;
}

.btn-exchange {
  min-width: 130rpx;
  height: 62rpx;
  line-height: 62rpx;
  border-radius: 999rpx;
  font-size: 24rpx;
  border: none;
  background: #2f65f9;
  color: #fff;
}

.btn-exchange[disabled] {
  opacity: 0.5;
}

.my-badge-item {
  display: flex;
  align-items: center;
  gap: 14rpx;
  padding: 14rpx 0;
  border-bottom: 1rpx solid #edf1f7;
}

.my-badge-item:last-child {
  border-bottom: none;
}

.my-badge-icon {
  width: 60rpx;
  height: 60rpx;
}

.my-badge-text {
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.my-badge-name {
  font-size: 26rpx;
  color: $text-primary;
  font-weight: 600;
}

.task-badge-desc {
  font-size: 22rpx;
  line-height: 1.5;
  color: $text-secondary;
}

.my-badge-time {
  font-size: 22rpx;
  color: $text-muted;
}
</style>
