<template>
  <view class="ep-page">

    <!-- 头像区 -->
    <view class="avatar-section">
      <view class="avatar-wrap" @tap="chooseAvatar">
        <image
          v-if="form.userAvatar"
          :src="resolveAvatarUrl(form.userAvatar)"
          mode="aspectFill"
          class="avatar-img"
        />
        <view v-else class="avatar-fallback">
          <text class="avatar-initials">{{ form.userName ? form.userName.slice(0, 1) : '我' }}</text>
        </view>
        <!-- 编辑蒙层 -->
        <view class="avatar-mask">
          <uni-icons type="camera-filled" size="22" color="#fff" />
        </view>
      </view>
      <text class="avatar-hint">点击更换头像</text>
    </view>

    <!-- 信息表单卡片（基本信息 + 地址信息合并） -->
    <view class="form-card">

      <!-- 昵称 -->
      <view class="form-item">
        <text class="form-label"><text class="required">*</text>昵称</text>
        <uni-easyinput
          v-model="form.userName"
          placeholder="请输入昵称"
          :clearable="true"
          class="form-input"
        />
      </view>
      <view class="divider" />

      <!-- 手机号 -->
      <view class="form-item">
        <text class="form-label">手机号</text>
        <uni-easyinput
          v-model="form.userPhone"
          type="number"
          placeholder="请输入手机号"
          :clearable="true"
          class="form-input"
        />
      </view>
      <view class="divider" />

      <!-- 邮箱 -->
      <view class="form-item">
        <text class="form-label">邮箱</text>
        <uni-easyinput
          v-model="form.userEmail"
          placeholder="请输入邮箱"
          :clearable="true"
          class="form-input"
        />
      </view>
      <view class="divider" />

      <!-- 性别 -->
      <view class="form-item">
        <text class="form-label">性别</text>
        <view class="form-input">
          <uni-data-checkbox
            v-model="form.gender"
            :localdata="genderOptions"
          />
        </view>
      </view>
      <view class="divider" />

      <!-- 生日 -->
      <view class="form-item">
        <text class="form-label">生日</text>
        <view class="form-input">
          <uni-datetime-picker
            v-model="form.birthDate"
            type="date"
            placeholder="请选择生日"
          />
        </view>
      </view>
      <view class="divider" />

      <!-- 个人简介 -->
      <view class="form-item form-item--top">
        <text class="form-label">简介</text>
        <uni-easyinput
          v-model="form.userProfile"
          type="textarea"
          placeholder="介绍一下自己吧～"
          :maxlength="120"
          class="form-input"
        />
      </view>
      <view class="divider" />

      <!-- 所在地区 -->
      <view class="form-item">
        <text class="form-label">地区</text>
        <view class="form-input">
          <uni-data-picker
            v-model="form.region"
            :localdata="regionData"
            placeholder="请选择省 / 市 / 区"
            @change="onRegionChange"
          />
        </view>
      </view>
      <view class="divider" />

      <!-- 详细地址 -->
      <view class="form-item">
        <text class="form-label">地址</text>
        <uni-easyinput
          v-model="form.address"
          placeholder="街道、门牌号等"
          :clearable="true"
          class="form-input"
        />
      </view>

    </view>

    <!-- 操作按钮 -->
    <view class="btn-row">
      <button class="btn-cancel" @tap="cancelEdit">取消</button>
      <button class="btn-save" @tap="saveProfile">保存</button>
    </view>

  </view>
</template>

<script>
import { userApi } from '@/utils/api.js';
import { resolveFileUrl } from '@/utils/request.js';

const REGION_DATA = [
  {
    text: '北京市', value: '110000', children: [
      { text: '北京市', value: '110100', children: [
        { text: '东城区', value: '110101' }, { text: '西城区', value: '110102' },
        { text: '朝阳区', value: '110105' }, { text: '海淀区', value: '110108' },
        { text: '丰台区', value: '110106' }, { text: '石景山区', value: '110107' },
        { text: '通州区', value: '110112' }, { text: '昌平区', value: '110114' }
      ]}
    ]
  },
  {
    text: '上海市', value: '310000', children: [
      { text: '上海市', value: '310100', children: [
        { text: '黄浦区', value: '310101' }, { text: '徐汇区', value: '310104' },
        { text: '长宁区', value: '310105' }, { text: '静安区', value: '310106' },
        { text: '浦东新区', value: '310115' }, { text: '闵行区', value: '310112' },
        { text: '宝山区', value: '310113' }, { text: '嘉定区', value: '310114' }
      ]}
    ]
  },
  {
    text: '广东省', value: '440000', children: [
      { text: '广州市', value: '440100', children: [
        { text: '越秀区', value: '440104' }, { text: '海珠区', value: '440105' },
        { text: '天河区', value: '440106' }, { text: '白云区', value: '440111' }
      ]},
      { text: '深圳市', value: '440300', children: [
        { text: '福田区', value: '440304' }, { text: '罗湖区', value: '440303' },
        { text: '南山区', value: '440305' }, { text: '宝安区', value: '440306' }
      ]}
    ]
  },
  {
    text: '浙江省', value: '330000', children: [
      { text: '杭州市', value: '330100', children: [
        { text: '上城区', value: '330102' }, { text: '拱墅区', value: '330105' },
        { text: '西湖区', value: '330106' }, { text: '滨江区', value: '330108' },
        { text: '余杭区', value: '330110' }
      ]},
      { text: '宁波市', value: '330200', children: [
        { text: '海曙区', value: '330203' }, { text: '江北区', value: '330205' },
        { text: '鄞州区', value: '330212' }
      ]}
    ]
  },
  {
    text: '江苏省', value: '320000', children: [
      { text: '南京市', value: '320100', children: [
        { text: '玄武区', value: '320102' }, { text: '秦淮区', value: '320104' },
        { text: '建邺区', value: '320105' }, { text: '鼓楼区', value: '320106' }
      ]},
      { text: '苏州市', value: '320500', children: [
        { text: '姑苏区', value: '320508' }, { text: '吴中区', value: '320506' },
        { text: '相城区', value: '320507' }, { text: '吴江区', value: '320509' }
      ]}
    ]
  },
  {
    text: '四川省', value: '510000', children: [
      { text: '成都市', value: '510100', children: [
        { text: '锦江区', value: '510104' }, { text: '青羊区', value: '510105' },
        { text: '金牛区', value: '510106' }, { text: '武侯区', value: '510107' },
        { text: '成华区', value: '510108' }
      ]}
    ]
  }
];

export default {
  data() {
    return {
      form: {
        userName: '',
        userPhone: '',
        userEmail: '',
        gender: '女',
        birthDate: '',
        region: '',
        address: '',
        userProfile: '',
        userAvatar: ''
      },
      genderOptions: [
        { text: '男', value: '男' },
        { text: '女', value: '女' },
        { text: '保密', value: '保密' }
      ],
      regionData: REGION_DATA,
      regionText: { province: '', city: '', district: '' }
    };
  },

  async onLoad() {
    try {
      const user = await userApi.fetchCurrentUser();
      if (user) this.fillForm(user);
    } catch {
      const user = uni.getStorageSync('userInfo');
      if (user) this.fillForm(user);
    }
  },

  methods: {
    resolveAvatarUrl(url) {
      return resolveFileUrl(url);
    },
    isLocalTempFile(path) {
      if (!path) return false;
      const value = String(path).trim();
      if (!value) return false;
      if (
        value.startsWith('http://') ||
        value.startsWith('https://') ||
        value.startsWith('data:') ||
        value.startsWith('/files/') ||
        value.startsWith('/api/file/') ||
        value.startsWith('/file/')
      ) {
        return false;
      }
      return (
        value.startsWith('wxfile://') ||
        value.startsWith('file://') ||
        value.startsWith('blob:') ||
        value.startsWith('/private/') ||
        value.startsWith('/var/') ||
        value.startsWith('/tmp/')
      );
    },
    fillForm(user) {
      this.form = { ...this.form, ...user };
    },

    // 点击头像直接调起选图
    chooseAvatar() {
      uni.chooseImage({
        count: 1,
        sizeType: ['compressed'],
        sourceType: ['album', 'camera'],
        success: (res) => {
          const path = res.tempFilePaths[0];
          if (path) this.form.userAvatar = path;
        }
      });
    },

    onRegionChange(e) {
      const nodes = Array.isArray(e) ? e : (e?.detail ?? []);
      this.regionText.province = nodes[0]?.text || '';
      this.regionText.city     = nodes[1]?.text || '';
      this.regionText.district = nodes[2]?.text || '';
    },

    async saveProfile() {
      if (!this.form.userName?.trim()) {
        return uni.showToast({ title: '请输入昵称', icon: 'none' });
      }
      try {
        let avatarPath = this.form.userAvatar;
        if (this.isLocalTempFile(avatarPath)) {
          uni.showLoading({ title: '上传头像中...' });
          avatarPath = await userApi.uploadAvatar(avatarPath);
          this.form.userAvatar = avatarPath;
          uni.hideLoading();
        }

        const regionStr = [
          this.regionText.province,
          this.regionText.city,
          this.regionText.district
        ].filter(Boolean).join(' ');

        await userApi.updateProfile({
          userName:    this.form.userName,
          userAvatar:  avatarPath,
          userProfile: this.form.userProfile || regionStr,
          userPhone:   this.form.userPhone,
          userEmail:   this.form.userEmail,
          gender:      this.form.gender,
          birthDate:   this.form.birthDate,
          province:    this.regionText.province,
          city:        this.regionText.city,
          district:    this.regionText.district,
          address:     this.form.address
        });

        const refreshed = await userApi.fetchCurrentUser().catch(() => null);
        if (refreshed) uni.setStorageSync('userInfo', refreshed);

        uni.showToast({ title: '保存成功', icon: 'success' });
        setTimeout(() => uni.navigateBack(), 700);
      } catch (error) {
        uni.hideLoading();
        uni.showToast({ title: error.message || '保存失败', icon: 'none' });
      }
    },

    cancelEdit() {
      uni.navigateBack();
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.ep-page {
  min-height: 100vh;
  background: #f5f6fa;
  padding: 32rpx 24rpx 60rpx;
  box-sizing: border-box;
}

/* ── 头像区 ── */
.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40rpx 0 32rpx;
}

.avatar-wrap {
  position: relative;
  width: 160rpx;
  height: 160rpx;
  border-radius: 80rpx;
  overflow: hidden;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.15);

  .avatar-img {
    width: 100%;
    height: 100%;
    display: block;
  }

  .avatar-fallback {
    width: 100%;
    height: 100%;
    background: $primary-color;
    display: flex;
    align-items: center;
    justify-content: center;

    .avatar-initials {
      font-size: 56rpx;
      font-weight: 700;
      color: #fff;
    }
  }

  /* 相机蒙层 */
  .avatar-mask {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 56rpx;
    background: rgba(0, 0, 0, 0.42);
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

.avatar-hint {
  margin-top: 16rpx;
  font-size: 24rpx;
  color: $text-muted;
}

/* ── 表单卡片 ── */
.form-card {
  background: #fff;
  border-radius: $radius-lg;
  overflow: hidden;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

/* 每一行 */
.form-item {
  display: flex;
  align-items: center;
  padding: 0 32rpx;
  min-height: 100rpx;

  &--top {
    align-items: flex-start;
    padding-top: 24rpx;
    padding-bottom: 24rpx;
  }
}

.form-label {
  width: 120rpx;
  flex-shrink: 0;
  font-size: 28rpx;
  color: $text-primary;
  font-weight: 500;

  .required {
    color: #f44;
    margin-right: 4rpx;
  }
}

.form-input {
  flex: 1;
  min-width: 0;

  /* 去掉 uni-easyinput 默认边框 */
  :deep(.uni-easyinput__content) {
    border: none !important;
    background: transparent !important;
    padding-left: 0 !important;
  }

  :deep(.uni-easyinput) {
    border: none !important;
    background: transparent !important;
  }

  /* uni-datetime-picker 对齐 */
  :deep(.uni-date-editor) {
    border: none !important;
    background: transparent !important;
    padding-left: 0 !important;
  }

  /* uni-data-picker 对齐 */
  :deep(.uni-data-picker) {
    border: none !important;
    padding-left: 0 !important;
  }
  :deep(.uni-data-picker__value) {
    padding-left: 0 !important;
  }

  /* uni-data-checkbox 间距 */
  :deep(.uni-data-checklist) {
    padding: 0 !important;
  }
}

.divider {
  height: 1rpx;
  background: #f0f0f0;
  margin: 0 32rpx;
}

/* ── 底部按钮 ── */
.btn-row {
  display: flex;
  gap: 24rpx;
  margin-top: 48rpx;
}

.btn-cancel {
  flex: 1;
  height: 88rpx;
  line-height: 88rpx;
  border-radius: $radius-full;
  font-size: 30rpx;
  font-weight: 500;
  color: $text-secondary;
  background: #fff;
  border: 2rpx solid #e0e0e0;
}

.btn-save {
  flex: 1;
  height: 88rpx;
  line-height: 88rpx;
  border-radius: $radius-full;
  font-size: 30rpx;
  font-weight: 600;
  color: #fff;
  background: $primary-color;
  border: none;
}
</style>
