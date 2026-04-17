<template>
  <view class="page-content cert-page">
    <view class="hero-section">
      <text class="text-lg font-bold text-primary">教练认证</text>
      <text class="text-sm text-secondary" style="display:block;margin-top:8rpx;">
        {{ statusDesc }}
      </text>
    </view>

    <view class="card status-card" v-if="profile">
      <view class="status-head">
        <text class="text-base font-semibold text-primary">当前认证信息</text>
        <text class="status-tag" :class="'status-' + profile.status">
          {{ statusText[profile.status] || '未知状态' }}
        </text>
      </view>
      <view class="info-row">
        <text class="label">姓名</text>
        <text class="value">{{ profile.realName || '-' }}</text>
      </view>
      <view class="info-row">
        <text class="label">证书类型</text>
        <text class="value">{{ profile.certificateType || '-' }}</text>
      </view>
      <view class="info-row">
        <text class="label">证书编号</text>
        <text class="value">{{ profile.certificateNo || '-' }}</text>
      </view>
      <view class="info-row">
        <text class="label">擅长方向</text>
        <text class="value">{{ profile.specialties || '-' }}</text>
      </view>
      <view class="info-row">
        <text class="label">个人简介</text>
        <text class="value">{{ profile.introduction || '-' }}</text>
      </view>
      <view class="reject-box" v-if="profile.status === 'rejected' && profile.rejectReason">
        <text class="text-sm">驳回原因：{{ profile.rejectReason }}</text>
      </view>
      <view class="actions" v-if="profile.status === 'rejected'">
        <button class="btn-primary-action" @tap="startEdit">重新提交</button>
      </view>
      <view class="actions approved-actions" v-if="profile.status === 'approved'">
        <button class="btn-primary-action" @tap="goCoachWorkbench">教练工作台</button>
        <button class="btn-secondary-action" @tap="goCoachPlanOptimize">方案优化</button>
      </view>
    </view>

    <view class="card form-card" v-if="showForm">
      <text class="text-base font-semibold text-primary">提交认证申请</text>
      <view class="field">
        <text class="field-label">真实姓名</text>
        <uni-easyinput v-model="form.realName" placeholder="请输入真实姓名" />
      </view>
      <view class="field">
        <text class="field-label">证书类型</text>
        <uni-easyinput v-model="form.certificateType" placeholder="如：国家职业资格健身教练" />
      </view>
      <view class="field">
        <text class="field-label">证书编号</text>
        <uni-easyinput v-model="form.certificateNo" placeholder="请输入证书编号" />
      </view>
      <view class="field">
        <text class="field-label">擅长方向</text>
        <uni-easyinput v-model="form.specialties" placeholder="如：减脂塑形、体态改善" />
      </view>
      <view class="field">
        <text class="field-label">个人简介</text>
        <uni-easyinput
          v-model="form.introduction"
          type="textarea"
          :maxlength="500"
          placeholder="请简要介绍你的从业经验与服务特点"
        />
      </view>
      <button class="btn-primary-action submit-btn" :disabled="submitting" @tap="submit">
        {{ submitting ? '提交中...' : '提交认证' }}
      </button>
    </view>
  </view>
</template>

<script>
import { fitApi } from '@/utils/api.js';

export default {
  data() {
    return {
      profile: null,
      submitting: false,
      forceEdit: false,
      form: {
        realName: '',
        certificateType: '',
        certificateNo: '',
        specialties: '',
        introduction: ''
      },
      statusText: {
        pending: '待审核',
        approved: '已通过',
        rejected: '已驳回'
      }
    };
  },
  computed: {
    showForm() {
      if (!this.profile) return true;
      return this.profile.status === 'rejected' && this.forceEdit;
    },
    statusDesc() {
      if (!this.profile) return '还未提交认证，填写资料后可申请成为平台教练。';
      if (this.profile.status === 'pending') return '认证资料已提交，等待管理员审核。';
      if (this.profile.status === 'approved') return '认证已通过，你可以在教练工作台处理咨询。';
      return '认证未通过，可根据驳回原因修改后重新提交。';
    }
  },
  onShow() {
    this.loadProfile();
  },
  methods: {
    patchForm(profile) {
      this.form = {
        realName: profile?.realName || '',
        certificateType: profile?.certificateType || '',
        certificateNo: profile?.certificateNo || '',
        specialties: profile?.specialties || '',
        introduction: profile?.introduction || ''
      };
    },
    async loadProfile() {
      this.forceEdit = false;
      try {
        const profile = await fitApi.myCoachCertification();
        this.profile = profile || null;
        if (this.profile) {
          this.patchForm(this.profile);
        }
      } catch (error) {
        this.profile = null;
      }
    },
    startEdit() {
      this.forceEdit = true;
    },
    async submit() {
      if (this.submitting) return;
      if (!this.form.realName.trim()) {
        return uni.showToast({ title: '请输入真实姓名', icon: 'none' });
      }
      if (!this.form.certificateType.trim()) {
        return uni.showToast({ title: '请输入证书类型', icon: 'none' });
      }
      if (!this.form.certificateNo.trim()) {
        return uni.showToast({ title: '请输入证书编号', icon: 'none' });
      }
      this.submitting = true;
      try {
        await fitApi.applyCoachCertification({
          realName: this.form.realName.trim(),
          certificateType: this.form.certificateType.trim(),
          certificateNo: this.form.certificateNo.trim(),
          specialties: this.form.specialties.trim(),
          introduction: this.form.introduction.trim()
        });
        uni.showToast({ title: '提交成功', icon: 'success' });
        await this.loadProfile();
      } catch (error) {
        uni.showToast({ title: error.message || '提交失败', icon: 'none' });
      } finally {
        this.submitting = false;
      }
    },
    goCoachWorkbench() {
      uni.navigateTo({ url: '/pages/coach-workbench/index' });
    },
    goCoachPlanOptimize() {
      uni.navigateTo({ url: '/pages/coach-plan-optimize/index' });
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.cert-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.status-card,
.form-card {
  margin-top: 16rpx;
}

.status-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18rpx;
}

.status-tag {
  font-size: 22rpx;
  border-radius: 999rpx;
  padding: 6rpx 16rpx;
}

.status-pending {
  color: #d97706;
  background: #ffedd5;
}

.status-approved {
  color: #047857;
  background: #dcfce7;
}

.status-rejected {
  color: #b91c1c;
  background: #fee2e2;
}

.info-row {
  display: flex;
  align-items: flex-start;
  margin-top: 12rpx;
}

.label {
  width: 150rpx;
  font-size: 24rpx;
  color: $text-muted;
  flex-shrink: 0;
}

.value {
  font-size: 24rpx;
  color: $text-primary;
  line-height: 1.6;
}

.reject-box {
  margin-top: 18rpx;
  border-radius: 10rpx;
  background: #fff1f2;
  color: #be123c;
  padding: 14rpx;
}

.actions {
  margin-top: 20rpx;
}

.approved-actions {
  display: flex;
  gap: 12rpx;
}

.approved-actions .btn-primary-action,
.approved-actions .btn-secondary-action {
  flex: 1;
  width: auto;
}

.field {
  margin-top: 18rpx;
}

.field-label {
  display: block;
  margin-bottom: 8rpx;
  font-size: 24rpx;
  color: $text-primary;
}

.btn-primary-action {
  width: 100%;
  height: 78rpx;
  line-height: 78rpx;
  border-radius: 999rpx;
  border: none;
  color: #fff;
  background: $primary-color;
  font-size: 28rpx;
}

.btn-secondary-action {
  width: 100%;
  height: 78rpx;
  line-height: 78rpx;
  border-radius: 999rpx;
  border: 1rpx solid #c7d2fe;
  color: #1e3a8a;
  background: #eef2ff;
  font-size: 28rpx;
}

.submit-btn {
  margin-top: 26rpx;
}
</style>
