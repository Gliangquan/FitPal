<template>
  <view class="page-content health-page">
    <view class="hero-section summary-card" v-if="summary">
      <text class="text-lg font-bold text-primary">健康数据记录</text>
      <view class="summary-grid">
        <view class="summary-item">
          <text class="text-sm text-muted">记录天数</text>
          <text class="summary-value">{{ summary.recordCount || 0 }}</text>
        </view>
        <view class="summary-item">
          <text class="text-sm text-muted">起始体重(kg)</text>
          <text class="summary-value">{{ summary.startWeight || '-' }}</text>
        </view>
        <view class="summary-item">
          <text class="text-sm text-muted">当前体重(kg)</text>
          <text class="summary-value">{{ summary.endWeight || '-' }}</text>
        </view>
        <view class="summary-item">
          <text class="text-sm text-muted">体重变化(kg)</text>
          <text class="summary-value" :class="{ 'value-down': Number(summary.weightDelta) < 0 }">{{ summary.weightDelta || '-' }}</text>
        </view>
      </view>
    </view>

    <view class="card chart-card">
      <view class="chart-header">
        <text class="section-title" style="padding: 0;">体重趋势图</text>
        <view class="chart-switch">
          <text
            class="switch-item"
            :class="{ active: trendDays === 7 }"
            @tap="setTrendDays(7)"
          >
            7天
          </text>
          <text
            class="switch-item"
            :class="{ active: trendDays === 30 }"
            @tap="setTrendDays(30)"
          >
            30天
          </text>
        </view>
      </view>
      <view id="trendCanvasWrap" class="trend-canvas-wrap">
        <canvas canvas-id="weightTrendCanvas" id="weightTrendCanvas" class="trend-canvas" />
      </view>
      <text class="text-sm text-muted" v-if="trendRecords.length">
        最低 {{ trendMin }} kg，最高 {{ trendMax }} kg
      </text>
    </view>

    <view class="card form-card">
      <text class="section-title">今日记录</text>

      <view class="form-item">
        <text class="form-label"><text class="required">*</text>体重</text>
        <uni-easyinput v-model="form.weightKg" type="digit" placeholder="如 68.5" :clearable="true" class="form-input">
          <template v-slot:right>
            <text class="input-unit">kg</text>
          </template>
        </uni-easyinput>
      </view>
      <view class="divider" />

      <view class="form-item">
        <text class="form-label">身高</text>
        <uni-easyinput v-model="form.heightCm" type="digit" placeholder="如 168" :clearable="true" class="form-input">
          <template v-slot:right>
            <text class="input-unit">cm</text>
          </template>
        </uni-easyinput>
      </view>
      <view class="divider" />

      <view class="form-item">
        <text class="form-label">性别</text>
        <view class="form-input"><uni-data-checkbox v-model="form.gender" :localdata="genderOptions" /></view>
      </view>
      <view class="divider" />

      <view class="form-item">
        <text class="form-label">年龄</text>
        <uni-easyinput v-model="form.age" type="number" placeholder="如 28" :clearable="true" class="form-input">
          <template v-slot:right>
            <text class="input-unit">岁</text>
          </template>
        </uni-easyinput>
      </view>
      <view class="divider" />

      <view class="form-item">
        <text class="form-label">睡眠</text>
        <uni-easyinput v-model="form.sleepHours" type="digit" placeholder="如 7.5" :clearable="true" class="form-input">
          <template v-slot:right>
            <text class="input-unit">小时</text>
          </template>
        </uni-easyinput>
      </view>
      <view class="divider" />

      <view class="form-item form-item--top">
        <text class="form-label">备注</text>
        <uni-easyinput v-model="form.note" type="textarea" placeholder="今天状态如何..." :maxlength="120" class="form-input" />
      </view>

      <button class="btn-save" @tap="submitRecord">保存今日记录</button>
    </view>

    <view class="card records-card">
      <text class="section-title">最近记录</text>
      <view v-if="records.length" class="records-list">
        <view class="record-item" v-for="item in records" :key="item.id">
          <view>
            <text class="record-date">{{ item.recordDate }}</text>
          </view>
          <view class="record-data">
            <text class="record-weight">{{ item.weightKg }} kg</text>
            <text class="record-fat" v-if="item.bodyFatRate">{{ item.bodyFatRate }}%</text>
          </view>
        </view>
      </view>
      <view v-else class="empty-tip">
        <uni-icons type="info" size="32" color="#94a3b8" />
        <text class="text-sm text-muted">还没有记录，先填写一条数据吧</text>
      </view>
    </view>
  </view>
</template>

<script>
import { fitApi } from '@/utils/api.js';

export default {
  data() {
    return {
      summary: null,
      records: [],
      trendDays: 30,
      trendRecords: [],
      trendMin: '-',
      trendMax: '-',
      genderOptions: [
        { text: '男', value: 'male' },
        { text: '女', value: 'female' }
      ],
      form: {
        weightKg: '',
        heightCm: '',
        gender: 'male',
        age: '',
        sleepHours: '',
        note: ''
      }
    };
  },
  onShow() {
    this.loadReport();
  },
  methods: {
    async loadReport() {
      try {
        const report = await fitApi.getHealthReport(30);
        this.records = report.records || [];
        this.summary = report.summary || null;
        this.$nextTick(() => {
          this.drawTrendChart();
        });
      } catch (error) {
        this.records = [];
        this.summary = null;
        this.$nextTick(() => {
          this.drawTrendChart();
        });
        uni.showToast({ title: error.message || '加载失败', icon: 'none' });
      }
    },
    setTrendDays(days) {
      this.trendDays = days;
      this.$nextTick(() => {
        this.drawTrendChart();
      });
    },
    getTrendRecords() {
      const sorted = (this.records || [])
        .filter((item) => item && item.weightKg !== null && item.weightKg !== undefined)
        .map((item) => ({
          ...item,
          _weight: Number(item.weightKg)
        }))
        .filter((item) => !Number.isNaN(item._weight))
        .sort((a, b) => String(a.recordDate).localeCompare(String(b.recordDate)));
      const limit = Math.max(1, this.trendDays);
      return sorted.slice(-limit);
    },
    getCanvasSize() {
      return new Promise((resolve) => {
        const query = uni.createSelectorQuery().in(this);
        query.select('#trendCanvasWrap').boundingClientRect((rect) => resolve(rect)).exec();
      });
    },
    async drawTrendChart() {
      const data = this.getTrendRecords();
      this.trendRecords = data;
      if (!data.length) {
        this.trendMin = '-';
        this.trendMax = '-';
      } else {
        const values = data.map((item) => item._weight);
        this.trendMin = Math.min(...values).toFixed(1);
        this.trendMax = Math.max(...values).toFixed(1);
      }

      const rect = await this.getCanvasSize();
      if (!rect || !rect.width) {
        return;
      }

      const width = rect.width;
      const height = rect.height || 220;
      const left = 34;
      const right = 14;
      const top = 16;
      const bottom = 30;
      const drawWidth = width - left - right;
      const drawHeight = height - top - bottom;
      const ctx = uni.createCanvasContext('weightTrendCanvas', this);
      ctx.clearRect(0, 0, width, height);

      ctx.setStrokeStyle('#e7edf7');
      ctx.setLineWidth(1);
      ctx.beginPath();
      ctx.moveTo(left, top);
      ctx.lineTo(left, top + drawHeight);
      ctx.lineTo(left + drawWidth, top + drawHeight);
      ctx.stroke();

      if (!data.length) {
        ctx.setFillStyle('#94a3b8');
        ctx.setFontSize(12);
        ctx.fillText('暂无体重数据', left + 8, top + drawHeight / 2);
        ctx.draw();
        return;
      }

      const values = data.map((item) => item._weight);
      let min = Math.min(...values);
      let max = Math.max(...values);
      if (min === max) {
        min = min - 1;
        max = max + 1;
      }
      const gap = max - min;
      const count = data.length;

      const points = data.map((item, index) => {
        const x = left + (count === 1 ? drawWidth / 2 : (drawWidth * index) / (count - 1));
        const y = top + ((max - item._weight) / gap) * drawHeight;
        return { x, y, item };
      });

      ctx.setStrokeStyle('#2f65f9');
      ctx.setLineWidth(2);
      ctx.beginPath();
      points.forEach((point, idx) => {
        if (idx === 0) {
          ctx.moveTo(point.x, point.y);
        } else {
          ctx.lineTo(point.x, point.y);
        }
      });
      ctx.stroke();

      ctx.setFillStyle('#2f65f9');
      points.forEach((point) => {
        ctx.beginPath();
        ctx.arc(point.x, point.y, 3, 0, Math.PI * 2);
        ctx.fill();
      });

      ctx.setFillStyle('#64748b');
      ctx.setFontSize(10);
      const firstDate = String(points[0].item.recordDate || '').slice(5);
      const lastDate = String(points[points.length - 1].item.recordDate || '').slice(5);
      ctx.fillText(firstDate || '', left, top + drawHeight + 18);
      if (points.length > 1) {
        ctx.fillText(lastDate || '', left + drawWidth - 28, top + drawHeight + 18);
      }
      ctx.setFillStyle('#0f172a');
      ctx.fillText(`${max.toFixed(1)}kg`, left + 4, top + 10);
      ctx.fillText(`${min.toFixed(1)}kg`, left + 4, top + drawHeight - 4);
      ctx.draw();
    },
    async submitRecord() {
      if (!this.form.weightKg) {
        return uni.showToast({ title: '请输入体重', icon: 'none' });
      }
      try {
        await fitApi.addHealthRecord({
          weightKg: Number(this.form.weightKg),
          bodyFatRate: this.form.heightCm ? Number(this.form.heightCm) : undefined,
          calorieIntake: this.form.gender === 'female' ? 2 : this.form.gender === 'male' ? 1 : undefined,
          calorieBurn: this.form.age ? Number(this.form.age) : undefined,
          sleepHours: this.form.sleepHours ? Number(this.form.sleepHours) : undefined,
          note: this.form.note
        });
        uni.showToast({ title: '记录成功', icon: 'success' });
        this.form = {
          weightKg: '',
          heightCm: '',
          gender: 'male',
          age: '',
          sleepHours: '',
          note: ''
        };
        this.loadReport();
      } catch (error) {
        uni.showToast({ title: error.message || '记录失败', icon: 'none' });
      }
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.health-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.summary-card {
  margin-bottom: 16rpx;
}

.chart-card {
  margin-bottom: 16rpx;
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12rpx;
}

.chart-switch {
  display: flex;
  background: #f1f5f9;
  border-radius: 999rpx;
  padding: 4rpx;
  gap: 6rpx;
}

.switch-item {
  padding: 6rpx 16rpx;
  font-size: 22rpx;
  color: #64748b;
  border-radius: 999rpx;
}

.switch-item.active {
  background: #2f65f9;
  color: #ffffff;
}

.trend-canvas-wrap {
  width: 100%;
  height: 420rpx;
}

.trend-canvas {
  width: 100%;
  height: 420rpx;
}

.summary-grid {
  margin-top: 14rpx;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10rpx;
}

.summary-item {
  background: #f6f9ff;
  border-radius: 12rpx;
  padding: 12rpx;
}

.summary-value {
  display: block;
  margin-top: 6rpx;
  font-size: 32rpx;
  font-weight: 700;
  color: $primary-color;
}

.value-down {
  color: #16a34a;
}

.form-card {
  padding: 0;
  overflow: hidden;
  margin-bottom: 16rpx;
}

.section-title {
  display: block;
  font-size: 30rpx;
  font-weight: 600;
  color: $text-primary;
  padding: 22rpx 24rpx 16rpx;
}

.form-item {
  display: flex;
  align-items: center;
  padding: 0 24rpx;
  min-height: 94rpx;

  &--top {
    align-items: flex-start;
    padding-top: 20rpx;
    padding-bottom: 20rpx;
  }
}

.form-label {
  width: 140rpx;
  flex-shrink: 0;
  font-size: 27rpx;
  color: $text-primary;
  font-weight: 500;

  .required {
    color: #ef4444;
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

  :deep(.uni-data-checklist) {
    padding: 0 !important;
  }
}

.input-unit {
  font-size: 24rpx;
  color: $text-muted;
  margin-left: 8rpx;
}

.divider {
  height: 1rpx;
  background: #edf1f7;
  margin: 0 24rpx;
}

.btn-save {
  width: calc(100% - 48rpx);
  height: 82rpx;
  line-height: 82rpx;
  border-radius: 999rpx;
  font-size: 28rpx;
  font-weight: 600;
  color: #fff;
  background: $primary-color;
  border: none;
  margin: 24rpx;
}

.records-card {
  padding: 0 22rpx 10rpx;
}

.records-list {
  margin-top: 8rpx;
}

.record-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16rpx 2rpx;
  border-bottom: 1rpx solid #edf1f7;

  &:last-child {
    border-bottom: none;
  }
}

.record-date {
  font-size: 25rpx;
  color: $text-secondary;
}

.record-data {
  display: flex;
  gap: 12rpx;
}

.record-weight {
  font-size: 27rpx;
  font-weight: 600;
  color: $primary-color;
}

.record-fat {
  font-size: 24rpx;
  color: $text-muted;
}

.empty-tip {
  text-align: center;
  padding: 42rpx 0;

  .text-sm {
    display: block;
    margin-top: 8rpx;
  }
}
</style>
