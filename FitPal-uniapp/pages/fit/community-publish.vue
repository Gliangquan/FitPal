<template>
  <view class="page-content publish-page">
    <view class="hero-section publish-hero">
      <text class="text-lg font-bold text-primary">发布动态</text>
      <text class="text-sm text-secondary" style="display:block;margin-top:6rpx;">记录饮食、运动和减脂心得</text>
    </view>

    <view class="card form-card">
      <uni-forms label-position="top">
        <uni-forms-item label="标题">
          <uni-easyinput
            v-model="form.title"
            placeholder="请输入文章标题（必填）"
            maxlength="100"
            :clearable="true"
          />
          <text class="char-count">{{ form.title.length }}/100</text>
        </uni-forms-item>

        <uni-forms-item label="分类">
          <view class="category-list">
            <view
              v-for="(cat, idx) in categories"
              :key="cat.value"
              class="category-item"
              :class="{ active: form.category === cat.value }"
              @tap="form.category = cat.value"
            >
              {{ cat.text }}
            </view>
          </view>
        </uni-forms-item>

        <uni-forms-item label="内容">
          <uni-easyinput
            v-model="form.content"
            type="textarea"
            placeholder="分享你的减脂心得、饮食经验、运动打卡等..."
            maxlength="5000"
          />
          <text class="char-count">{{ form.content.length }}/5000</text>
        </uni-forms-item>
      </uni-forms>

      <view class="image-section">
        <text class="section-label">图片（最多9张）</text>
        <view class="image-grid">
          <view class="image-item" v-for="(img, idx) in form.images" :key="idx">
            <image :src="img" mode="aspectFill" />
            <view class="image-delete" @tap="deleteImage(idx)">
              <uni-icons type="close" size="14" color="#fff" />
            </view>
          </view>
          <view v-if="form.images.length < 9" class="image-add" @tap="chooseImages">
            <uni-icons type="plus" size="22" color="#94a3b8" />
            <text class="text-sm text-muted">添加图片</text>
          </view>
        </view>
      </view>

      <button class="publish-btn" :disabled="!canPublish || loading" @tap="handlePublish">
        {{ loading ? '发布中...' : '发布' }}
      </button>
    </view>
  </view>
</template>

<script>
import { fitApi } from '@/utils/api.js';

export default {
  data() {
    return {
      form: {
        title: '',
        category: 'weight-loss',
        content: '',
        images: []
      },
      categories: [
        { text: '减脂心得', value: 'weight-loss' },
        { text: '饮食分享', value: 'diet' },
        { text: '运动打卡', value: 'workout' },
        { text: '成果展示', value: 'achievement' },
        { text: '问题求助', value: 'help' }
      ],
      loading: false
    };
  },
  computed: {
    canPublish() {
      return this.form.title.trim() && this.form.content.trim() && !this.loading;
    }
  },
  methods: {
    chooseImages() {
      const remaining = 9 - this.form.images.length;
      uni.chooseImage({
        count: remaining,
        sizeType: ['compressed'],
        sourceType: ['album', 'camera'],
        success: (res) => {
          this.form.images = [...this.form.images, ...res.tempFilePaths];
        }
      });
    },
    deleteImage(idx) {
      this.form.images.splice(idx, 1);
    },
    isLocalTempFile(path) {
      if (!path) return false;
      const value = String(path).trim();
      if (!value) return false;
      // 微信临时文件 http://tmp/xxx 需要上传
      if (value.startsWith('http://tmp/')) {
        return true;
      }
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
    async uploadImages() {
      if (!this.form.images.length) return [];
      const uploaded = [];
      for (let i = 0; i < this.form.images.length; i++) {
        const filePath = this.form.images[i];
        if (!this.isLocalTempFile(filePath)) {
          // 已是远程路径，直接使用
          uploaded.push(filePath);
          continue;
        }
        try {
          console.log('[发布] 开始上传图片', filePath, `(${i+1}/${this.form.images.length})`);
          const remotePath = await fitApi.uploadCommunityImage(filePath);
          if (remotePath) {
            uploaded.push(remotePath);
            console.log('[发布] 图片上传成功', remotePath);
          }
          // 等待上传任务完全完成
          await new Promise(resolve => setTimeout(resolve, 1000));
        } catch (error) {
          console.error('[发布] 单张图片上传失败', filePath, error);
          uni.showToast({ title: '图片上传失败，请重试', icon: 'none' });
          throw error; // 抛出错误，停止发布
        }
      }
      return uploaded;
    },
    async handlePublish() {
      if (!this.canPublish) {
        uni.showToast({ title: '请填写标题和内容', icon: 'none' });
        return;
      }

      this.loading = true;
      try {
        console.log('[发布] 开始上传图片');
        let imageUrls = [];
        if (this.form.images.length > 0) {
          imageUrls = await this.uploadImages();
          console.log('[发布] 图片上传完成', imageUrls);
        }
        const imageUrlsText = imageUrls.length ? JSON.stringify(imageUrls) : undefined;
        console.log('[发布] 准备提交帖子', { title: this.form.title, content: this.form.content, category: this.form.category, imageUrlsText });

        const result = await fitApi.addCommunityPost({
          title: this.form.title,
          content: this.form.content,
          category: this.form.category,
          imageUrls: imageUrlsText
        });
        console.log('[发布] 发布成功', result);

        const badge = result?.badgeAwarded;
        uni.showToast({ title: badge ? `获得${badge.badgeName}` : '发布成功', icon: 'success' });
        setTimeout(() => {
          uni.navigateBack();
        }, 700);
      } catch (error) {
        console.error('[发布] 发布失败', error);
        uni.showToast({ title: error.message || '发布失败', icon: 'none' });
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style lang="scss">
@import "@/styles/common.scss";

.publish-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 32rpx;
}

.publish-hero {
  margin-bottom: 16rpx;
}

.form-card {
  padding: 22rpx;
}

.char-count {
  font-size: 20rpx;
  color: $text-muted;
  display: block;
  margin-top: 8rpx;
  text-align: right;
}

.image-section {
  margin-top: 8rpx;
}

.section-label {
  display: block;
  font-size: 26rpx;
  font-weight: 500;
  color: $text-primary;
  margin-bottom: 12rpx;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12rpx;
}

.image-item {
  position: relative;
  height: 200rpx;
  border-radius: 12rpx;
  overflow: hidden;
  background: #f1f5f9;

  image {
    width: 100%;
    height: 100%;
    display: block;
  }
}

.image-delete {
  position: absolute;
  top: 6rpx;
  right: 6rpx;
  width: 30rpx;
  height: 30rpx;
  border-radius: 50%;
  background: rgba(15, 23, 42, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-add {
  height: 200rpx;
  border: 2rpx dashed #d1dbe8;
  border-radius: 12rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8rpx;
  background: #f8fbff;
}

.publish-btn {
  margin-top: 28rpx;
  width: 100%;
  height: 82rpx;
  line-height: 82rpx;
  border-radius: 999rpx;
  border: none;
  background: $primary-color;
  color: #fff;
  font-size: 28rpx;
  font-weight: 600;

  &:disabled {
    opacity: 0.55;
  }
}

.category-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.category-item {
  padding: 12rpx 24rpx;
  border-radius: 40rpx;
  background: #f1f5f9;
  color: #64748b;
  font-size: 24rpx;
  border: 2rpx solid transparent;
  transition: all 0.2s;

  &.active {
    background: #eff6ff;
    color: #2f65f9;
    border-color: #2f65f9;
  }
}
</style>
