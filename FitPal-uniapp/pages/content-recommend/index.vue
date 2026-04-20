<template>
  <view class="page-content recommend-page">
    <view class="hero-section intro-card">
      <view>
        <text class="text-lg font-bold text-primary">{{ pageTitle }}</text>
        <text class="text-sm text-secondary" style="display:block;margin-top:6rpx;">{{ pageDesc }}</text>
      </view>
    </view>

    <view v-if="isSeasonMode && seasonTopic" class="card season-card">
      <text class="season-title">{{ seasonTopic.title }}</text>
      <text class="season-desc">{{ seasonTopic.routineAdvice || seasonTopic.recipeText || '结合当前节气调整饮食与作息。' }}</text>
    </view>

    <view class="card filter-card" v-if="!isSeasonMode">
      <text class="text-sm text-secondary">筛选标签</text>
      <picker mode="selector" :range="tagLabels" :value="currentTagIndex" @change="onTagChange">
        <view class="picker-trigger">
          <text class="picker-text">{{ tags[currentTagIndex].label }}</text>
          <uni-icons type="down" size="14" color="#64748b" />
        </view>
      </picker>
    </view>

    <view class="content-list" v-if="contentList.length">
      <view class="card content-item" v-for="item in contentList" :key="item.id" @tap="viewContent(item)">
        <view class="content-cover" v-if="item.coverImage">
          <image :src="resolveImageUrl(item.coverImage)" mode="aspectFill" />
          <view class="content-type" v-if="item.contentType === 'video'">
            <uni-icons type="videocam-filled" size="16" color="#fff" />
          </view>
        </view>
        <view class="content-info">
          <text class="content-title">{{ item.title }}</text>
          <text class="content-summary">{{ item.summary || '暂无摘要' }}</text>
          <view class="content-meta">
            <view class="meta-item">
              <uni-icons type="eye" size="14" color="#94a3b8" />
              <text>{{ item.viewCount || 0 }}</text>
            </view>
            <view class="meta-item">
              <uni-icons type="heart" size="14" color="#94a3b8" />
              <text>{{ item.likeCount || 0 }}</text>
            </view>
            <text class="meta-date">{{ item.publishTime || '' }}</text>
          </view>
        </view>
      </view>
    </view>

    <view class="card empty-card" v-else>
      <uni-icons type="info" size="44" color="#94a3b8" />
      <text class="empty-title">暂无推荐内容</text>
      <text class="empty-desc">完善个人信息后将获得更精准推荐</text>
    </view>
  </view>
</template>

<script>
import { fitApi } from '@/utils/api.js';
import { resolveFileUrl } from '@/utils/request.js';

export default {
  data() {
    return {
      currentTag: '',
      currentTagIndex: 0,
      mode: 'recommend',
      seasonTopic: null,
      tags: [
        { label: '全部', value: '' },
        { label: '减脂知识', value: 'weight-loss' },
        { label: '饮食营养', value: 'nutrition' },
        { label: '运动健身', value: 'workout' },
        { label: '健康生活', value: 'lifestyle' },
        { label: '心理调节', value: 'mental' }
      ],
      contentList: []
    };
  },
  computed: {
    isSeasonMode() {
      return this.mode === 'season';
    },
    pageTitle() {
      return this.isSeasonMode ? '节气专栏' : '个性化推荐';
    },
    pageDesc() {
      return this.isSeasonMode ? '查看当前节气专题与相关推荐内容' : '根据减脂阶段和身体指标推送内容';
    },
    tagLabels() {
      return this.tags.map((item) => item.label);
    }
  },
  onLoad(options) {
    this.mode = options?.mode === 'season' ? 'season' : 'recommend';
  },
  onShow() {
    this.loadContent();
    if (this.isSeasonMode) {
      this.loadSeasonTopic();
    }
  },
  methods: {
    resolveImageUrl(url) {
      return resolveFileUrl(url);
    },
    async loadSeasonTopic() {
      try {
        const data = await fitApi.getCurrentSeasonTopic();
        this.seasonTopic = Array.isArray(data) ? (data[0] || null) : data;
      } catch (error) {
        this.seasonTopic = null;
      }
    },
    async loadContent() {
      try {
        this.contentList = await fitApi.recommendContent(this.currentTag, 20);
      } catch (error) {
        this.contentList = [];
      }
    },
    onTagChange(e) {
      const idx = Number(e.detail.value || 0);
      this.currentTagIndex = idx;
      this.currentTag = this.tags[idx]?.value || '';
      this.loadContent();
    },
    viewContent(item) {
      uni.navigateTo({
        url: `/pages/content-detail/index?id=${item.id}`
      });
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.recommend-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.intro-card {
  margin-bottom: 16rpx;
}

.season-card {
  margin-bottom: 16rpx;
}

.season-title {
  display: block;
  font-size: 30rpx;
  font-weight: 600;
  color: $text-primary;
}

.season-desc {
  display: block;
  margin-top: 10rpx;
  font-size: 25rpx;
  line-height: 1.7;
  color: $text-secondary;
}

.filter-card {
  margin-bottom: 16rpx;
  padding: 18rpx 20rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.picker-trigger {
  min-width: 220rpx;
  border: 1rpx solid #dbe7ff;
  background: #f8fbff;
  border-radius: 999rpx;
  height: 56rpx;
  line-height: 56rpx;
  padding: 0 18rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10rpx;
}

.picker-text {
  font-size: 24rpx;
  color: #334155;
}

.content-list {
  display: flex;
  flex-direction: column;
  gap: 14rpx;
}

.content-item {
  padding: 0;
  overflow: hidden;
}

.content-cover {
  position: relative;
  width: 100%;
  height: 320rpx;
  background: #f1f5f9;

  image {
    width: 100%;
    height: 100%;
    display: block;
  }
}

.content-type {
  position: absolute;
  top: 14rpx;
  right: 14rpx;
  width: 42rpx;
  height: 42rpx;
  border-radius: 21rpx;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
}

.content-info {
  padding: 16rpx;
}

.content-title {
  font-size: 28rpx;
  font-weight: 600;
  color: $text-primary;
  line-height: 1.5;
  display: -webkit-box;
  overflow: hidden;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.content-summary {
  display: block;
  margin-top: 10rpx;
  font-size: 24rpx;
  color: $text-secondary;
  line-height: 1.6;
  display: -webkit-box;
  overflow: hidden;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.content-meta {
  margin-top: 12rpx;
  display: flex;
  align-items: center;
  gap: 18rpx;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6rpx;
  font-size: 22rpx;
  color: #94a3b8;
}

.meta-date {
  margin-left: auto;
  font-size: 22rpx;
  color: #94a3b8;
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
