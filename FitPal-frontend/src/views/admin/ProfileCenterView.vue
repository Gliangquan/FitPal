<template>
  <a-card title="后台登录" :bordered="false">
    <a-row :gutter="24">
      <a-col :xs="24" :md="8" :lg="7">
        <div class="avatar-panel">
          <a-avatar :size="120" :src="avatarPreview">
            <template #icon>
              <user-outlined />
            </template>
          </a-avatar>
          <div class="account">{{ profile.userAccount || '-' }}</div>
          <a-upload
            accept="image/*"
            :show-upload-list="false"
            :before-upload="handleBeforeUpload"
            :disabled="uploading"
          >
            <a-button :loading="uploading">上传头像</a-button>
          </a-upload>
          <div class="hint">支持 jpg / png / webp，大小不超过 5MB</div>
        </div>
      </a-col>

      <a-col :xs="24" :md="16" :lg="17">
        <a-form layout="vertical">
          <a-form-item label="账号">
            <a-input :value="profile.userAccount" disabled />
          </a-form-item>
          <a-form-item label="昵称">
            <a-input v-model:value="profile.userName" allow-clear />
          </a-form-item>
          <a-form-item label="简介">
            <a-textarea v-model:value="profile.userProfile" :rows="4" :maxlength="300" show-count />
          </a-form-item>
          <a-space>
            <a-button type="primary" :loading="saving" @click="saveProfile">保存</a-button>
            <a-button :loading="loading" @click="loadProfile">刷新</a-button>
          </a-space>
        </a-form>
      </a-col>
    </a-row>
  </a-card>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { message } from 'ant-design-vue';
import { UserOutlined } from '@ant-design/icons-vue';
import { getLoginUser, resolveFilePreviewUrl, updateMyUser, uploadFile } from '../../api';

const loading = ref(false);
const saving = ref(false);
const uploading = ref(false);
const avatarPreview = ref('');

const profile = reactive<any>({
  id: undefined,
  userAccount: '',
  userName: '',
  userProfile: '',
  userAvatar: '',
});

const syncAvatarPreview = () => {
  avatarPreview.value = resolveFilePreviewUrl(profile.userAvatar);
};

const loadProfile = async () => {
  loading.value = true;
  try {
    const res = await getLoginUser();
    const latestUser = res.data || {};
    Object.assign(profile, latestUser);
    syncAvatarPreview();
    const localUser = JSON.parse(localStorage.getItem('user') || '{}');
    localStorage.setItem(
      'user',
      JSON.stringify({
        ...localUser,
        ...latestUser,
        token: latestUser.token || localUser.token,
      })
    );
    window.dispatchEvent(new Event('fitpal-user-updated'));
  } catch (error: any) {
    message.error(error?.message || '加载个人信息失败');
  } finally {
    loading.value = false;
  }
};

const handleBeforeUpload = async (file: File) => {
  const isImage = file.type.startsWith('image/');
  if (!isImage) {
    message.warning('请选择图片文件');
    return false;
  }

  const isLt5M = file.size / 1024 / 1024 < 5;
  if (!isLt5M) {
    message.warning('图片大小不能超过 5MB');
    return false;
  }

  uploading.value = true;
  try {
    const res = await uploadFile(file, 'user_avatar');
    profile.userAvatar = res.data || '';
    syncAvatarPreview();
    const localUser = JSON.parse(localStorage.getItem('user') || '{}');
    localStorage.setItem('user', JSON.stringify({ ...localUser, userAvatar: profile.userAvatar }));
    window.dispatchEvent(new Event('fitpal-user-updated'));
    message.success('头像上传成功');
  } catch (error: any) {
    message.error(error?.message || '头像上传失败');
  } finally {
    uploading.value = false;
  }
  return false;
};

const saveProfile = async () => {
  saving.value = true;
  try {
    await updateMyUser({
      userName: String(profile.userName || '').trim() || undefined,
      userProfile: profile.userProfile,
      userAvatar: profile.userAvatar,
    });
    message.success('保存成功');
    await loadProfile();
  } catch (error: any) {
    message.error(error?.message || '保存失败');
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  loadProfile();
});
</script>

<style scoped>
.avatar-panel {
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.account {
  font-weight: 600;
  color: #111827;
  word-break: break-all;
}

.hint {
  font-size: 12px;
  color: #6b7280;
}
</style>
