<template>
  <view class="page-content coach-member-page">
    <view class="hero-section">
      <text class="text-lg font-bold text-primary">会员定制服务</text>
      <text class="text-sm text-secondary" style="display:block;margin-top:8rpx;">当前基于现有能力，为会员用户提供方案优化与咨询跟进入口</text>
    </view>

    <view class="card service-card">
      <view class="service-item">
        <text class="service-title">减脂方案优化</text>
        <text class="service-desc">针对用户已有个性化减脂方案进行二次优化与执行建议补充。</text>
        <button class="btn-primary-action" @tap="goPlanOptimize">进入减脂方案优化</button>
      </view>
      <view class="service-divider" />
      <view class="service-item">
        <text class="service-title">在线咨询回复</text>
        <text class="service-desc">集中处理会员咨询、补充训练建议和饮食反馈。</text>
        <button class="btn-secondary-action" @tap="goConsultReply">进入在线咨询回复</button>
      </view>
    </view>
  </view>
</template>

<script>
import { ensureRoleAccess } from '@/utils/permissions.js';

export default {
  onShow() {
    ensureRoleAccess(['coach', 'admin']);
  },
  methods: {
    goPlanOptimize() {
      uni.navigateTo({ url: '/pages/coach-plan-optimize/index' });
    },
    goConsultReply() {
      uni.navigateTo({ url: '/pages/coach-workbench/index' });
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.coach-member-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.service-card {
  margin-top: 16rpx;
}

.service-item {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.service-title {
  font-size: 30rpx;
  font-weight: 600;
  color: $text-primary;
}

.service-desc {
  font-size: 24rpx;
  line-height: 1.7;
  color: $text-secondary;
}

.service-divider {
  height: 1rpx;
  background: #edf1f7;
  margin: 24rpx 0;
}

.btn-primary-action,
.btn-secondary-action {
  width: 100%;
  height: 78rpx;
  line-height: 78rpx;
  border-radius: 999rpx;
  font-size: 28rpx;
  border: none;
}

.btn-primary-action {
  color: #fff;
  background: $primary-color;
}

.btn-secondary-action {
  color: #1e3a8a;
  background: #eef2ff;
}
</style>
