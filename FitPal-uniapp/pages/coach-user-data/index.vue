<template>
  <view class="page-content coach-user-page">
    <view class="hero-section">
      <text class="text-lg font-bold text-primary">查看用户数据</text>
      <text class="text-sm text-secondary" style="display:block;margin-top:8rpx;">仅展示与当前教练已建立咨询关系的用户数据</text>
    </view>

    <view class="card empty-card" v-if="!users.length && !loading">
      <text class="text-base font-semibold text-primary">暂无用户数据</text>
      <text class="text-sm text-muted" style="margin-top:8rpx;">用户发起在线咨询后，数据会出现在这里。</text>
    </view>

    <view v-else class="list-wrap">
      <view class="user-card" v-for="item in users" :key="item.userId">
        <view class="card-head">
          <text class="user-name">{{ item.userName || ('用户#' + item.userId) }}</text>
          <text class="user-id">用户ID：{{ item.userId }}</text>
        </view>
        <view class="metric-grid">
          <view class="metric-item">
            <text class="metric-label">健康记录</text>
            <text class="metric-value">{{ item.recordCount || 0 }}</text>
          </view>
          <view class="metric-item">
            <text class="metric-label">咨询次数</text>
            <text class="metric-value">{{ item.consultationCount || 0 }}</text>
          </view>
          <view class="metric-item">
            <text class="metric-label">最新体重</text>
            <text class="metric-value">{{ item.latestWeightKg ? (item.latestWeightKg + 'kg') : '-' }}</text>
          </view>
          <view class="metric-item">
            <text class="metric-label">方案热量</text>
            <text class="metric-value">{{ item.latestPlanCalories ? (item.latestPlanCalories + 'kcal') : '-' }}</text>
          </view>
        </view>
        <view class="detail-list">
          <text class="detail-item">最新记录日期：{{ item.latestRecordDate || '-' }}</text>
          <text class="detail-item">问卷当前体重：{{ item.currentWeightKg ? (item.currentWeightKg + 'kg') : '-' }}</text>
          <text class="detail-item">问卷目标体重：{{ item.targetWeightKg ? (item.targetWeightKg + 'kg') : '-' }}</text>
          <text class="detail-item">最新方案来源：{{ planSourceLabel(item.latestPlanSource) }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { fitApi } from '@/utils/api.js';
import { ensureRoleAccess } from '@/utils/permissions.js';

export default {
  data() {
    return {
      loading: false,
      users: []
    };
  },
  onShow() {
    if (!ensureRoleAccess(['coach', 'admin'])) return;
    this.loadData();
  },
  methods: {
    planSourceLabel(value) {
      if (value === 'coach-optimize') return '教练优化';
      if (value === 'admin-manual') return '管理员录入';
      if (value === 'mifflin-st-jeor+linear-regression') return '系统生成';
      if (value === 'mifflin-st-jeor') return '系统生成';
      return value || '-';
    },
    async loadData() {
      this.loading = true;
      try {
        this.users = await fitApi.getCoachUsersData();
      } catch (error) {
        this.users = [];
        uni.showToast({ title: error.message || '加载失败', icon: 'none' });
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.coach-user-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.list-wrap {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.user-card {
  background: #fff;
  border-radius: 18rpx;
  padding: 24rpx;
  box-shadow: 0 6rpx 20rpx rgba(0, 0, 0, 0.06);
}

.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12rpx;
}

.user-name {
  font-size: 30rpx;
  font-weight: 600;
  color: $text-primary;
}

.user-id {
  font-size: 22rpx;
  color: $text-muted;
}

.metric-grid {
  margin-top: 18rpx;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12rpx;
}

.metric-item {
  background: #f6f9ff;
  border-radius: 14rpx;
  padding: 16rpx;
}

.metric-label {
  display: block;
  font-size: 22rpx;
  color: $text-muted;
}

.metric-value {
  display: block;
  margin-top: 8rpx;
  font-size: 30rpx;
  font-weight: 700;
  color: $primary-color;
}

.detail-list {
  margin-top: 16rpx;
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.detail-item {
  font-size: 23rpx;
  line-height: 1.6;
  color: $text-secondary;
}

.empty-card {
  margin-top: 16rpx;
  text-align: center;
}
</style>
