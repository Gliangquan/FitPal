<template>
  <view class="coach-page">

    <!-- 教练信息卡片 -->
    <view class="coach-card" v-if="coach">
      <view class="coach-header">
        <view class="coach-avatar">
          <image v-if="coach.avatar" :src="resolveImageUrl(coach.avatar)" mode="aspectFill" />
          <view v-else class="avatar-fallback">
            <uni-icons type="person-filled" size="32" color="#fff" />
          </view>
        </view>
        <view class="coach-info">
          <text class="coach-name">{{ coach.name || '专业教练' }}</text>
          <view class="coach-rating">
            <uni-rate :value="coach.rating || 5" size="16" readonly />
            <text class="rating-text">{{ coach.rating || 5 }} 分</text>
          </view>
          <text class="coach-cert">{{ coach.certification || '国家认证健身教练' }}</text>
        </view>
      </view>

      <view class="coach-stats">
        <view class="stat-item">
          <text class="stat-value">{{ coach.planCount || 0 }}</text>
          <text class="stat-label">方案数</text>
        </view>
        <view class="stat-divider" />
        <view class="stat-item">
          <text class="stat-value">{{ coach.studentCount || 0 }}</text>
          <text class="stat-label">学员数</text>
        </view>
        <view class="stat-divider" />
        <view class="stat-item">
          <text class="stat-value">{{ coach.experience || 0 }}</text>
          <text class="stat-label">从业年限</text>
        </view>
      </view>

      <view class="coach-intro">
        <text class="intro-title">教练简介</text>
        <text class="intro-content">{{ coach.introduction || '暂无简介' }}</text>
      </view>
    </view>

    <!-- 无教练提示 -->
    <view class="empty-card" v-else>
      <uni-icons type="info-filled" size="48" color="#c0c4cc" />
      <text class="empty-title">还没有专属教练</text>
      <text class="empty-desc">完成问卷后系统将为您匹配教练</text>
      <button class="btn-goto" @tap="goQuestionnaire">去填写问卷</button>
    </view>

    <!-- 功能菜单 -->
    <view class="menu-card" v-if="coach">
      <view class="menu-item" @tap="goConsultation">
        <view class="menu-left">
          <view class="menu-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <uni-icons type="chatbubble-filled" size="20" color="#fff" />
          </view>
          <text class="menu-title">在线咨询</text>
        </view>
        <uni-icons type="forward" size="16" color="#c0c4cc" />
      </view>
      <view class="menu-divider" />

      <view class="menu-item" @tap="showRateDialog">
        <view class="menu-left">
          <view class="menu-icon" style="background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);">
            <uni-icons type="star-filled" size="20" color="#fff" />
          </view>
          <text class="menu-title">评价教练</text>
        </view>
        <uni-icons type="forward" size="16" color="#c0c4cc" />
      </view>
    </view>

    <!-- 我的评价记录 -->
    <view class="reviews-card" v-if="reviews.length">
      <view class="card-title">我的评价</view>
      <view class="review-item" v-for="item in reviews" :key="item.id">
        <view class="review-header">
          <uni-rate :value="item.rating" size="14" readonly />
          <text class="review-date">{{ item.createTime }}</text>
        </view>
        <text class="review-content">{{ item.content }}</text>
      </view>
    </view>

    <!-- 评价弹窗 -->
    <uni-popup ref="ratePopup" type="center">
      <view class="rate-dialog">
        <text class="dialog-title">评价教练</text>
        
        <view class="rate-section">
          <text class="rate-label">服务评分</text>
          <uni-rate v-model="rateForm.rating" size="24" />
        </view>

        <view class="rate-section">
          <text class="rate-label">评价内容</text>
          <uni-easyinput
            v-model="rateForm.content"
            type="textarea"
            placeholder="说说您的真实体验..."
            :maxlength="200"
          />
        </view>

        <view class="dialog-btns">
          <button class="btn-cancel" @tap="closeRateDialog">取消</button>
          <button class="btn-confirm" @tap="submitRate">提交</button>
        </view>
      </view>
    </uni-popup>

  </view>
</template>

<script>
import { fitApi } from '@/utils/api.js';
import { resolveFileUrl } from '@/utils/request.js';

export default {
  data() {
    return {
      coach: null,
      reviews: [],
      rateForm: {
        rating: 5,
        content: ''
      }
    };
  },
  onShow() {
    this.loadCoach();
    this.loadReviews();
  },
  methods: {
    resolveImageUrl(url) {
      return resolveFileUrl(url);
    },
    async loadCoach() {
      try {
        this.coach = await fitApi.getMyCoach();
      } catch (error) {
        this.coach = null;
      }
    },
    async loadReviews() {
      try {
        this.reviews = await fitApi.getMyCoachReviews();
      } catch (error) {
        this.reviews = [];
      }
    },
    goQuestionnaire() {
      uni.navigateTo({ url: '/pages/fit/questionnaire' });
    },
    goConsultation() {
      uni.navigateTo({ url: '/pages/consultation/index' });
    },
    showRateDialog() {
      this.$refs.ratePopup.open();
    },
    closeRateDialog() {
      this.$refs.ratePopup.close();
      this.rateForm = { rating: 5, content: '' };
    },
    async submitRate() {
      if (!this.rateForm.content.trim()) {
        return uni.showToast({ title: '请填写评价内容', icon: 'none' });
      }
      try {
        await fitApi.rateCoach({
          coachId: this.coach.id,
          rating: this.rateForm.rating,
          content: this.rateForm.content.trim()
        });
        uni.showToast({ title: '评价成功', icon: 'success' });
        this.closeRateDialog();
        this.loadReviews();
      } catch (error) {
        uni.showToast({ title: error.message || '评价失败', icon: 'none' });
      }
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.coach-page {
  min-height: 100vh;
  background: #f5f6fa;
  padding: 24rpx;
  padding-bottom: 60rpx;
  box-sizing: border-box;
}

/* ── 教练信息卡片 ── */
.coach-card {
  background: #fff;
  border-radius: $radius-lg;
  padding: 32rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.coach-header {
  display: flex;
  gap: 24rpx;
  margin-bottom: 24rpx;
}

.coach-avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 60rpx;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  flex-shrink: 0;

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
  }
}

.coach-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.coach-name {
  font-size: 32rpx;
  font-weight: 600;
  color: $text-primary;
}

.coach-rating {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.rating-text {
  font-size: 24rpx;
  color: $text-muted;
}

.coach-cert {
  font-size: 24rpx;
  color: $text-secondary;
  background: rgba(102, 126, 234, 0.1);
  padding: 4rpx 16rpx;
  border-radius: 20rpx;
  align-self: flex-start;
}

.coach-stats {
  display: flex;
  background: #f8f9fa;
  border-radius: 12rpx;
  padding: 24rpx;
  margin-bottom: 24rpx;
}

.stat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
}

.stat-value {
  font-size: 36rpx;
  font-weight: 700;
  color: $primary-color;
}

.stat-label {
  font-size: 22rpx;
  color: $text-muted;
}

.stat-divider {
  width: 1rpx;
  background: #e0e0e0;
  margin: 0 24rpx;
}

.coach-intro {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.intro-title {
  font-size: 28rpx;
  font-weight: 600;
  color: $text-primary;
}

.intro-content {
  font-size: 26rpx;
  line-height: 1.6;
  color: $text-secondary;
}

/* ── 空状态 ── */
.empty-card {
  background: #fff;
  border-radius: $radius-lg;
  padding: 80rpx 32rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.empty-title {
  font-size: 28rpx;
  font-weight: 600;
  color: $text-primary;
}

.empty-desc {
  font-size: 24rpx;
  color: $text-muted;
}

.btn-goto {
  margin-top: 16rpx;
  padding: 16rpx 48rpx;
  background: $primary-color;
  color: #fff;
  border-radius: $radius-full;
  font-size: 26rpx;
  border: none;
}

/* ── 菜单卡片 ── */
.menu-card {
  background: #fff;
  border-radius: $radius-lg;
  overflow: hidden;
  margin-bottom: 24rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 28rpx 32rpx;
}

.menu-left {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.menu-icon {
  width: 64rpx;
  height: 64rpx;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.menu-title {
  font-size: 28rpx;
  color: $text-primary;
  font-weight: 500;
}

.menu-divider {
  height: 1rpx;
  background: #f0f0f0;
  margin: 0 32rpx;
}

/* ── 评价记录 ── */
.reviews-card {
  background: #fff;
  border-radius: $radius-lg;
  padding: 32rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.card-title {
  font-size: 30rpx;
  font-weight: 600;
  color: $text-primary;
  margin-bottom: 16rpx;
}

.review-item {
  padding: 20rpx 0;
  border-bottom: 1rpx solid #f0f0f0;

  &:last-child {
    border-bottom: none;
  }
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12rpx;
}

.review-date {
  font-size: 22rpx;
  color: $text-muted;
}

.review-content {
  font-size: 26rpx;
  line-height: 1.6;
  color: $text-secondary;
}

/* ── 评价弹窗 ── */
.rate-dialog {
  width: 600rpx;
  background: #fff;
  border-radius: $radius-lg;
  padding: 40rpx;
}

.dialog-title {
  font-size: 32rpx;
  font-weight: 600;
  color: $text-primary;
  text-align: center;
  display: block;
  margin-bottom: 32rpx;
}

.rate-section {
  margin-bottom: 32rpx;
}

.rate-label {
  font-size: 26rpx;
  color: $text-primary;
  font-weight: 500;
  display: block;
  margin-bottom: 16rpx;
}

.dialog-btns {
  display: flex;
  gap: 24rpx;
  margin-top: 40rpx;
}

.btn-cancel {
  flex: 1;
  height: 80rpx;
  line-height: 80rpx;
  border-radius: $radius-full;
  font-size: 28rpx;
  color: $text-secondary;
  background: #f0f0f0;
  border: none;
}

.btn-confirm {
  flex: 1;
  height: 80rpx;
  line-height: 80rpx;
  border-radius: $radius-full;
  font-size: 28rpx;
  font-weight: 600;
  color: #fff;
  background: $primary-color;
  border: none;
}
</style>
