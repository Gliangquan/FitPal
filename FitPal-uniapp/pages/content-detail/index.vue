<template>
  <view class="page-content detail-page">
    <view class="card" v-if="loading">
      <text class="text-sm text-muted">加载中...</text>
    </view>

    <view class="card" v-else-if="content">
      <text class="title">{{ content.title || '内容详情' }}</text>
      <text class="meta" v-if="content.stageTag">阶段：{{ content.stageTag }}</text>
      <text class="summary" v-if="content.summary">{{ content.summary }}</text>
      <text class="body" v-if="content.contentBody">{{ content.contentBody }}</text>
      <text class="body" v-else>暂无详细正文</text>

      <view class="link-wrap" v-if="content.contentUrl">
        <button class="btn-link" @tap="openContentUrl">查看原文/视频</button>
      </view>
    </view>

    <view class="card" v-else>
      <text class="text-sm text-muted">内容不存在或已下架</text>
    </view>
  </view>
</template>

<script>
import { fitApi } from '@/utils/api.js';

export default {
  data() {
    return {
      loading: false,
      content: null
    };
  },
  onLoad(options) {
    const id = Number(options?.id || 0);
    if (!id) {
      uni.showToast({ title: '参数错误', icon: 'none' });
      setTimeout(() => uni.navigateBack(), 600);
      return;
    }
    this.loadDetail(id);
  },
  methods: {
    async loadDetail(id) {
      this.loading = true;
      try {
        this.content = await fitApi.getContentDetail(id);
      } catch (error) {
        this.content = null;
        uni.showToast({ title: error.message || '加载失败', icon: 'none' });
      } finally {
        this.loading = false;
      }
    },
    openContentUrl() {
      const url = String(this.content?.contentUrl || '').trim();
      if (!url) return;
      uni.setClipboardData({
        data: url,
        success: () => {
          uni.showToast({ title: '链接已复制', icon: 'success' });
        }
      });
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.detail-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.title {
  display: block;
  font-size: 34rpx;
  font-weight: 700;
  color: $text-primary;
  line-height: 1.5;
}

.meta {
  display: block;
  margin-top: 12rpx;
  font-size: 22rpx;
  color: $text-muted;
}

.summary {
  display: block;
  margin-top: 14rpx;
  font-size: 26rpx;
  color: $text-secondary;
  line-height: 1.7;
}

.body {
  display: block;
  margin-top: 14rpx;
  font-size: 26rpx;
  color: $text-secondary;
  line-height: 1.8;
  white-space: pre-wrap;
}

.link-wrap {
  margin-top: 20rpx;
}

.btn-link {
  background: $primary-color;
  color: #fff;
  border: none;
  border-radius: 999rpx;
  height: 72rpx;
  line-height: 72rpx;
  font-size: 26rpx;
}
</style>
