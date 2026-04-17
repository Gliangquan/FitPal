<template>
  <view class="page-content workbench-page">
    <view class="hero-section">
      <view class="flex flex-between items-center">
        <view>
          <text class="text-lg font-bold text-primary">教练工作台</text>
          <text class="text-sm text-secondary" style="display:block;margin-top:8rpx;">
            待回复咨询 {{ todoList.length }} 条
          </text>
        </view>
        <button size="mini" type="default" @tap="loadTodo">刷新</button>
      </view>
    </view>

    <view class="list-card" v-if="todoList.length">
      <view class="item-card" v-for="item in todoList" :key="item.id">
        <view class="item-head">
          <text class="text-sm text-muted">咨询ID：{{ item.id }}</text>
          <text class="text-sm text-muted">{{ formatTime(item.createTime) }}</text>
        </view>
        <text class="question">{{ item.question || '（无内容）' }}</text>
        <view class="item-actions">
          <button class="btn-sub btn-opt" @tap="goOptimize(item)">优化用户方案</button>
          <button class="btn-sub btn-reply" @tap="openReply(item)">回复咨询</button>
        </view>
      </view>
    </view>

    <view class="card empty-card" v-else>
      <text class="text-base font-semibold text-primary">暂无待处理咨询</text>
      <text class="text-sm text-muted" style="margin-top:8rpx;">有新咨询后会显示在这里。</text>
    </view>

    <uni-popup ref="replyPopup" type="center">
      <view class="reply-dialog" v-if="currentItem">
        <text class="dialog-title">回复咨询</text>
        <view class="question-box">
          <text class="text-sm text-muted">用户提问</text>
          <text class="dialog-question">{{ currentItem.question }}</text>
        </view>
        <view class="field">
          <text class="text-sm text-muted">回复内容</text>
          <uni-easyinput
            v-model="replyText"
            type="textarea"
            :maxlength="800"
            placeholder="请输入给用户的建议与回复"
          />
        </view>
        <view class="dialog-actions">
          <button class="btn-cancel" @tap="closeReply">取消</button>
          <button class="btn-confirm" :disabled="replying" @tap="submitReply">
            {{ replying ? '提交中...' : '提交回复' }}
          </button>
        </view>
      </view>
    </uni-popup>
  </view>
</template>

<script>
import { fitApi } from '@/utils/api.js';

export default {
  data() {
    return {
      todoList: [],
      currentItem: null,
      replyText: '',
      replying: false
    };
  },
  onShow() {
    this.loadTodo();
  },
  methods: {
    formatTime(value) {
      if (!value) return '';
      return String(value).replace('T', ' ').slice(0, 16);
    },
    async loadTodo() {
      try {
        this.todoList = await fitApi.coachTodoConsultations();
      } catch (error) {
        this.todoList = [];
        uni.showToast({ title: error.message || '加载失败', icon: 'none' });
      }
    },
    openReply(item) {
      this.currentItem = item;
      this.replyText = '';
      this.$refs.replyPopup.open();
    },
    goOptimize(item) {
      const userId = Number(item?.userId || 0);
      if (!userId) {
        return uni.showToast({ title: '咨询用户信息缺失', icon: 'none' });
      }
      uni.navigateTo({ url: `/pages/coach-plan-optimize/index?userId=${userId}` });
    },
    closeReply() {
      this.$refs.replyPopup.close();
      this.currentItem = null;
      this.replyText = '';
    },
    async submitReply() {
      if (!this.currentItem?.id) return;
      const content = this.replyText.trim();
      if (!content) {
        return uni.showToast({ title: '请输入回复内容', icon: 'none' });
      }
      this.replying = true;
      try {
        await fitApi.coachReplyConsultation(this.currentItem.id, { reply: content });
        uni.showToast({ title: '回复成功', icon: 'success' });
        this.closeReply();
        await this.loadTodo();
      } catch (error) {
        uni.showToast({ title: error.message || '回复失败', icon: 'none' });
      } finally {
        this.replying = false;
      }
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.workbench-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.list-card {
  display: flex;
  flex-direction: column;
  gap: 14rpx;
}

.item-card {
  background: #fff;
  border-radius: 18rpx;
  padding: 22rpx;
  box-shadow: 0 6rpx 20rpx rgba(0, 0, 0, 0.06);
}

.item-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.question {
  display: block;
  margin-top: 12rpx;
  font-size: 26rpx;
  line-height: 1.6;
  color: $text-primary;
}

.item-actions {
  margin-top: 16rpx;
  display: flex;
  gap: 12rpx;
}

.btn-sub {
  flex: 1;
  height: 62rpx;
  line-height: 62rpx;
  border-radius: 999rpx;
  border: none;
  font-size: 24rpx;
}

.btn-opt {
  color: #1e3a8a;
  background: #dbeafe;
}

.btn-reply {
  color: #fff;
  background: $primary-color;
}

.empty-card {
  margin-top: 16rpx;
  text-align: center;
}

.reply-dialog {
  width: 620rpx;
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
}

.dialog-title {
  display: block;
  text-align: center;
  font-size: 30rpx;
  font-weight: 600;
  color: $text-primary;
}

.question-box {
  margin-top: 20rpx;
  padding: 16rpx;
  border-radius: 12rpx;
  background: #f8fafc;
}

.dialog-question {
  display: block;
  margin-top: 8rpx;
  font-size: 25rpx;
  color: $text-primary;
  line-height: 1.6;
}

.field {
  margin-top: 18rpx;
}

.dialog-actions {
  display: flex;
  gap: 16rpx;
  margin-top: 26rpx;
}

.btn-cancel,
.btn-confirm {
  flex: 1;
  height: 74rpx;
  line-height: 74rpx;
  border-radius: 999rpx;
  font-size: 26rpx;
  border: none;
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
