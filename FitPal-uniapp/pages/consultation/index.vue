<template>
  <view class="consultation-page">

    <!-- 咨询列表 -->
    <view class="list-card" v-if="consultations.length">
      <view class="consultation-item" v-for="item in consultations" :key="item.id" @tap="viewDetail(item)">
        <view class="item-header">
          <view class="status-badge" :class="'status-' + item.status">
            {{ statusText[item.status] || '未知' }}
          </view>
          <text class="item-date">{{ item.createTime }}</text>
        </view>
        <text class="item-question">{{ item.question }}</text>
        <text class="item-reply" v-if="item.reply">教练回复：{{ item.reply }}</text>
      </view>
    </view>

    <!-- 空状态 -->
    <view class="empty-card" v-else>
      <uni-icons type="chatbubble" size="48" color="#c0c4cc" />
      <text class="empty-title">还没有咨询记录</text>
      <text class="empty-desc">有问题可随时发起在线咨询</text>
    </view>

    <!-- 发起咨询按钮 -->
    <view class="fab-btn" @tap="showConsultDialog">
      <uni-icons type="plus" size="24" color="#fff" />
    </view>

    <!-- 咨询弹窗 -->
    <uni-popup ref="consultPopup" type="center">
      <view class="consult-dialog">
        <text class="dialog-title">在线咨询</text>

        <view class="consult-section">
          <text class="consult-label">详细描述</text>
          <uni-easyinput
            v-model="consultForm.question"
            type="textarea"
            placeholder="详细说明您遇到的问题或困惑..."
            :maxlength="500"
          />
        </view>

        <view class="dialog-btns">
          <button class="btn-cancel" @tap="closeConsultDialog">取消</button>
          <button class="btn-confirm" @tap="submitConsult">提交</button>
        </view>
      </view>
    </uni-popup>

    <!-- 详情弹窗 -->
    <uni-popup ref="detailPopup" type="center">
      <view class="detail-dialog" v-if="currentItem">
        <text class="dialog-title">咨询详情</text>

        <view class="detail-section">
          <text class="detail-label">问题描述</text>
          <text class="detail-content">{{ currentItem.question }}</text>
        </view>

        <view class="detail-section" v-if="currentItem.reply">
          <text class="detail-label">教练回复</text>
          <text class="detail-content reply-content">{{ currentItem.reply }}</text>
        </view>

        <view class="detail-section" v-else>
          <text class="detail-label">状态</text>
          <text class="detail-content">教练正在处理中，请耐心等待...</text>
        </view>

        <button class="btn-close" @tap="closeDetailDialog">关闭</button>
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
      consultations: [],
      consultForm: {
        question: ''
      },
      currentItem: null,
      statusText: {
        pending: '待回复',
        replied: '已回复',
        closed: '已关闭'
      }
    };
  },
  onShow() {
    if (!ensureRoleAccess(['user', 'admin'])) return;
    this.loadConsultations();
  },
  methods: {
    async loadConsultations() {
      try {
        this.consultations = await fitApi.myConsultations();
      } catch (error) {
        this.consultations = [];
      }
    },
    showConsultDialog() {
      this.$refs.consultPopup.open();
    },
    closeConsultDialog() {
      this.$refs.consultPopup.close();
      this.consultForm = { question: '' };
    },
    async submitConsult() {
      if (!this.consultForm.question.trim()) {
        return uni.showToast({ title: '请详细描述您的问题', icon: 'none' });
      }
      try {
        await fitApi.createConsultation({
          question: this.consultForm.question
        });
        uni.showToast({ title: '提交成功', icon: 'success' });
        this.closeConsultDialog();
        this.loadConsultations();
      } catch (error) {
        uni.showToast({ title: error.message || '提交失败', icon: 'none' });
      }
    },
    viewDetail(item) {
      this.currentItem = item;
      this.$refs.detailPopup.open();
    },
    closeDetailDialog() {
      this.$refs.detailPopup.close();
      this.currentItem = null;
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.consultation-page {
  min-height: 100vh;
  background: #f5f6fa;
  padding: 24rpx;
  padding-bottom: 140rpx;
  box-sizing: border-box;
}

/* ── 列表卡片 ── */
.list-card {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.consultation-item {
  background: #fff;
  border-radius: $radius-lg;
  padding: 28rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.status-badge {
  padding: 6rpx 20rpx;
  border-radius: 20rpx;
  font-size: 22rpx;
  font-weight: 500;

  &.status-pending {
    background: rgba(251, 191, 36, 0.1);
    color: #fbbf24;
  }

  &.status-replied {
    background: rgba(67, 233, 123, 0.1);
    color: #43e97b;
  }

  &.status-closed {
    background: rgba(192, 196, 204, 0.1);
    color: #c0c4cc;
  }
}

.item-date {
  font-size: 22rpx;
  color: $text-muted;
}

.item-question {
  font-size: 28rpx;
  color: $text-primary;
  font-weight: 500;
  line-height: 1.5;
  display: block;
  margin-bottom: 12rpx;
}

.item-reply {
  font-size: 24rpx;
  color: $text-secondary;
  line-height: 1.6;
  display: block;
  padding: 16rpx;
  background: #f8f9fa;
  border-radius: 8rpx;
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

/* ── 悬浮按钮 ── */
.fab-btn {
  position: fixed;
  right: 40rpx;
  bottom: 120rpx;
  width: 100rpx;
  height: 100rpx;
  border-radius: 50rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

/* ── 咨询弹窗 ── */
.consult-dialog {
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

.consult-section {
  margin-bottom: 32rpx;
}

.consult-label {
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

/* ── 详情弹窗 ── */
.detail-dialog {
  width: 600rpx;
  max-height: 80vh;
  background: #fff;
  border-radius: $radius-lg;
  padding: 40rpx;
  overflow-y: auto;
}

.detail-section {
  margin-bottom: 32rpx;
}

.detail-label {
  font-size: 24rpx;
  color: $text-muted;
  display: block;
  margin-bottom: 12rpx;
}

.detail-content {
  font-size: 26rpx;
  color: $text-primary;
  line-height: 1.6;
  display: block;

  &.reply-content {
    padding: 20rpx;
    background: rgba(102, 126, 234, 0.05);
    border-left: 4rpx solid $primary-color;
    border-radius: 8rpx;
  }
}

.btn-close {
  width: 100%;
  height: 80rpx;
  line-height: 80rpx;
  border-radius: $radius-full;
  font-size: 28rpx;
  color: $text-secondary;
  background: #f0f0f0;
  border: none;
  margin-top: 24rpx;
}
</style>
