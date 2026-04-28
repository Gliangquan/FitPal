<template>
  <view class="page-content coach-plan-page">
    <view class="hero-section">
      <text class="text-lg font-bold text-primary">减脂方案优化</text>
      <text class="text-sm text-secondary" style="display:block;margin-top:8rpx;">
        教练可基于系统方案进行二次优化并保存
      </text>
      <view class="filter-line" v-if="queryUserId">
        <text class="text-sm text-theme">当前仅显示用户ID {{ queryUserId }} 的方案</text>
        <text class="text-sm text-muted clear-link" @tap="clearUserFilter">清除筛选</text>
      </view>
    </view>

    <view class="status-tabs">
      <view
        v-for="tab in statusTabs"
        :key="tab.value || 'all'"
        class="tab-item"
        :class="{ active: statusFilter === tab.value }"
        @tap="switchStatus(tab.value)"
      >
        {{ tab.label }}
      </view>
    </view>

    <view class="list-wrap" v-if="plans.length">
      <view class="plan-card" v-for="item in plans" :key="item.id">
        <view class="plan-head">
          <text class="user-name">{{ item.userNickname || ('用户#' + item.userId) }}</text>
          <text class="status-tag" :class="'status-' + item.status">
            {{ item.status === 'coached' ? '已优化' : '系统方案' }}
          </text>
        </view>
        <text class="meta">方案ID：{{ item.id }}  创建时间：{{ formatTime(item.createdAt) }}</text>
        <text class="meta">目标热量：{{ item.targetCalories || '-' }} kcal</text>
        <text class="section-label">饮食建议</text>
        <text class="content">{{ item.dietPlan || '暂无' }}</text>
        <text class="section-label">运动建议</text>
        <text class="content">{{ item.exercisePlan || '暂无' }}</text>
        <text class="section-label">生活建议</text>
        <text class="content">{{ item.lifestyleTips || '暂无' }}</text>
        <button class="btn-opt" @tap="openOptimize(item)">优化并保存</button>
      </view>
    </view>

    <view class="card empty-card" v-else>
      <text class="text-base font-semibold text-primary">暂无方案数据</text>
      <text class="text-sm text-muted" style="margin-top:8rpx;">可先在用户端生成个性化方案。</text>
    </view>

    <view class="load-more" v-if="plans.length && hasMore">
      <button size="mini" type="default" :disabled="loadingMore" @tap="loadMore">
        {{ loadingMore ? '加载中...' : '加载更多' }}
      </button>
    </view>

    <uni-popup ref="editPopup" type="center">
      <view class="edit-dialog" v-if="currentPlan">
        <text class="dialog-title">优化方案</text>
        <text class="dialog-user">用户：{{ currentPlan.userNickname || ('用户#' + currentPlan.userId) }}</text>
        <view class="field">
          <text class="field-label">饮食建议</text>
          <uni-easyinput v-model="form.dietPlan" type="textarea" :maxlength="1200" />
        </view>
        <view class="field">
          <text class="field-label">运动建议</text>
          <uni-easyinput v-model="form.exercisePlan" type="textarea" :maxlength="1200" />
        </view>
        <view class="field">
          <text class="field-label">生活建议</text>
          <uni-easyinput v-model="form.lifestyleTips" type="textarea" :maxlength="1200" />
        </view>
        <view class="field">
          <text class="field-label">教练备注</text>
          <uni-easyinput
            v-model="form.coachNote"
            type="textarea"
            :maxlength="300"
            placeholder="补充个性化执行建议（将追加到生活建议中）"
          />
        </view>
        <view class="dialog-actions">
          <button class="btn-cancel" @tap="closeOptimize">取消</button>
          <button class="btn-confirm" :disabled="saving" @tap="submitOptimize">
            {{ saving ? '保存中...' : '保存优化' }}
          </button>
        </view>
      </view>
    </uni-popup>
  </view>
</template>

<script>
import { fitApi } from '@/utils/api.js';
import { ensureRoleAccess } from '@/utils/permissions.js';

export default {
  data() {
    return {
      statusTabs: [
        { label: '全部', value: '' },
        { label: '系统方案', value: 'system' },
        { label: '已优化', value: 'coached' }
      ],
      statusFilter: '',
      queryUserId: '',
      plans: [],
      current: 1,
      size: 10,
      hasMore: true,
      loadingMore: false,
      currentPlan: null,
      saving: false,
      form: {
        dietPlan: '',
        exercisePlan: '',
        lifestyleTips: '',
        coachNote: ''
      }
    };
  },
  onLoad(options) {
    const userId = Number(options?.userId || 0);
    this.queryUserId = userId > 0 ? userId : '';
  },
  onShow() {
    if (!ensureRoleAccess(['coach', 'admin'])) return;
    this.reload();
  },
  onReachBottom() {
    this.loadMore();
  },
  methods: {
    formatTime(value) {
      if (!value) return '-';
      return String(value).replace('T', ' ').slice(0, 16);
    },
    switchStatus(value) {
      if (this.statusFilter === value) return;
      this.statusFilter = value;
      this.reload();
    },
    clearUserFilter() {
      this.queryUserId = '';
      this.reload();
    },
    async reload() {
      this.current = 1;
      this.hasMore = true;
      this.plans = [];
      await this.loadMore();
    },
    async loadMore() {
      if (!this.hasMore || this.loadingMore) return;
      this.loadingMore = true;
      try {
        const result = await fitApi.listCoachPlans({
          status: this.statusFilter || undefined,
          userId: this.queryUserId || undefined,
          current: this.current,
          size: this.size
        });
        const records = result?.records || [];
        const total = Number(result?.total || 0);
        if (this.current === 1) {
          this.plans = records;
        } else {
          this.plans = this.plans.concat(records);
        }
        this.current += 1;
        this.hasMore = total > 0 ? this.plans.length < total : records.length >= this.size;
      } catch (error) {
        this.hasMore = false;
        uni.showToast({ title: error.message || '加载失败', icon: 'none' });
      } finally {
        this.loadingMore = false;
      }
    },
    openOptimize(item) {
      this.currentPlan = item;
      this.form = {
        dietPlan: item?.dietPlan || '',
        exercisePlan: item?.exercisePlan || '',
        lifestyleTips: item?.lifestyleTips || '',
        coachNote: ''
      };
      this.$refs.editPopup.open();
    },
    closeOptimize() {
      this.$refs.editPopup.close();
      this.currentPlan = null;
      this.form = {
        dietPlan: '',
        exercisePlan: '',
        lifestyleTips: '',
        coachNote: ''
      };
    },
    async submitOptimize() {
      if (!this.currentPlan?.id) return;
      if (this.saving) return;
      this.saving = true;
      try {
        await fitApi.optimizeCoachPlan(this.currentPlan.id, {
          dietPlan: this.form.dietPlan.trim(),
          exercisePlan: this.form.exercisePlan.trim(),
          lifestyleTips: this.form.lifestyleTips.trim(),
          coachNote: this.form.coachNote.trim()
        });
        uni.showToast({ title: '已保存优化方案', icon: 'success' });
        this.closeOptimize();
        await this.reload();
      } catch (error) {
        uni.showToast({ title: error.message || '保存失败', icon: 'none' });
      } finally {
        this.saving = false;
      }
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.coach-plan-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.filter-line {
  margin-top: 12rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.clear-link {
  text-decoration: underline;
}

.status-tabs {
  display: flex;
  gap: 12rpx;
  margin-bottom: 14rpx;
}

.tab-item {
  padding: 10rpx 24rpx;
  border-radius: 999rpx;
  font-size: 24rpx;
  color: #64748b;
  background: #eef2ff;
}

.tab-item.active {
  color: #fff;
  background: $primary-color;
}

.list-wrap {
  display: flex;
  flex-direction: column;
  gap: 14rpx;
}

.plan-card {
  background: #fff;
  border-radius: 18rpx;
  padding: 22rpx;
  box-shadow: 0 6rpx 20rpx rgba(0, 0, 0, 0.06);
}

.plan-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.user-name {
  font-size: 28rpx;
  color: $text-primary;
  font-weight: 600;
}

.status-tag {
  border-radius: 999rpx;
  font-size: 22rpx;
  padding: 6rpx 16rpx;
}

.status-system {
  color: #1d4ed8;
  background: #dbeafe;
}

.status-coached {
  color: #047857;
  background: #dcfce7;
}

.meta {
  margin-top: 8rpx;
  display: block;
  font-size: 22rpx;
  color: $text-muted;
}

.section-label {
  margin-top: 12rpx;
  display: block;
  font-size: 24rpx;
  color: #334155;
  font-weight: 500;
}

.content {
  margin-top: 6rpx;
  display: block;
  font-size: 24rpx;
  line-height: 1.6;
  color: $text-secondary;
}

.btn-opt {
  margin-top: 14rpx;
  width: 200rpx;
  height: 64rpx;
  line-height: 64rpx;
  border-radius: 999rpx;
  border: none;
  color: #fff;
  background: $primary-color;
  font-size: 24rpx;
}

.empty-card {
  margin-top: 16rpx;
  text-align: center;
}

.load-more {
  margin-top: 12rpx;
  text-align: center;
}

.edit-dialog {
  width: 640rpx;
  max-height: 85vh;
  overflow-y: auto;
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
}

.dialog-title {
  display: block;
  text-align: center;
  font-size: 30rpx;
  color: $text-primary;
  font-weight: 600;
}

.dialog-user {
  margin-top: 10rpx;
  display: block;
  text-align: center;
  font-size: 23rpx;
  color: $text-muted;
}

.field {
  margin-top: 16rpx;
}

.field-label {
  display: block;
  margin-bottom: 8rpx;
  font-size: 23rpx;
  color: #334155;
}

.dialog-actions {
  display: flex;
  gap: 16rpx;
  margin-top: 22rpx;
}

.btn-cancel,
.btn-confirm {
  flex: 1;
  height: 74rpx;
  line-height: 74rpx;
  border-radius: 999rpx;
  border: none;
  font-size: 26rpx;
}

.btn-cancel {
  color: $text-secondary;
  background: #f1f5f9;
}

.btn-confirm {
  color: #fff;
  background: $primary-color;
}
</style>
