<template>
  <view class="page-content season-page">
    <view class="hero-section intro-card">
      <view>
        <text class="text-lg font-bold text-primary">节气专栏</text>
        <text class="text-sm text-secondary" style="display:block;margin-top:6rpx;">查看当前节气与近期专题内容</text>
      </view>
    </view>

    <view v-if="topicList.length" class="topic-list">
      <view class="card topic-item" v-for="item in topicList" :key="item.id || item.title">
        <view class="topic-head">
          <text class="topic-title">{{ item.title || item.name || '节气专题' }}</text>
          <text class="topic-date" v-if="item.startDate || item.endDate">{{ item.startDate || '' }} {{ item.endDate ? `- ${item.endDate}` : '' }}</text>
        </view>
        <text class="topic-content">{{ item.routineAdvice || item.recipeText || item.description || '结合当前节气调整饮食与作息。' }}</text>
      </view>
    </view>

    <view class="card empty-card" v-else>
      <uni-icons type="info" size="44" color="#94a3b8" />
      <text class="empty-title">暂无节气内容</text>
      <text class="empty-desc">稍后再来看看</text>
    </view>
  </view>
</template>

<script>
import { fitApi } from '@/utils/api.js';

export default {
  data() {
    return {
      topicList: []
    };
  },
  onShow() {
    this.loadTopics();
  },
  methods: {
    async loadTopics() {
      try {
        const data = await fitApi.getCurrentSeasonTopic();
        this.topicList = Array.isArray(data) ? data : (data ? [data] : []);
      } catch (error) {
        this.topicList = [];
      }
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.season-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.intro-card {
  margin-bottom: 16rpx;
}

.topic-list {
  display: flex;
  flex-direction: column;
  gap: 14rpx;
}

.topic-item {
  display: flex;
  flex-direction: column;
  gap: 10rpx;
}

.topic-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12rpx;
}

.topic-title {
  font-size: 30rpx;
  font-weight: 600;
  color: $text-primary;
}

.topic-date {
  font-size: 22rpx;
  color: $text-muted;
  flex-shrink: 0;
}

.topic-content {
  font-size: 25rpx;
  line-height: 1.7;
  color: $text-secondary;
}

.empty-card {
  text-align: center;
  padding: 72rpx 24rpx;
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
</style>
