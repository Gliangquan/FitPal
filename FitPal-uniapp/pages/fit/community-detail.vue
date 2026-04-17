<template>
  <view class="detail-page">

    <!-- 文章内容 -->
    <view class="article-container" v-if="post">
      <!-- 文章头部 -->
      <view class="article-header">
        <text class="article-title">{{ post.title }}</text>
        
        <view class="article-meta">
          <view class="user-info">
            <view class="user-avatar">
              <image v-if="post.userAvatar" :src="normalizeImageUrl(post.userAvatar)" mode="aspectFill" />
              <view v-else class="avatar-fallback">
                <text>{{ post.authorName ? post.authorName.slice(0, 1) : '用' }}</text>
              </view>
            </view>
            <view class="user-detail">
              <text class="user-name">{{ post.authorName || '匿名用户' }}</text>
              <text class="post-time">{{ formatTime(post.createTime) }}</text>
            </view>
          </view>
          <view class="post-category" v-if="post.category">
            <text>{{ getCategoryLabel(post.category) }}</text>
          </view>
        </view>
      </view>

      <!-- 文章内容 -->
      <view class="article-content">
        <text>{{ post.content }}</text>
      </view>

      <!-- 文章图片 -->
      <view v-if="post.imageList && post.imageList.length" class="article-images">
        <image
          v-for="(img, idx) in post.imageList"
          :key="img + idx"
          :src="normalizeImageUrl(img)"
          mode="widthFix"
          class="article-image"
        />
      </view>

      <!-- 互动数据 -->
      <view class="article-stats">
        <view class="stat-item">
          <uni-icons type="eye" size="18" color="#999" />
          <text>{{ post.viewCount || 0 }} 浏览</text>
        </view>
        <view class="stat-item">
          <uni-icons type="heart" size="18" color="#999" />
          <text>{{ post.likeCount || 0 }} 点赞</text>
        </view>
        <view class="stat-item">
          <uni-icons type="chatbubble" size="18" color="#999" />
          <text>{{ post.commentCount || 0 }} 评论</text>
        </view>
      </view>

      <!-- 分割线 -->
      <view class="divider" />

      <!-- 评论区 -->
      <view class="comments-section">
        <text class="section-title">评论 ({{ comments.length }})</text>

        <!-- 评论列表 -->
        <view v-if="comments.length" class="comments-list">
          <view class="comment-item" v-for="comment in comments" :key="comment.id">
            <view class="comment-header">
              <view class="user-info">
                <view class="user-avatar-sm">
                  <image v-if="comment.userAvatar" :src="normalizeImageUrl(comment.userAvatar)" mode="aspectFill" />
                  <view v-else class="avatar-fallback-sm">
                    <text>{{ comment.userName ? comment.userName.slice(0, 1) : '用' }}</text>
                  </view>
                </view>
                <view class="user-detail-sm">
                  <text class="user-name-sm">{{ comment.userName || '匿名用户' }}</text>
                  <text class="comment-time">{{ formatTime(comment.createTime) }}</text>
                </view>
              </view>
            </view>
            <text class="comment-content">{{ comment.content }}</text>
          </view>
        </view>

        <!-- 无评论提示 -->
        <view v-else class="no-comments">
          <text>暂无评论，快来评论吧</text>
        </view>
      </view>
    </view>

    <!-- 加载中 -->
    <view v-else class="loading-state">
      <uni-icons type="info" size="48" color="#c0c4cc" />
      <text>加载中...</text>
    </view>

    <!-- 底部操作栏 -->
    <view class="action-bar">
      <view class="action-item" @tap="toggleLike">
        <uni-icons :type="isLiked ? 'heart-filled' : 'heart'" :size="24" :color="isLiked ? '#f44' : '#999'" />
        <text>{{ likeCount }}</text>
      </view>
      <view class="action-item" @tap="focusComment">
        <uni-icons type="chatbubble" size="24" color="#999" />
        <text>评论</text>
      </view>
      <view class="action-item" @tap="sharePost">
        <uni-icons type="share" size="24" color="#999" />
        <text>分享</text>
      </view>
    </view>

    <!-- 评论输入框 -->
    <view class="comment-input-bar">
      <input
        ref="commentInput"
        v-model="commentText"
        type="text"
        placeholder="写下你的评论..."
        class="comment-input"
        @keyup.enter="submitComment"
      />
      <button class="btn-submit" @tap="submitComment" :disabled="!commentText.trim()">
        发送
      </button>
    </view>

  </view>
</template>

<script>
import { fitApi } from '@/utils/api.js';
import { resolveFileUrl } from '@/utils/request.js';

export default {
  data() {
    return {
      postId: '',
      post: null,
      comments: [],
      commentText: '',
      isLiked: false,
      likeCount: 0,
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
  onLoad(options) {
    this.postId = options.id;
    this.loadPost();
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
      if (diff < 3600000) return Math.floor(diff / 60000) + '分钟前';
      if (diff < 86400000) return Math.floor(diff / 3600000) + '小时前';
      if (diff < 604800000) return Math.floor(diff / 86400000) + '天前';
      
      return String(value).replace('T', ' ').slice(0, 10);
    },
    getCategoryLabel(value) {
      const cat = this.categories.find(c => c.value === value);
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
    async loadPost() {
      try {
        // 获取文章详情（需要后端接口）
        const post = await fitApi.getCommunityPost(this.postId);
        this.post = {
          ...post,
          imageList: this.parseImageList(post)
        };
        this.likeCount = post.likeCount || 0;
        
        // 加载评论
        await this.loadComments();
      } catch (error) {
        uni.showToast({ title: '加载失败', icon: 'none' });
      }
    },
    async loadComments() {
      try {
        // 获取评论列表（需要后端接口）
        this.comments = await fitApi.getPostComments(this.postId) || [];
      } catch (error) {
        this.comments = [];
      }
    },
    async toggleLike() {
      try {
        if (this.isLiked) {
          this.isLiked = false;
          this.likeCount = Math.max(0, this.likeCount - 1);
        } else {
          this.isLiked = true;
          this.likeCount++;
          uni.showToast({ title: '点赞成功', icon: 'success', duration: 1000 });
        }
        await fitApi.likeCommunityPost(this.postId);
      } catch (error) {
        uni.showToast({ title: error.message || '操作失败', icon: 'none' });
      }
    },
    focusComment() {
      this.$refs.commentInput?.focus();
    },
    async submitComment() {
      if (!this.commentText.trim()) {
        return uni.showToast({ title: '请输入评论内容', icon: 'none' });
      }

      try {
        // 提交评论（需要后端接口）
        await fitApi.addPostComment(this.postId, {
          content: this.commentText
        });
        
        uni.showToast({ title: '评论成功', icon: 'success' });
        this.commentText = '';
        
        // 重新加载评论
        await this.loadComments();
      } catch (error) {
        uni.showToast({ title: error.message || '评论失败', icon: 'none' });
      }
    },
    sharePost() {
      uni.showToast({ title: '分享功能开发中', icon: 'none' });
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.detail-page {
  min-height: 100vh;
  background: #f5f6fa;
  padding-bottom: 120rpx;
}

/* ── 文章容器 ── */
.article-container {
  background: #fff;
  padding: 32rpx 24rpx;
}

.article-header {
  margin-bottom: 24rpx;
}

.article-title {
  font-size: 32rpx;
  font-weight: 700;
  color: $text-primary;
  line-height: 1.5;
  display: block;
  margin-bottom: 16rpx;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.user-info {
  display: flex;
  gap: 12rpx;
}

.user-avatar {
  width: 56rpx;
  height: 56rpx;
  border-radius: 28rpx;
  overflow: hidden;
  background: $primary-color;

  image {
    width: 100%;
    height: 100%;
    display: block;
  }

  .avatar-fallback {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 24rpx;
    font-weight: 600;
  }
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
  background: rgba($primary-color, 0.1);
  border-radius: 20rpx;
  font-size: 22rpx;
  color: $primary-color;
  font-weight: 500;
}

/* ── 文章内容 ── */
.article-content {
  font-size: 26rpx;
  line-height: 1.8;
  color: $text-secondary;
  margin-bottom: 24rpx;
}

/* ── 文章图片 ── */
.article-images {
  margin-bottom: 24rpx;
}

.article-image {
  width: 100%;
  border-radius: 12rpx;
  margin-bottom: 12rpx;
}

/* ── 互动数据 ── */
.article-stats {
  display: flex;
  gap: 32rpx;
  padding: 16rpx 0;
  border-top: 1rpx solid #f0f0f0;
  border-bottom: 1rpx solid #f0f0f0;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
  font-size: 22rpx;
  color: $text-muted;
}

/* ── 分割线 ── */
.divider {
  height: 12rpx;
  background: #f5f6fa;
  margin: 24rpx -24rpx;
}

/* ── 评论区 ── */
.comments-section {
  padding: 24rpx 0;
}

.section-title {
  font-size: 28rpx;
  font-weight: 600;
  color: $text-primary;
  display: block;
  margin-bottom: 16rpx;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.comment-item {
  padding: 16rpx;
  background: #f8f9fa;
  border-radius: 12rpx;
}

.comment-header {
  margin-bottom: 12rpx;
}

.user-avatar-sm {
  width: 40rpx;
  height: 40rpx;
  border-radius: 20rpx;
  overflow: hidden;
  background: $primary-color;

  image {
    width: 100%;
    height: 100%;
    display: block;
  }

  .avatar-fallback-sm {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 18rpx;
    font-weight: 600;
  }
}

.user-detail-sm {
  display: flex;
  flex-direction: column;
  gap: 2rpx;
}

.user-name-sm {
  font-size: 24rpx;
  font-weight: 600;
  color: $text-primary;
}

.comment-time {
  font-size: 20rpx;
  color: $text-muted;
}

.comment-content {
  font-size: 24rpx;
  line-height: 1.6;
  color: $text-secondary;
}

.no-comments {
  padding: 40rpx 0;
  text-align: center;
  color: $text-muted;
  font-size: 24rpx;
}

/* ── 加载状态 ── */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 120rpx 24rpx;
  text-align: center;
  color: $text-muted;
}

/* ── 底部操作栏 ── */
.action-bar {
  position: fixed;
  bottom: 120rpx;
  left: 0;
  right: 0;
  height: 80rpx;
  background: #fff;
  border-top: 1rpx solid #f0f0f0;
  display: flex;
  justify-content: space-around;
  align-items: center;
  z-index: 99;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4rpx;
  font-size: 20rpx;
  color: $text-muted;
}

/* ── 评论输入框 ── */
.comment-input-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 120rpx;
  background: #fff;
  border-top: 1rpx solid #f0f0f0;
  display: flex;
  align-items: center;
  gap: 12rpx;
  padding: 16rpx 24rpx;
  box-sizing: border-box;
  z-index: 100;
}

.comment-input {
  flex: 1;
  height: 80rpx;
  padding: 12rpx 16rpx;
  border: 1rpx solid #e0e0e0;
  border-radius: 40rpx;
  font-size: 24rpx;
  background: #f8f9fa;
}

.btn-submit {
  padding: 12rpx 32rpx;
  background: $primary-color;
  color: #fff;
  border-radius: 40rpx;
  font-size: 24rpx;
  border: none;
  font-weight: 600;

  &:disabled {
    opacity: 0.5;
  }
}
</style>
