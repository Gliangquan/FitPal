<template>
  <view class="page-content coach-review-page">
    <view class="hero-section">
      <text class="text-lg font-bold text-primary">查看服务评价</text>
      <text class="text-sm text-secondary" style="display:block;margin-top:8rpx;">查看用户对当前教练服务的评分与评价内容</text>
    </view>

    <view class="card summary-card">
      <text class="summary-title">平均评分</text>
      <text class="summary-value">{{ avgRatingText }}</text>
    </view>

    <view class="card empty-card" v-if="!reviews.length && !loading">
      <text class="text-base font-semibold text-primary">暂无服务评价</text>
      <text class="text-sm text-muted" style="margin-top:8rpx;">用户提交教练服务评价后会展示在这里。</text>
    </view>

    <view v-else class="review-list">
      <view class="review-card" v-for="item in reviews" :key="item.id">
        <view class="review-head">
          <text class="user-name">{{ item.userName || ('用户#' + item.userId) }}</text>
          <text class="review-time">{{ item.createTime || '-' }}</text>
        </view>
        <uni-rate :value="item.rating || 0" size="16" readonly />
        <text class="review-content">{{ item.content || '暂无评价内容' }}</text>
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
      avgRating: 0,
      reviews: []
    };
  },
  computed: {
    avgRatingText() {
      return this.avgRating ? `${this.avgRating} 分` : '暂无评分';
    }
  },
  onShow() {
    if (!ensureRoleAccess(['coach', 'admin'])) return;
    this.loadData();
  },
  methods: {
    async loadData() {
      this.loading = true;
      try {
        const data = await fitApi.getCoachReceivedReviews();
        this.avgRating = Number(data?.avgRating || 0);
        this.reviews = Array.isArray(data?.records) ? data.records : [];
      } catch (error) {
        this.avgRating = 0;
        this.reviews = [];
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

.coach-review-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.summary-card {
  margin-top: 16rpx;
  text-align: center;
}

.summary-title {
  display: block;
  font-size: 24rpx;
  color: $text-muted;
}

.summary-value {
  display: block;
  margin-top: 10rpx;
  font-size: 42rpx;
  font-weight: 700;
  color: $primary-color;
}

.review-list {
  margin-top: 16rpx;
  display: flex;
  flex-direction: column;
  gap: 14rpx;
}

.review-card {
  background: #fff;
  border-radius: 18rpx;
  padding: 22rpx;
  box-shadow: 0 6rpx 20rpx rgba(0, 0, 0, 0.06);
}

.review-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12rpx;
}

.user-name {
  font-size: 28rpx;
  font-weight: 600;
  color: $text-primary;
}

.review-time {
  font-size: 22rpx;
  color: $text-muted;
}

.review-content {
  display: block;
  margin-top: 12rpx;
  font-size: 24rpx;
  line-height: 1.7;
  color: $text-secondary;
}

.empty-card {
  margin-top: 16rpx;
  text-align: center;
}
</style>
