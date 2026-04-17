<template>
  <view class="page-content checkin-page">
    <view class="hero-section">
      <view class="flex flex-between items-center">
        <view>
          <text class="text-lg font-bold text-primary">打卡日历</text>
          <text class="text-sm text-secondary" style="display:block;margin-top:6rpx;">
            {{ currentMonthLabel }} 已打卡 {{ checkinCount }} 天
          </text>
        </view>
        <button size="mini" type="primary" @tap="checkin">今日打卡</button>
      </view>
    </view>

    <view class="card calendar-card">
      <uni-calendar
        :insert="true"
        :selected="selectedDays"
        :date="calendarDate"
        :showMonth="true"
        @monthSwitch="onMonthSwitch"
      />
    </view>

    <view class="card tips-card">
      <text class="text-sm text-muted">
        蓝点日期表示已完成打卡。每次打卡都会累计积分。
      </text>
    </view>
  </view>
</template>

<script>
import { fitApi } from '@/utils/api.js';

const toYearMonth = (date) => {
  const year = date.getFullYear();
  const month = `${date.getMonth() + 1}`.padStart(2, '0');
  return `${year}-${month}`;
};

export default {
  data() {
    const now = new Date();
    return {
      currentMonth: toYearMonth(now),
      calendarDate: `${toYearMonth(now)}-01`,
      selectedDays: [],
      checkinCount: 0
    };
  },
  computed: {
    currentMonthLabel() {
      return this.currentMonth.replace('-', '年') + '月';
    }
  },
  onShow() {
    this.loadCalendar(this.currentMonth);
  },
  methods: {
    async loadCalendar(month) {
      try {
        const data = await fitApi.getCheckinCalendar(month);
        this.currentMonth = data?.month || month;
        this.calendarDate = `${this.currentMonth}-01`;
        this.selectedDays = data?.selected || [];
        this.checkinCount = data?.count || 0;
      } catch (error) {
        this.selectedDays = [];
        this.checkinCount = 0;
        uni.showToast({ title: error.message || '加载失败', icon: 'none' });
      }
    },
    onMonthSwitch(e) {
      const year = Number(e?.year || 0);
      const month = Number(e?.month || 0);
      if (!year || !month) return;
      const monthText = `${year}-${`${month}`.padStart(2, '0')}`;
      this.loadCalendar(monthText);
    },
    async checkin() {
      try {
        const result = await fitApi.checkin();
        const badge = result?.badgeAwarded;
        uni.showToast({ title: badge ? `获得${badge.badgeName}` : '打卡成功', icon: 'success' });
        this.loadCalendar(this.currentMonth);
        if (badge) {
          setTimeout(() => {
            uni.navigateTo({ url: '/pages/points-badges/index' });
          }, 700);
        }
      } catch (error) {
        uni.showToast({ title: error.message || '打卡失败', icon: 'none' });
      }
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.checkin-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.calendar-card {
  padding: 18rpx 12rpx;
}

.tips-card {
  margin-top: 14rpx;
}
</style>
