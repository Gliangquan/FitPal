<template>
  <view class="page-content profile-page">
    <view class="hero-section user-card" @tap="goEdit">
      <view class="user-info">
        <view class="avatar-wrap">
          <image
            v-if="user.userAvatar"
            :src="normalizeImageUrl(user.userAvatar)"
            mode="aspectFill"
            class="avatar-img"
          />
          <view v-else class="avatar-fallback">
            <text class="avatar-text">{{ user.userName ? user.userName.slice(0, 1) : '我' }}</text>
          </view>
        </view>
        <view class="user-detail">
          <text class="text-lg font-semibold text-primary">{{ user.userName || '未设置昵称' }}</text>
          <text class="text-sm text-secondary">{{ user.userAccount || '未登录' }}</text>
          <view class="user-chip-row">
            <view class="point-chip">
              <text class="text-sm text-theme">当前积分：{{ points }}</text>
            </view>
            <view class="badge-chip">
              <text class="text-sm badge-chip-text">任务勋章：{{ taskBadgeCount }}</text>
            </view>
          </view>
        </view>
      </view>
      <uni-icons type="forward" size="18" color="#94a3b8" />
    </view>

    <view class="card menu-card">
      <view class="menu-item" @tap="goMyCoach">
        <view class="menu-left">
          <view class="menu-icon"><image class="menu-icon-img" src="/static/icon_fit/yisheng.png" mode="aspectFit" /></view>
          <text class="menu-title">我的教练</text>
        </view>
        <uni-icons type="forward" size="16" color="#94a3b8" />
      </view>
      <view class="menu-divider" />

      <view class="menu-item" v-if="user.userRole === 'coach'" @tap="goCoachCertification">
        <view class="menu-left">
          <view class="menu-icon"><image class="menu-icon-img" src="/static/icon_fit/xianhua.png" mode="aspectFit" /></view>
          <text class="menu-title">教练资质</text>
        </view>
        <uni-icons type="forward" size="16" color="#94a3b8" />
      </view>
      <view class="menu-divider" v-if="user.userRole === 'coach'" />

      <view class="menu-item" v-if="user.userRole === 'coach'" @tap="goCoachWorkbench">
        <view class="menu-left">
          <view class="menu-icon"><image class="menu-icon-img" src="/static/icon_fit/redu.png" mode="aspectFit" /></view>
          <text class="menu-title">教练工作台</text>
        </view>
        <uni-icons type="forward" size="16" color="#94a3b8" />
      </view>
      <view class="menu-divider" v-if="user.userRole === 'coach'" />

      <view class="menu-item" v-if="user.userRole === 'coach'" @tap="goCoachPlanOptimize">
        <view class="menu-left">
          <view class="menu-icon"><image class="menu-icon-img" src="/static/icon_fit/geixnghua.png" mode="aspectFit" /></view>
          <text class="menu-title">方案优化</text>
        </view>
        <uni-icons type="forward" size="16" color="#94a3b8" />
      </view>
      <view class="menu-divider" v-if="user.userRole === 'coach'" />

      <view class="menu-item" @tap="goHealth">
        <view class="menu-left">
          <view class="menu-icon"><image class="menu-icon-img" src="/static/icon_fit/zhenduanjilu.png" mode="aspectFit" /></view>
          <text class="menu-title">健康记录</text>
        </view>
        <uni-icons type="forward" size="16" color="#94a3b8" />
      </view>
      <view class="menu-divider" />

      <view class="menu-item" @tap="goQuestionnaire">
        <view class="menu-left">
          <view class="menu-icon"><image class="menu-icon-img" src="/static/icon_fit/xunwen.png" mode="aspectFit" /></view>
          <text class="menu-title">减脂问卷</text>
        </view>
        <uni-icons type="forward" size="16" color="#94a3b8" />
      </view>
      <view class="menu-divider" />

      <view class="menu-item" @tap="goPlan">
        <view class="menu-left">
          <view class="menu-icon"><image class="menu-icon-img" src="/static/icon_fit/geixnghua.png" mode="aspectFit" /></view>
          <text class="menu-title">个性化方案</text>
        </view>
        <uni-icons type="forward" size="16" color="#94a3b8" />
      </view>
      <view class="menu-divider" />

      <view class="menu-item" @tap="goCommunity">
        <view class="menu-left">
          <view class="menu-icon"><image class="menu-icon-img" src="/static/icon_fit/xiaoxi.png" mode="aspectFit" /></view>
          <text class="menu-title">轻体社区</text>
        </view>
        <uni-icons type="forward" size="16" color="#94a3b8" />
      </view>
      <view class="menu-divider" />

      <view class="menu-item" @tap="goContentRecommend">
        <view class="menu-left">
          <view class="menu-icon"><image class="menu-icon-img" src="/static/icon_fit/redu.png" mode="aspectFit" /></view>
          <text class="menu-title">内容推荐</text>
        </view>
        <uni-icons type="forward" size="16" color="#94a3b8" />
      </view>
      <view class="menu-divider" />

      <view class="menu-item" @tap="goPointBadges">
        <view class="menu-left">
          <view class="menu-icon"><image class="menu-icon-img" src="/static/icon_fit/jiangbei.png" mode="aspectFit" /></view>
          <text class="menu-title">勋章兑换</text>
        </view>
        <uni-icons type="forward" size="16" color="#94a3b8" />
      </view>
    </view>

    <view class="card menu-card">
      <view class="menu-item" @tap="goEdit">
        <view class="menu-left">
          <view class="menu-icon"><image class="menu-icon-img" src="/static/icon_fit/bianji.png" mode="aspectFit" /></view>
          <text class="menu-title">编辑个人信息</text>
        </view>
        <uni-icons type="forward" size="16" color="#94a3b8" />
      </view>
      <view class="menu-divider" />

      <view class="menu-item" @tap="goChangePassword">
        <view class="menu-left">
          <view class="menu-icon"><image class="menu-icon-img" src="/static/icon_fit/yaoxiang.png" mode="aspectFit" /></view>
          <text class="menu-title">修改密码</text>
        </view>
        <uni-icons type="forward" size="16" color="#94a3b8" />
      </view>
      <view class="menu-divider" />

      <view class="menu-item" @tap="goSettings">
        <view class="menu-left">
          <view class="menu-icon"><image class="menu-icon-img" src="/static/icon_fit/shezhi.png" mode="aspectFit" /></view>
          <text class="menu-title">系统设置</text>
        </view>
        <uni-icons type="forward" size="16" color="#94a3b8" />
      </view>
    </view>

    <view class="card logout-card">
      <button class="logout-btn" @tap="logout">退出登录</button>
    </view>
  </view>
</template>

<script>
import { fitApi, userApi } from '@/utils/api.js';
import { resolveFileUrl } from '@/utils/request.js';

export default {
  data() {
    return {
      user: {},
      points: 0,
      taskBadgeCount: 0
    };
  },
  async onShow() {
    await this.loadUser();
    await this.loadPoints();
  },
  methods: {
    normalizeImageUrl(url) {
      return resolveFileUrl(url);
    },
    async loadUser() {
      try {
        const user = await userApi.fetchCurrentUser();
        this.user = user || {};
        if (user) uni.setStorageSync('userInfo', user);
      } catch (error) {
        this.user = uni.getStorageSync('userInfo') || {};
      }
    },
    async loadPoints() {
      try {
        const data = await fitApi.myPoints();
        this.points = data?.account?.availablePoint || 0;
        this.taskBadgeCount = Array.isArray(data?.taskBadges) ? data.taskBadges.length : 0;
      } catch (error) {
        this.points = 0;
        this.taskBadgeCount = 0;
      }
    },
    goHealth() {
      uni.navigateTo({ url: '/pages/fit/health' });
    },
    goMyCoach() {
      uni.navigateTo({ url: '/pages/my-coach/index' });
    },
    goCoachCertification() {
      uni.navigateTo({ url: '/pages/coach-certification/index' });
    },
    goCoachWorkbench() {
      uni.navigateTo({ url: '/pages/coach-workbench/index' });
    },
    goCoachPlanOptimize() {
      uni.navigateTo({ url: '/pages/coach-plan-optimize/index' });
    },
    goQuestionnaire() {
      uni.navigateTo({ url: '/pages/fit/questionnaire' });
    },
    goPlan() {
      uni.navigateTo({ url: '/pages/fit/plan' });
    },
    goCommunity() {
      uni.switchTab({ url: '/pages/fit/community' });
    },
    goContentRecommend() {
      uni.navigateTo({ url: '/pages/content-recommend/index' });
    },
    goPointBadges() {
      uni.navigateTo({ url: '/pages/points-badges/index' });
    },
    goEdit() {
      uni.navigateTo({ url: '/pages/edit-profile/index' });
    },
    goChangePassword() {
      uni.navigateTo({ url: '/pages/change-password/index' });
    },
    goSettings() {
      uni.navigateTo({ url: '/pages/settings/index' });
    },
    async logout() {
      const confirmed = await new Promise((resolve) => {
        uni.showModal({
          title: '退出登录',
          content: '确定要退出登录吗？',
          success: (res) => resolve(res.confirm)
        });
      });
      if (!confirmed) return;
      try {
        await userApi.logout();
      } catch (error) {
        console.warn('退出登录错误', error);
      }
      uni.clearStorageSync();
      uni.reLaunch({ url: '/pages/login/index' });
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.profile-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.user-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16rpx;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.avatar-wrap {
  width: 100rpx;
  height: 100rpx;
  border-radius: 50rpx;
  overflow: hidden;
  background: #e8f0ff;
  border: 2rpx solid #d7e4ff;
}

.avatar-img {
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

.avatar-text {
  font-size: 40rpx;
  font-weight: 700;
  color: $primary-color;
}

.user-detail {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.user-chip-row {
  display: flex;
  align-items: center;
  gap: 10rpx;
  flex-wrap: wrap;
}

.point-chip {
  align-self: flex-start;
  background: #edf3ff;
  border-radius: 999rpx;
  padding: 4rpx 14rpx;
}

.badge-chip {
  align-self: flex-start;
  background: #fff7db;
  border-radius: 999rpx;
  padding: 4rpx 14rpx;
}

.badge-chip-text {
  color: #b7791f;
}

.menu-card {
  margin-bottom: 16rpx;
  padding: 0;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 26rpx 28rpx;
}

.menu-left {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.menu-icon {
  width: 56rpx;
  height: 56rpx;
  border-radius: 14rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #edf3ff;
}

.menu-icon-img {
  width: 32rpx;
  height: 32rpx;
}

.menu-title {
  font-size: 28rpx;
  color: $text-primary;
}

.menu-divider {
  height: 1rpx;
  background: #edf1f7;
  margin: 0 28rpx;
}

.logout-card {
  padding: 20rpx;
}

.logout-btn {
  width: 100%;
  height: 82rpx;
  line-height: 82rpx;
  border-radius: 999rpx;
  font-size: 28rpx;
  font-weight: 500;
  color: #64748b;
  background: #f8fafc;
  border: 1rpx solid #e2e8f0;
}
</style>
