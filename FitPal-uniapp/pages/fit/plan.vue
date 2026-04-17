<template>
  <view class="page-content plan-page">
    <view class="hero-section" v-if="plan">
      <view class="plan-header">
        <text class="text-lg font-bold text-primary">个性化减脂方案</text>
        <button class="btn-regenerate" size="mini" @tap="generate">
          <uni-icons type="refresh" size="14" color="#2f65f9" />
          <text>重新生成</text>
        </button>
      </view>
      <view class="metric-row">
        <view class="metric-item">
          <text class="text-sm text-muted">基础代谢</text>
          <text class="metric-value">{{ plan.bmr || '-' }}</text>
          <text class="text-sm text-muted">kcal</text>
        </view>
        <view class="metric-item">
          <text class="text-sm text-muted">日目标热量</text>
          <text class="metric-value">{{ plan.dailyCalorieTarget || '-' }}</text>
          <text class="text-sm text-muted">kcal</text>
        </view>
      </view>
    </view>

    <view class="card empty-card" v-else>
      <uni-icons type="info-filled" size="44" color="#94a3b8" />
      <text class="empty-title">还没有生成方案</text>
      <text class="empty-desc">请先填写减脂问卷</text>
      <button class="btn-goto" @tap="goQuestionnaire">去填写问卷</button>
    </view>

    <view class="card section-card" v-if="plan">
      <view class="section-header">
        <uni-icons type="nutrition" size="18" color="#2f65f9" />
        <text class="section-title">饮食建议</text>
      </view>
      <text class="section-content">{{ plan.dietSuggestion || '暂无饮食建议' }}</text>
    </view>

    <view class="card section-card" v-if="plan">
      <view class="section-header">
        <uni-icons type="fire" size="18" color="#2f65f9" />
        <text class="section-title">运动建议</text>
      </view>
      <text class="section-content">{{ plan.workoutSuggestion || '暂无运动建议' }}</text>
    </view>

    <view class="card section-card" v-if="plan">
      <view class="section-header">
        <uni-icons type="calendar" size="18" color="#2f65f9" />
        <text class="section-title">节气提示</text>
      </view>
      <text class="section-content">{{ plan.seasonTips || '暂无节气提示' }}</text>
    </view>

    <view class="card section-card" v-if="topicTitle">
      <view class="section-header">
        <uni-icons type="star-filled" size="18" color="#2f65f9" />
        <text class="section-title">{{ topicTitle }}</text>
      </view>
      <text class="section-content">{{ topicGuide || '结合当前节气调整饮食和作息。' }}</text>
    </view>

    <view class="card section-card">
      <view class="section-header">
        <uni-icons type="paperplane" size="18" color="#2f65f9" />
        <text class="section-title">推荐内容</text>
      </view>
      <view v-if="recommendList.length" class="recommend-list">
        <view class="recommend-item" v-for="item in recommendList" :key="item.id">
          <text class="recommend-title">{{ item.title }}</text>
          <text class="recommend-summary">{{ item.summary || '暂无摘要' }}</text>
        </view>
      </view>
      <text v-else class="text-sm text-muted">暂无推荐内容</text>
    </view>
  </view>
</template>

<script>
import { fitApi } from '@/utils/api.js';

export default {
  data() {
    return {
      plan: null,
      topicTitle: '',
      topicGuide: '',
      recommendList: []
    };
  },
  onShow() {
    this.loadData();
  },
  methods: {
    async loadData() {
      try {
        this.plan = await fitApi.getLatestPlan();
      } catch (error) {
        this.plan = null;
      }
      try {
        const topic = await fitApi.getCurrentSeasonTopic();
        if (Array.isArray(topic)) {
          const first = topic[0] || {};
          this.topicTitle = first.title || '';
          this.topicGuide = first.routineAdvice || '';
        } else {
          this.topicTitle = topic?.title || '';
          this.topicGuide = topic?.routineAdvice || '';
        }
      } catch (error) {
        this.topicTitle = '';
        this.topicGuide = '';
      }
      try {
        this.recommendList = await fitApi.recommendContent('', 6);
      } catch (error) {
        this.recommendList = [];
      }
    },
    async generate() {
      try {
        await fitApi.generatePlan();
        uni.showToast({ title: '方案已更新', icon: 'success' });
        this.loadData();
      } catch (error) {
        uni.showToast({ title: error.message || '请先填问卷', icon: 'none' });
      }
    },
    goQuestionnaire() {
      uni.navigateTo({ url: '/pages/fit/questionnaire' });
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.plan-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.plan-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14rpx;
}

.btn-regenerate {
  display: flex;
  align-items: center;
  gap: 6rpx;
  background: #edf3ff;
  color: $primary-color;
  border-radius: 999rpx;
  border: 1rpx solid #dbe7ff;
  padding: 6rpx 18rpx;
  font-size: 22rpx;
}

.metric-row {
  display: flex;
  gap: 12rpx;
}

.metric-item {
  flex: 1;
  background: #f6f9ff;
  border-radius: 12rpx;
  padding: 14rpx;
}

.metric-value {
  display: block;
  margin: 6rpx 0;
  font-size: 36rpx;
  font-weight: 700;
  color: $primary-color;
}

.empty-card {
  text-align: center;
  padding: 64rpx 24rpx;
}

.empty-title {
  display: block;
  margin-top: 14rpx;
  font-size: 28rpx;
  font-weight: 600;
  color: $text-primary;
}

.empty-desc {
  display: block;
  margin-top: 8rpx;
  font-size: 24rpx;
  color: $text-muted;
}

.btn-goto {
  margin-top: 20rpx;
  background: $primary-color;
  color: #fff;
  border-radius: 999rpx;
  border: none;
  height: 72rpx;
  line-height: 72rpx;
  padding: 0 40rpx;
  font-size: 26rpx;
}

.section-card {
  margin-top: 14rpx;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 10rpx;
  margin-bottom: 10rpx;
}

.section-title {
  font-size: 28rpx;
  font-weight: 600;
  color: $text-primary;
}

.section-content {
  font-size: 25rpx;
  line-height: 1.65;
  color: $text-secondary;
}

.recommend-list {
  display: flex;
  flex-direction: column;
  gap: 10rpx;
}

.recommend-item {
  background: #f8fbff;
  border: 1rpx solid #eaf0fb;
  border-radius: 10rpx;
  padding: 12rpx;
}

.recommend-title {
  display: block;
  font-size: 26rpx;
  font-weight: 600;
  color: $text-primary;
}

.recommend-summary {
  display: block;
  margin-top: 6rpx;
  font-size: 22rpx;
  color: $text-muted;
}
</style>
