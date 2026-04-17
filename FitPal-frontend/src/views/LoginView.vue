<template>
  <div class="login-page">
    <a-card class="login-card" :bordered="false">
      <h2>FitPal PC 登录</h2>
      <p class="sub">   </p>

      <a-segmented
        v-model:value="loginType"
        :options="[
          { label: '账号登录', value: 'account' },
          { label: '手机号登录', value: 'phone' },
        ]"
        block
        style="margin-bottom: 16px"
      />

      <a-form layout="vertical">
        <a-form-item v-if="loginType === 'account'" label="账号">
          <a-input v-model:value="form.userAccount" placeholder="请输入账号" />
        </a-form-item>
        <a-form-item v-else label="手机号">
          <a-input v-model:value="form.userPhone" placeholder="请输入手机号" />
        </a-form-item>
        <a-form-item label="密码">
          <a-input-password v-model:value="form.userPassword" placeholder="请输入密码" />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" block :loading="loading" @click="handleLogin">登录</a-button>
        </a-form-item>
      </a-form>

      <div class="actions">
        <a @click="router.push('/register')">还没有账号？去注册</a>
      </div>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import { userLogin, type UserLoginRequest } from '../api';

const router = useRouter();
const loading = ref(false);
const loginType = ref<'phone' | 'account'>('account');

const form = reactive({
  userAccount: '',
  userPhone: '',
  userPassword: '',
});

const handleLogin = async () => {
  const password = form.userPassword?.trim();
  const account = form.userAccount?.trim();
  const phone = form.userPhone?.trim();

  if (!password) {
    message.warning('请输入密码');
    return;
  }

  if (loginType.value === 'account' && !account) {
    message.warning('请输入账号');
    return;
  }

  if (loginType.value === 'phone' && !phone) {
    message.warning('请输入手机号');
    return;
  }

  const params: UserLoginRequest = {
    loginType: loginType.value,
    userPassword: password,
    userAccount: loginType.value === 'account' ? account : undefined,
    userPhone: loginType.value === 'phone' ? phone : undefined,
  };

  loading.value = true;
  try {
    const res = await userLogin(params);
    if (res.data?.userRole !== 'admin') {
      message.error('PC 端仅支持管理员账号登录');
      return;
    }
    localStorage.setItem('user', JSON.stringify(res.data));
    message.success('登录成功');
    router.replace('/admin/users');
  } catch (error: any) {
    message.error(error?.message || '登录失败');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: radial-gradient(circle at 10% 10%, #dbeafe, #eff6ff 40%, #f8fafc 75%);
  padding: 16px;
}

.login-card {
  width: 420px;
  border-radius: 14px;
}

h2 {
  margin: 0;
}

.sub {
  color: #64748b;
  margin: 8px 0 16px;
}

.actions {
  text-align: center;
}
</style>
