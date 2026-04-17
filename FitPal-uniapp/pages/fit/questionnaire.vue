<template>
  <view class="page-content questionnaire-page">
    <view class="hero-section intro-card">
      <view class="intro-icon">
        <uni-icons type="compose" size="24" color="#2f65f9" />
      </view>
      <view class="intro-content">
        <text class="text-lg font-bold text-primary">减脂问卷</text>
        <text class="text-sm text-secondary" style="display:block;margin-top:6rpx;">用于生成个性化方案，请尽量如实填写</text>
      </view>
    </view>

    <view class="card form-card">
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
        <text class="form-label">性别</text>
        <view class="form-input"><uni-data-checkbox v-model="form.gender" :localdata="genderOptions" /></view>
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
        <text class="form-label"><text class="required">*</text>当前体重</text>
        <uni-easyinput v-model="form.currentWeightKg" type="digit" placeholder="如 68" :clearable="true" class="form-input">
          <template v-slot:right>
            <text class="input-unit">kg</text>
          </template>
        </uni-easyinput>
      </view>
      <view class="divider" />

      <view class="form-item">
        <text class="form-label"><text class="required">*</text>目标体重</text>
        <uni-easyinput v-model="form.targetWeightKg" type="digit" placeholder="如 60" :clearable="true" class="form-input">
          <template v-slot:right>
            <text class="input-unit">kg</text>
          </template>
        </uni-easyinput>
      </view>
      <view class="divider" />

      <view class="form-item">
        <text class="form-label">目标周期</text>
        <uni-easyinput v-model="form.goalCycleDays" type="number" placeholder="如 90" :clearable="true" class="form-input">
          <template v-slot:right>
            <text class="input-unit">天</text>
          </template>
        </uni-easyinput>
      </view>
      <view class="divider" />

      <view class="form-item">
        <text class="form-label">饮食偏好</text>
        <uni-easyinput v-model="form.dietPreference" placeholder="如 高蛋白/低碳" :clearable="true" class="form-input" />
      </view>
      <view class="divider" />

      <view class="form-item">
        <text class="form-label">运动偏好</text>
        <uni-easyinput v-model="form.sportPreference" placeholder="如 慢跑/瑜伽/力量" :clearable="true" class="form-input" />
      </view>
      <view class="divider" />

      <view class="form-item">
        <text class="form-label">运动强度</text>
        <view class="form-input"><uni-data-checkbox v-model="form.intensity" :localdata="intensityOptions" /></view>
      </view>
      <view class="divider" />

      <view class="form-item form-item--top">
        <text class="form-label">健康状况</text>
        <uni-easyinput v-model="form.healthCondition" type="textarea" placeholder="如有慢性病史请填写" :maxlength="200" class="form-input" />
      </view>

      <button class="btn-save" @tap="submitQuestionnaire">保存问卷并生成方案</button>
    </view>
  </view>
</template>

<script>
import { fitApi } from '@/utils/api.js';

export default {
  data() {
    return {
      genderOptions: [
        { text: '男', value: 'male' },
        { text: '女', value: 'female' }
      ],
      intensityOptions: [
        { text: '低', value: 'low' },
        { text: '中', value: 'medium' },
        { text: '高', value: 'high' }
      ],
      form: {
        age: '',
        gender: 'male',
        heightCm: '',
        currentWeightKg: '',
        targetWeightKg: '',
        goalCycleDays: '60',
        dietPreference: '',
        sportPreference: '',
        intensity: 'medium',
        healthCondition: ''
      }
    };
  },
  methods: {
    async submitQuestionnaire() {
      if (!this.form.currentWeightKg || !this.form.targetWeightKg) {
        return uni.showToast({ title: '请填写当前/目标体重', icon: 'none' });
      }
      try {
        const questionnaireResult = await fitApi.submitQuestionnaire({
          age: this.form.age ? Number(this.form.age) : undefined,
          gender: this.form.gender,
          heightCm: this.form.heightCm ? Number(this.form.heightCm) : undefined,
          currentWeightKg: Number(this.form.currentWeightKg),
          targetWeightKg: Number(this.form.targetWeightKg),
          goalCycleDays: this.form.goalCycleDays ? Number(this.form.goalCycleDays) : 60,
          dietPreference: this.form.dietPreference,
          sportPreference: this.form.sportPreference,
          intensity: this.form.intensity,
          healthCondition: this.form.healthCondition
        });
        const badge = questionnaireResult?.badgeAwarded;
        await fitApi.generatePlan();
        uni.showToast({ title: badge ? `获得${badge.badgeName}` : '方案生成成功', icon: 'success' });
        setTimeout(() => {
          uni.navigateTo({ url: badge ? '/pages/points-badges/index' : '/pages/fit/plan' });
        }, 700);
      } catch (error) {
        uni.showToast({ title: error.message || '提交失败', icon: 'none' });
      }
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.questionnaire-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.intro-card {
  margin-bottom: 16rpx;
  display: flex;
  align-items: center;
  gap: 14rpx;
}

.intro-icon {
  width: 56rpx;
  height: 56rpx;
  border-radius: 14rpx;
  background: #e8f0ff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-card {
  padding: 0;
  overflow: hidden;
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
</style>
