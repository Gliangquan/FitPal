<template>
  <div class="register-page">
    <a-card class="register-card" :bordered="false">
      <h2>注册账号</h2>

      <a-form layout="vertical">
        <a-form-item label="账号">
          <a-input v-model:value="form.userAccount" placeholder="请输入账号" />
        </a-form-item>

        <a-form-item label="手机号">
          <a-input v-model:value="form.userPhone" placeholder="请输入手机号" />
        </a-form-item>

        <a-form-item label="密码">
          <a-input-password v-model:value="form.userPassword" placeholder="请输入密码" />
        </a-form-item>

        <a-form-item label="确认密码">
          <a-input-password v-model:value="form.checkPassword" placeholder="请确认密码" />
        </a-form-item>

        <a-form-item>
          <a-button type="primary" block :loading="loading" @click="handleSubmit">注册</a-button>
        </a-form-item>
      </a-form>

      <div class="actions">
        <a @click="router.push('/login')">已有账号？去登录</a>
      </div>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import { userRegister } from '../api';

const router = useRouter();
const loading = ref(false);

const form = reactive({
  userAccount: '',
  userPhone: '',
  userPassword: '',
  checkPassword: '',
});

const handleSubmit = async () => {
  const userAccount = form.userAccount?.trim();
  const userPhone = form.userPhone?.trim();
  const userPassword = form.userPassword?.trim();
  const checkPassword = form.checkPassword?.trim();

  if (!userAccount) {
    message.warning('请输入账号');
    return;
  }

  if (!userPhone) {
    message.warning('请输入手机号');
    return;
  }

  if (!userPassword) {
    message.warning('请输入密码');
    return;
  }

  if (!checkPassword) {
    message.warning('请确认密码');
    return;
  }

  if (userPassword !== checkPassword) {
    message.error('两次密码不一致');
    return;
  }

  loading.value = true;
  try {
    await userRegister({
      userAccount,
      userPhone,
      userPassword,
      checkPassword,
    });
    message.success('注册成功，请登录');
    router.replace('/login');
  } catch (error: any) {
    message.error(error?.message || '注册失败');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: linear-gradient(160deg, #f8fafc, #e2e8f0);
  padding: 16px;
}

.register-card {
  width: 420px;
  border-radius: 14px;
}

.actions {
  text-align: center;
}
</style>
