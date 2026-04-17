<template>
  <view class="page-content community-page">
    <view class="hero-section community-header">
      <view class="header-top">
        <view>
          <text class="text-lg font-bold text-primary">轻体社区</text>
          <text class="text-sm text-secondary subtitle">分享减脂心得，互相鼓励成长</text>
        </view>
        <button class="btn-publish" @tap="goPublish">
          <uni-icons type="plus" size="16" color="#fff" />
          <text>发布</text>
        </button>
      </view>
      <view class="stats-row">
        <view class="stat-card">
          <text class="text-sm text-muted">我的积分</text>
          <text class="text-base font-bold text-primary">{{ points }}</text>
        </view>
        <view class="stat-card">
          <text class="text-sm text-muted">社区动态</text>
          <text class="text-base font-bold text-primary">{{ totalPosts }}</text>
        </view>
      </view>
    </view>

    <view class="card filter-card">
      <text class="text-sm text-secondary">内容分类</text>
      <picker mode="selector" :range="categoryLabels" :value="currentCategoryIndex" @change="onCategoryChange">
        <view class="picker-trigger">
          <text class="picker-text">{{ categories[currentCategoryIndex].label }}</text>
          <uni-icons type="down" size="14" color="#64748b" />
        </view>
      </picker>
    </view>

    <view class="posts-list" v-if="posts.length">
      <view class="card post-card" v-for="item in posts" :key="item.id" @tap="goDetail(item.id)">
        <view class="post-header">
          <view class="user-info">
            <view class="user-avatar">
              <image v-if="item.userAvatar" :src="normalizeImageUrl(item.userAvatar)" mode="aspectFill" />
              <view v-else class="avatar-fallback">
                <text>{{ item.authorName ? item.authorName.slice(0, 1) : '用' }}</text>
              </view>
            </view>
            <view class="user-detail">
              <text class="user-name">{{ item.authorName || '匿名用户' }}</text>
              <text class="post-time">{{ formatTime(item.createTime) }}</text>
            </view>
          </view>
          <view class="post-category" v-if="item.category">
            <text>{{ getCategoryLabel(item.category) }}</text>
          </view>
        </view>

        <view class="post-content">
          <text class="post-title">{{ item.title }}</text>
          <text class="post-excerpt">{{ item.content }}</text>
        </view>

        <view v-if="item.imageList && item.imageList.length" class="image-grid">
          <view class="image-item" v-for="(img, idx) in item.imageList.slice(0, 3)" :key="img + idx">
            <image :src="normalizeImageUrl(img)" mode="aspectFill" />
            <view v-if="item.imageList.length > 3 && idx === 2" class="image-more">
              <text>+{{ item.imageList.length - 3 }}</text>
            </view>
          </view>
        </view>

        <view class="post-stats">
          <view class="stat" @tap.stop="toggleLike(item.id)">
            <image class="stat-icon" :src="item.isLiked ? '/static/icon_fit/wancheng.png' : '/static/icon_fit/zan.png'" mode="aspectFit" />
            <text>{{ item.likeCount || 0 }}</text>
          </view>
          <view class="stat">
            <image class="stat-icon" src="/static/icon_fit/xiaoxi.png" mode="aspectFit" />
            <text>{{ item.commentCount || 0 }}</text>
          </view>
          <view class="stat">
            <image class="stat-icon" src="/static/icon_fit/yulan.png" mode="aspectFit" />
            <text>{{ item.viewCount || 0 }}</text>
          </view>
        </view>
      </view>
    </view>

    <view class="card empty-state" v-else>
      <uni-icons type="info" size="44" color="#94a3b8" />
      <text class="empty-title">暂无内容</text>
      <text class="empty-desc">快去发布第一篇文章吧</text>
      <button class="btn-publish-empty" @tap="goPublish">发布文章</button>
    </view>

    <view class="load-more" v-if="posts.length && !noMore">
      <button class="btn-load" @tap="loadMore">加载更多</button>
    </view>
  </view>
</template>

<script>
import { fitApi } from '@/utils/api.js';
import { resolveFileUrl } from '@/utils/request.js';

export default {
  data() {
    return {
      points: 0,
      posts: [],
      totalPosts: 0,
      currentCategory: '',
      currentCategoryIndex: 0,
      currentPage: 1,
      pageSize: 10,
      noMore: false,
      categories: [
        { label: '全部', value: '' },
        { label: '减脂心得', value: 'weight-loss' },
        { label: '饮食分享', value: 'diet' },
        { label: '运动打卡', value: 'workout' },
        { label: '成果展示', value: 'achievement' },
        { label: '问题求助', value: 'help' }
      ]
    };
  },
  computed: {
    categoryLabels() {
      return this.categories.map((item) => item.label);
    }
  },
  onShow() {
    this.loadAll();
  },
  methods: {
    normalizeImageUrl(url) {
      return resolveFileUrl(url);
    },
    formatTime(value) {
      if (!value) return '';
      const date = new Date(value);
      const now = new Date();
      const diff = now - date;

      if (diff < 60000) return '刚刚';
      if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`;
      if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`;
      if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`;

      return String(value).replace('T', ' ').slice(0, 10);
    },
    getCategoryLabel(value) {
      const cat = this.categories.find((c) => c.value === value);
      return cat ? cat.label : value;
    },
    parseImageList(post) {
      if (Array.isArray(post.imageList)) return post.imageList;
      if (!post.imageUrls) return [];
      try {
        const parsed = JSON.parse(post.imageUrls);
        return Array.isArray(parsed) ? parsed : [];
      } catch (error) {
        return String(post.imageUrls)
          .split(',')
          .map((s) => s.trim())
          .filter(Boolean);
      }
    },
    async loadAll() {
      this.currentPage = 1;
      this.noMore = false;
      await Promise.all([this.loadPosts(), this.loadPoints()]);
    },
    async loadPoints() {
      try {
        const data = await fitApi.myPoints();
        this.points = data?.account?.availablePoint || 0;
      } catch (error) {
        this.points = 0;
      }
    },
    async loadPosts() {
      try {
        const page = await fitApi.listCommunityPosts({
          current: this.currentPage,
          size: this.pageSize,
          category: this.currentCategory
        });

        const newPosts = (page.records || []).map((item) => ({
          ...item,
          imageList: this.parseImageList(item),
          isLiked: false
        }));

        if (this.currentPage === 1) {
          this.posts = newPosts;
        } else {
          this.posts = [...this.posts, ...newPosts];
        }

        this.totalPosts = page.total || 0;
        this.noMore = newPosts.length < this.pageSize;
      } catch (error) {
        if (this.currentPage === 1) {
          this.posts = [];
        }
      }
    },
    onCategoryChange(e) {
      const idx = Number(e.detail.value || 0);
      this.currentCategoryIndex = idx;
      this.currentCategory = this.categories[idx]?.value || '';
      this.loadAll();
    },
    async loadMore() {
      this.currentPage += 1;
      await this.loadPosts();
    },
    async toggleLike(postId) {
      try {
        const post = this.posts.find((p) => p.id === postId);
        if (!post) return;

        if (post.isLiked) {
          post.isLiked = false;
          post.likeCount = Math.max(0, (post.likeCount || 0) - 1);
        } else {
          post.isLiked = true;
          post.likeCount = (post.likeCount || 0) + 1;
          uni.showToast({ title: '点赞成功', icon: 'success', duration: 1000 });
        }

        await fitApi.likeCommunityPost(postId);
      } catch (error) {
        uni.showToast({ title: error.message || '操作失败', icon: 'none' });
      }
    },
    goDetail(id) {
      uni.navigateTo({ url: `/pages/fit/community-detail?id=${id}` });
    },
    goPublish() {
      uni.navigateTo({ url: '/pages/fit/community-publish' });
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.community-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 48rpx;
}

.community-header {
  margin-bottom: 16rpx;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.subtitle {
  display: block;
  margin-top: 6rpx;
}

.btn-publish {
  display: flex;
  align-items: center;
  gap: 6rpx;
  background: $primary-color;
  color: #fff;
  border: none;
  border-radius: 999rpx;
  padding: 0 22rpx;
  height: 56rpx;
  line-height: 56rpx;
  font-size: 24rpx;
}

.stats-row {
  margin-top: 16rpx;
  display: flex;
  gap: 12rpx;
}

.stat-card {
  flex: 1;
  background: #f6f9ff;
  border-radius: 14rpx;
  padding: 14rpx;

  .text-base {
    display: block;
    margin-top: 6rpx;
  }
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

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 14rpx;
}

.post-card {
  padding: 22rpx;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 14rpx;
}

.user-info {
  display: flex;
  gap: 12rpx;
  flex: 1;
}

.user-avatar {
  width: 56rpx;
  height: 56rpx;
  border-radius: 28rpx;
  overflow: hidden;
  background: #e8f0ff;
  flex-shrink: 0;

  image {
    width: 100%;
    height: 100%;
    display: block;
  }
}

.avatar-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: $primary-color;
  font-size: 24rpx;
  font-weight: 600;
}

.user-detail {
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.user-name {
  font-size: 26rpx;
  font-weight: 600;
  color: $text-primary;
}

.post-time {
  font-size: 22rpx;
  color: $text-muted;
}

.post-category {
  padding: 4rpx 12rpx;
  background: #edf3ff;
  border-radius: 20rpx;
  font-size: 22rpx;
  color: $primary-color;
}

.post-content {
  margin-bottom: 14rpx;
}

.post-title {
  font-size: 28rpx;
  font-weight: 600;
  color: $text-primary;
  display: block;
  margin-bottom: 8rpx;
}

.post-excerpt {
  font-size: 24rpx;
  color: $text-secondary;
  line-height: 1.6;
  display: -webkit-box;
  overflow: hidden;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8rpx;
  margin-bottom: 14rpx;
}

.image-item {
  position: relative;
  height: 160rpx;
  border-radius: 12rpx;
  overflow: hidden;
  background: #f1f5f9;

  image {
    width: 100%;
    height: 100%;
    display: block;
  }
}

.image-more {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;

  text {
    color: #fff;
    font-size: 28rpx;
    font-weight: 700;
  }
}

.post-stats {
  display: flex;
  gap: 28rpx;
  padding-top: 14rpx;
  border-top: 1rpx solid #edf1f7;
}

.stat {
  display: flex;
  align-items: center;
  gap: 8rpx;
  font-size: 22rpx;
  color: #94a3b8;
}

.stat-icon {
  width: 28rpx;
  height: 28rpx;
}

.empty-state {
  text-align: center;
  padding: 72rpx 24rpx;
}

.empty-title {
  font-size: 28rpx;
  font-weight: 600;
  color: $text-primary;
  margin-top: 14rpx;
}

.empty-desc {
  font-size: 24rpx;
  color: $text-muted;
  margin-top: 8rpx;
}

.btn-publish-empty {
  margin-top: 28rpx;
  background: $primary-color;
  color: #fff;
  border: none;
  border-radius: 999rpx;
  height: 72rpx;
  line-height: 72rpx;
  padding: 0 44rpx;
  font-size: 26rpx;
}

.load-more {
  padding: 24rpx 0 12rpx;
  text-align: center;
}

.btn-load {
  background: #fff;
  color: $primary-color;
  border: 1rpx solid #dbe7ff;
  border-radius: 999rpx;
  height: 64rpx;
  line-height: 64rpx;
  padding: 0 36rpx;
  font-size: 24rpx;
}
</style>
