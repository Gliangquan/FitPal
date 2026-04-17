<template>
  <view class="page-content">
    <view class="hero-section">
      <view class="flex flex-between items-center" style="margin-bottom: 16rpx;">
        <view>
          <text class="text-lg font-bold text-primary">轻体云管家</text>
          <text class="text-sm text-secondary" style="display: block; margin-top: 6rpx;">{{ greeting }}</text>
        </view>
        <view class="header-actions">
          <button class="calendar-btn" type="primary" @tap="goCheckinCalendar">打卡日历</button>
        </view>
      </view>
      <text class="text-sm text-muted" style="display:block;">已连续记录健康趋势，目标是更科学地减脂。</text>
    </view>

    <view class="card" style="margin-bottom: 16rpx;">
      <view class="flex flex-between items-center">
        <text class="text-base font-semibold text-primary">数据总览（近30天）</text>
        <text class="text-sm text-theme" @tap="goFitHealth">查看详情</text>
      </view>
      <view class="flex gap-sm" style="margin-top: 12rpx;">
        <view style="flex:1;background:#f6f9ff;border-radius:14rpx;padding:14rpx;">
          <text class="text-sm text-muted">记录天数</text>
          <text class="text-base font-bold text-primary" style="display:block;margin-top:6rpx;">{{ dashboard.recordCount }}</text>
        </view>
        <view style="flex:1;background:#f6f9ff;border-radius:14rpx;padding:14rpx;">
          <text class="text-sm text-muted">当前体重</text>
          <text class="text-base font-bold text-primary" style="display:block;margin-top:6rpx;">{{ dashboard.endWeight }}</text>
        </view>
        <view style="flex:1;background:#f6f9ff;border-radius:14rpx;padding:14rpx;">
          <text class="text-sm text-muted">体重变化</text>
          <text class="text-base font-bold" :class="dashboard.deltaClass" style="display:block;margin-top:6rpx;">{{ dashboard.weightDelta }}</text>
        </view>
      </view>
    </view>

    <uni-section title="快捷功能" class="section">
      <uni-grid :column="3" :showBorder="false" :square="false">
        <uni-grid-item v-for="item in quickActions" :key="item.title">
          <view style="display:flex;flex-direction:column;align-items:center;padding:20rpx;" @tap="item.action">
            <image :src="item.icon" class="quick-action-icon" mode="aspectFit" />
            <text class="text-sm text-secondary" style="margin-top:8rpx;">{{ item.title }}</text>
          </view>
        </uni-grid-item>
      </uni-grid>
    </uni-section>

    <view class="card section" v-if="latestPlan" style="margin-top: 20rpx;">
      <view class="flex flex-between items-center">
        <text class="text-base font-semibold text-primary">最新个性化方案</text>
        <text class="text-sm text-theme" @tap="goFitPlan">进入方案</text>
      </view>
      <view style="margin-top: 10rpx;">
        <text class="text-sm text-muted">BMR：{{ latestPlan.bmr || '-' }} kcal</text>
        <text class="text-sm text-muted" style="display:block;margin-top:6rpx;">日目标热量：{{ latestPlan.dailyCalorieTarget || '-' }} kcal</text>
        <text class="text-sm text-secondary" style="display:block;margin-top:10rpx;">{{ latestPlan.dietSuggestion || '暂无饮食建议' }}</text>
      </view>
    </view>

    <view class="card section" style="margin-top: 20rpx;">
      <view class="flex flex-between items-center">
        <text class="text-base font-semibold text-primary">节气专题</text>
        <text class="text-sm text-theme" @tap="goFitPlan">查看全部</text>
      </view>
      <view v-if="seasonTopic" style="margin-top: 10rpx;">
        <text class="text-base font-semibold text-primary">{{ seasonTopic.title }}</text>
        <text class="text-sm text-secondary" style="display:block;margin-top:8rpx;">{{ seasonTopic.routineAdvice || seasonTopic.recipeText || '结合当前节气调整饮食与作息。' }}</text>
      </view>
      <text v-else class="text-sm text-muted" style="margin-top:10rpx;display:block;">暂无节气专题</text>
    </view>

    <view class="card section" style="margin-top: 20rpx;">
      <view class="flex flex-between items-center">
        <text class="text-base font-semibold text-primary">轻体社区</text>
        <text class="text-sm text-theme" @tap="goFitCommunity">进入社区</text>
      </view>
      <view v-if="communityPosts.length" style="margin-top: 10rpx;">
        <view v-for="item in communityPosts" :key="item.id" class="post-item">
          <text class="text-sm font-semibold text-primary">{{ item.title }}</text>
          <text class="text-sm text-secondary" style="display:block;margin-top:4rpx;">{{ item.content }}</text>
        </view>
      </view>
      <text v-else class="text-sm text-muted" style="margin-top:10rpx;display:block;">社区暂时还没有动态</text>
    </view>
  </view>
</template>

<script>
import { fitApi, userApi } from '@/utils/api.js';

export default {
  data() {
    return {
      userInfo: null,
      dashboard: {
        recordCount: 0,
        endWeight: '-',
        weightDelta: '-',
        deltaClass: 'text-theme'
      },
      latestPlan: null,
      seasonTopic: null,
      communityPosts: [],
      quickActions: [
        { title: '健康记录', icon: '/static/icon_fit/zhenduanjilu.png', action: () => this.goFitHealth() },
        { title: '减脂问卷', icon: '/static/icon_fit/xunwen.png', action: () => this.goFitQuestionnaire() },
        { title: '个性化方案', icon: '/static/icon_fit/geixnghua.png', action: () => this.goFitPlan() },
        { title: '轻体社区', icon: '/static/icon_fit/xiaoxi.png', action: () => this.goFitCommunity() },
        { title: '任务勋章', icon: '/static/icon_fit/jiangbei.png', action: () => this.goTaskBadges() },
        { title: '付费会员', icon: '/static/icon_fit/youhuika.png', action: () => this.goMembership() }
      ]
    };
  },
  computed: {
    greeting() {
      const name = this.userInfo?.userName || '轻体用户';
      return `你好，${name}，今天也要稳步向目标前进`;
    }
  },
  async onShow() {
    await this.ensureLogin();
    await this.loadDashboard();
  },
  methods: {
    async ensureLogin() {
      const localUser = uni.getStorageSync('userInfo');
      if (!localUser?.id) {
        uni.reLaunch({ url: '/pages/login/index' });
        return;
      }
      this.userInfo = localUser;
      try {
        const fresh = await userApi.fetchCurrentUser();
        if (fresh) {
          this.userInfo = fresh;
          uni.setStorageSync('userInfo', fresh);
        }
      } catch (error) {
        console.warn('获取用户信息失败', error);
      }
    },
    async loadDashboard() {
      try {
        const report = await fitApi.getHealthReport(30);
        const s = report?.summary || {};
        const delta = Number(s.weightDelta || 0);
        this.dashboard = {
          recordCount: s.recordCount || 0,
          endWeight: s.endWeight ? `${s.endWeight} kg` : '-',
          weightDelta: s.weightDelta !== undefined ? `${s.weightDelta} kg` : '-',
          deltaClass: delta <= 0 ? 'text-theme' : 'text-secondary'
        };
      } catch (error) {
        this.dashboard = { recordCount: 0, endWeight: '-', weightDelta: '-', deltaClass: 'text-theme' };
      }

      try {
        this.latestPlan = await fitApi.getLatestPlan();
      } catch (error) {
        this.latestPlan = null;
      }

      try {
        const topic = await fitApi.getCurrentSeasonTopic();
        this.seasonTopic = Array.isArray(topic) ? (topic[0] || null) : topic;
      } catch (error) {
        this.seasonTopic = null;
      }

      try {
        const page = await fitApi.listCommunityPosts({ current: 1, size: 3 });
        this.communityPosts = page?.records || [];
      } catch (error) {
        this.communityPosts = [];
      }
    },
    async checkin() {
      try {
        await fitApi.checkin();
        uni.showToast({ title: '打卡成功', icon: 'success' });
      } catch (error) {
        uni.showToast({ title: error.message || '打卡失败', icon: 'none' });
      }
    },
    goCheckinCalendar() {
      uni.navigateTo({ url: '/pages/checkin-calendar/index' });
    },
    goFitHealth() {
      uni.navigateTo({ url: '/pages/fit/health' });
    },
    goFitQuestionnaire() {
      uni.navigateTo({ url: '/pages/fit/questionnaire' });
    },
    goFitPlan() {
      uni.navigateTo({ url: '/pages/fit/plan' });
    },
    goFitCommunity() {
      uni.switchTab({ url: '/pages/fit/community' });
    },
    goProfile() {
      uni.switchTab({ url: '/pages/profile/index' });
    },
    goTaskBadges() {
      uni.navigateTo({ url: '/pages/points-badges/index' });
    },
    goMembership() {
      uni.navigateTo({ url: '/pages/membership/index' });
    },
    goSettings() {
      uni.navigateTo({ url: '/pages/settings/index' });
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.post-item {
  padding: 12rpx 0;
  border-bottom: 1rpx solid #edf1f7;
}

.quick-action-icon {
  width: 56rpx;
  height: 56rpx;
}

.header-actions {
  display: flex;
  gap: 10rpx;
}
</style>
