<template>
  <view class="page-content membership-page">
    <view class="hero-section membership-hero">
      <text class="text-lg font-bold text-primary">付费会员</text>
      <text class="text-sm text-secondary" style="display:block;margin-top:8rpx;">
        当前版本暂未接入真实支付，这里先展示论文描述中的会员权益与后续开通入口。
      </text>
    </view>

    <view class="card membership-card">
      <text class="section-title">会员权益</text>
      <view class="benefit-list">
        <view class="benefit-item" v-for="item in benefits" :key="item.title">
          <view class="benefit-icon-wrap">
            <image :src="item.icon" class="benefit-icon" mode="aspectFit" />
          </view>
          <view class="benefit-content">
            <text class="benefit-title">{{ item.title }}</text>
            <text class="benefit-desc">{{ item.desc }}</text>
          </view>
        </view>
      </view>
    </view>

    <view class="card membership-card">
      <text class="section-title">套餐说明</text>
      <view class="plan-list">
        <view class="plan-item" v-for="item in plans" :key="item.name">
          <view>
            <text class="plan-name">{{ item.name }}</text>
            <text class="plan-desc">{{ item.desc }}</text>
          </view>
          <text class="plan-price">{{ item.price }}</text>
        </view>
      </view>
      <button class="btn-primary membership-btn" @tap="comingSoon">立即开通</button>
      <text class="membership-tip">支付能力、会员订单、权益鉴权尚未接入，当前为占位版页面。</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      benefits: [
        {
          title: '专属减脂方案',
          desc: '获得更细化的饮食、运动和阶段性跟踪建议。',
          icon: '/static/icon_fit/geixnghua.png'
        },
        {
          title: '教练优先答疑',
          desc: '咨询问题优先进入教练工作台处理。',
          icon: '/static/icon_fit/yisheng.png'
        },
        {
          title: '会员专属内容',
          desc: '解锁更完整的训练、饮食与习惯养成专题。',
          icon: '/static/icon_fit/redu.png'
        },
        {
          title: '成长激励体系',
          desc: '会员任务、积分加速与更多勋章奖励可后续接入。',
          icon: '/static/icon_fit/jiangbei.png'
        }
      ],
      plans: [
        { name: '月度会员', desc: '适合短期减脂冲刺', price: '¥29/月' },
        { name: '季度会员', desc: '适合稳定执行计划', price: '¥79/季' },
        { name: '年度会员', desc: '适合长期健康管理', price: '¥199/年' }
      ]
    };
  },
  methods: {
    comingSoon() {
      uni.showToast({ title: '支付会员功能暂未接入', icon: 'none' });
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.membership-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.membership-card {
  margin-top: 16rpx;
}

.section-title {
  display: block;
  font-size: 30rpx;
  font-weight: 600;
  color: $text-primary;
  margin-bottom: 16rpx;
}

.benefit-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.benefit-item {
  display: flex;
  gap: 16rpx;
  padding: 18rpx;
  border-radius: 18rpx;
  background: #f7f9ff;
}

.benefit-icon-wrap {
  width: 72rpx;
  height: 72rpx;
  border-radius: 18rpx;
  background: #edf3ff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.benefit-icon {
  width: 38rpx;
  height: 38rpx;
}

.benefit-content {
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}

.benefit-title {
  font-size: 27rpx;
  font-weight: 600;
  color: $text-primary;
}

.benefit-desc {
  font-size: 22rpx;
  line-height: 1.6;
  color: $text-secondary;
}

.plan-list {
  display: flex;
  flex-direction: column;
  gap: 14rpx;
}

.plan-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16rpx;
  padding: 18rpx 20rpx;
  border-radius: 18rpx;
  background: #f6f9ff;
}

.plan-name {
  display: block;
  font-size: 27rpx;
  font-weight: 600;
  color: $text-primary;
}

.plan-desc {
  display: block;
  margin-top: 6rpx;
  font-size: 22rpx;
  color: $text-secondary;
}

.plan-price {
  flex-shrink: 0;
  font-size: 28rpx;
  font-weight: 700;
  color: $primary-color;
}

.membership-btn {
  width: 100%;
  margin-top: 20rpx;
}

.membership-tip {
  display: block;
  margin-top: 14rpx;
  font-size: 22rpx;
  color: $text-muted;
  line-height: 1.6;
}
</style>
