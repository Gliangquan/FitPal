<template>
  <div class="system-settings">
    <a-card title="系统设置" :bordered="false">
      <a-tabs>
        <a-tab-pane key="1" tab="基础配置">
          <a-form :model="basicSettings" layout="vertical" style="max-width: 600px">
            <a-form-item label="平台名称">
              <a-input v-model:value="basicSettings.platformName" />
            </a-form-item>
            <a-form-item label="平台描述">
              <a-textarea v-model:value="basicSettings.platformDescription" />
            </a-form-item>
            <a-form-item label="联系电话">
              <a-input v-model:value="basicSettings.contactPhone" />
            </a-form-item>
            <a-form-item label="联系邮箱">
              <a-input v-model:value="basicSettings.contactEmail" />
            </a-form-item>
            <a-form-item label="服务条款URL">
              <a-input v-model:value="basicSettings.termsUrl" />
            </a-form-item>
            <a-form-item label="隐私政策URL">
              <a-input v-model:value="basicSettings.privacyUrl" />
            </a-form-item>
            <a-button type="primary" @click="handleSaveBasicSettings" :loading="saveLoading">保存</a-button>
          </a-form>
        </a-tab-pane>
      </a-tabs>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import {
  getBasicSettings,
  updateBasicSettings,
} from '../../api';

const saveLoading = ref(false);

const basicSettings = reactive({
  platformName: '',
  platformDescription: '',
  contactPhone: '',
  contactEmail: '',
  termsUrl: '',
  privacyUrl: '',
});

const fetchBasicSettings = async () => {
  try {
    const basicRes = await getBasicSettings();
    if (basicRes.data) Object.assign(basicSettings, basicRes.data);
  } catch (error) {
    message.error('获取设置失败');
  }
};

const handleSaveBasicSettings = async () => {
  saveLoading.value = true;
  try {
    await updateBasicSettings(basicSettings);
    message.success('基础配置已保存');
  } catch (error) {
    message.error('保存失败');
  } finally {
    saveLoading.value = false;
  }
};

onMounted(() => {
  fetchBasicSettings();
});
</script>

<style scoped>
.system-settings {
  padding: 0;
}
</style>
