<template>
  <view class="page-content password-page">
    <view class="hero-section intro-card">
      <view class="intro-left">
        <image src="/static/icon_fit/yaoxiang.png" class="intro-icon" mode="aspectFit" />
      </view>
      <view class="intro-content">
        <text class="text-lg font-bold text-primary">修改密码</text>
        <text class="text-sm text-secondary intro-desc">当前提供已登录账号的密码维护能力</text>
      </view>
    </view>

    <view class="card form-card">
      <view class="form-item">
        <text class="form-label"><text class="required">*</text>原密码</text>
        <uni-easyinput
          v-model="form.oldPassword"
          type="password"
          placeholder="请输入原密码"
          :clearable="true"
          class="form-input"
        />
      </view>
      <view class="divider" />

      <view class="form-item">
        <text class="form-label"><text class="required">*</text>新密码</text>
        <uni-easyinput
          v-model="form.newPassword"
          type="password"
          placeholder="请输入新密码"
          :clearable="true"
          class="form-input"
        />
      </view>
      <view class="divider" />

      <view class="form-item">
        <text class="form-label"><text class="required">*</text>确认密码</text>
        <uni-easyinput
          v-model="form.confirmPassword"
          type="password"
          placeholder="请再次输入新密码"
          :clearable="true"
          class="form-input"
        />
      </view>

      <view class="tips-box">
        <text class="tips-title">密码建议</text>
        <text class="tips-item">长度至少 8 位，建议包含字母、数字和特殊字符。</text>
      </view>

      <view class="action-row">
        <button class="btn-cancel" @tap="goBack">取消</button>
        <button class="btn-save" @tap="changePassword">确认修改</button>
      </view>
    </view>
  </view>
</template>

<script>
import { userApi } from '@/utils/api.js';

export default {
  data() {
    return {
      form: {
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    };
  },
  methods: {
    goBack() {
      uni.navigateBack();
    },
    async changePassword() {
      if (!this.form.oldPassword) {
        return uni.showToast({ title: '请输入原密码', icon: 'none' });
      }
      if (!this.form.newPassword) {
        return uni.showToast({ title: '请输入新密码', icon: 'none' });
      }
      if (this.form.newPassword.length < 8) {
        return uni.showToast({ title: '密码长度至少 8 位', icon: 'none' });
      }
      if (this.form.newPassword !== this.form.confirmPassword) {
        return uni.showToast({ title: '两次密码不一致', icon: 'none' });
      }

      try {
        await userApi.changePassword({
          oldPassword: this.form.oldPassword,
          newPassword: this.form.newPassword
        });

        uni.showToast({ title: '修改成功，请重新登录', icon: 'success' });
        setTimeout(() => {
          uni.clearStorageSync();
          uni.reLaunch({ url: '/pages/login/index' });
        }, 1500);
      } catch (error) {
        uni.showToast({ title: error.message || '修改失败', icon: 'none' });
      }
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.password-page {
  min-height: 100vh;
  padding-bottom: 60rpx;
  box-sizing: border-box;
}

.intro-card {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.intro-left {
  width: 68rpx;
  height: 68rpx;
  border-radius: 16rpx;
  background: #edf3ff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.intro-icon {
  width: 36rpx;
  height: 36rpx;
}

.intro-content {
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}

.intro-desc {
  display: block;
}

.form-card {
  margin-top: 16rpx;
  padding: 0;
  overflow: hidden;
}

.form-item {
  display: flex;
  align-items: center;
  padding: 0 32rpx;
  min-height: 100rpx;
}

.form-label {
  width: 140rpx;
  flex-shrink: 0;
  font-size: 28rpx;
  color: $text-primary;
  font-weight: 500;

  .required {
    color: #f44;
    margin-right: 4rpx;
  }
}

.form-input {
  flex: 1;
  min-width: 0;

  :deep(.uni-easyinput__content) {
    border: none !important;
    background: transparent !important;
    padding-left: 0 !important;
  }

  :deep(.uni-easyinput) {
    border: none !important;
    background: transparent !important;
  }
}

.divider {
  height: 1rpx;
  background: #f0f0f0;
  margin: 0 32rpx;
}

.tips-box {
  margin: 26rpx 30rpx 8rpx;
  padding: 18rpx 20rpx;
  background: #f6f9ff;
  border: 1rpx solid #e1ebff;
  border-radius: 12rpx;
}

.tips-title {
  font-size: 24rpx;
  font-weight: 600;
  color: #3558a7;
  display: block;
}

.tips-item {
  margin-top: 6rpx;
  font-size: 23rpx;
  color: $text-secondary;
  line-height: 1.6;
}

.action-row {
  display: flex;
  gap: 16rpx;
  margin: 24rpx 30rpx 30rpx;
}

.btn-cancel {
  flex: 1;
  height: 84rpx;
  line-height: 84rpx;
  border-radius: $radius-full;
  font-size: 28rpx;
  color: #64748b;
  background: #f8fafc;
  border: 1rpx solid #e2e8f0;
}

.btn-save {
  flex: 1;
  height: 84rpx;
  line-height: 84rpx;
  border-radius: $radius-full;
  font-size: 28rpx;
  font-weight: 600;
  color: #fff;
  background: $primary-color;
  border: none;
}
</style>
