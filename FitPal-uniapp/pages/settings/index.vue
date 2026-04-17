<template>
  <view class="page-content settings-page">
    <view class="hero-section settings-hero">
      <view>
        <text class="text-lg font-bold text-primary">系统设置</text>
        <text class="text-sm text-secondary hero-desc">管理提醒通知</text>
      </view>
      <image src="/static/icon_fit/shezhi.png" class="hero-icon" mode="aspectFit" />
    </view>

    <view class="card settings-card">
      <view class="card-title-row">
        <text class="text-base font-semibold text-primary">提醒设置</text>
      </view>

      <view class="setting-item">
        <view class="setting-left">
          <view class="setting-icon-wrap">
            <image src="/static/icon_fit/tixing.png" class="setting-icon" mode="aspectFit" />
          </view>
          <view class="setting-info">
            <text class="setting-label">每日打卡提醒</text>
            <text class="setting-desc">提醒记录体重和饮食</text>
          </view>
        </view>
        <switch
          :checked="settings.dailyReminder"
          color="#2f65f9"
          @change="toggle('dailyReminder', $event)"
        />
      </view>
      <view class="divider" />

      <view class="setting-item">
        <view class="setting-left">
          <view class="setting-icon-wrap">
            <image src="/static/icon_fit/rili.png" class="setting-icon" mode="aspectFit" />
          </view>
          <view class="setting-info">
            <text class="setting-label">方案执行提醒</text>
            <text class="setting-desc">提醒完成当日运动计划</text>
          </view>
        </view>
        <switch
          :checked="settings.planReminder"
          color="#2f65f9"
          @change="toggle('planReminder', $event)"
        />
      </view>
      <view class="divider" />

      <view class="setting-item">
        <view class="setting-left">
          <view class="setting-icon-wrap">
            <image src="/static/icon_fit/xiaoxi.png" class="setting-icon" mode="aspectFit" />
          </view>
          <view class="setting-info">
            <text class="setting-label">社区互动提醒</text>
            <text class="setting-desc">点赞和评论消息提醒</text>
          </view>
        </view>
        <switch
          :checked="settings.communityReminder"
          color="#2f65f9"
          @change="toggle('communityReminder', $event)"
        />
      </view>
    </view>

  </view>
</template>

<script>
export default {
  data() {
    return {
      settings: {
        dailyReminder: true,
        planReminder: true,
        communityReminder: true
      }
    };
  },
  onLoad() {
    const settings = uni.getStorageSync('fit_settings');
    if (settings) this.settings = settings;
  },
  methods: {
    toggle(key, event) {
      this.settings = { ...this.settings, [key]: event.detail.value };
      uni.setStorageSync('fit_settings', this.settings);
      uni.showToast({ title: '已保存', icon: 'success' });
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.settings-page {
  min-height: 100vh;
  padding-bottom: 40rpx;
}

.settings-hero {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hero-desc {
  display: block;
  margin-top: 6rpx;
}

.hero-icon {
  width: 56rpx;
  height: 56rpx;
}

.settings-card {
  margin-top: 16rpx;
  padding: 0;
  overflow: hidden;
}

.card-title-row {
  padding: 24rpx 28rpx 14rpx;
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx 28rpx;
}

.setting-left {
  display: flex;
  align-items: center;
  gap: 16rpx;
  flex: 1;
}

.setting-icon-wrap {
  width: 56rpx;
  height: 56rpx;
  border-radius: 14rpx;
  background: #edf3ff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.setting-icon {
  width: 30rpx;
  height: 30rpx;
}

.setting-info {
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.setting-label {
  font-size: 27rpx;
  color: $text-primary;
  font-weight: 500;
}

.setting-desc {
  font-size: 22rpx;
  color: $text-muted;
}

.divider {
  height: 1rpx;
  background: #edf1f7;
  margin: 0 28rpx;
}

</style>
