<template>
  <a-layout class="layout-root">
    <a-layout-sider v-model:collapsed="collapsed" :trigger="null" collapsible class="sider">
      <div class="brand" @click="go('/admin/users')">
        <div class="brand-dot" />
        <span v-if="!collapsed">FitPal Admin</span>
      </div>

      <a-menu
        v-model:selectedKeys="selectedKeys"
        mode="inline"
        :inline-collapsed="collapsed"
        :items="menuItems"
        @click="onMenuClick"
        class="side-menu"
      />
    </a-layout-sider>

    <a-layout>
      <a-layout-header class="header">
        <div class="header-left">
          <a-button type="text" @click="collapsed = !collapsed">
            <menu-unfold-outlined v-if="collapsed" />
            <menu-fold-outlined v-else />
          </a-button>
        </div>

        <div class="header-right">
          <a-space>
            <a-tag color="red">管理员</a-tag>
            <a-dropdown>
              <a class="user-link" @click.prevent>
                <a-avatar :src="headerAvatar">
                  <template #icon>
                    <user-outlined />
                  </template>
                </a-avatar>
                <span>{{ currentUser.userName || currentUser.userAccount || 'admin' }}</span>
              </a>
              <template #overlay>
                <a-menu>
                  <a-menu-item key="logout" @click="handleLogout">退出登录</a-menu-item>
                </a-menu>
              </template>
            </a-dropdown>
          </a-space>
        </div>
      </a-layout-header>

      <a-layout-content class="content">
        <router-view />
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup lang="ts">
import { computed, h, onBeforeUnmount, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  UserOutlined,
  AuditOutlined,
  FileSearchOutlined,
  FileTextOutlined,
  IdcardOutlined,
  GiftOutlined,
  BarChartOutlined,
  SettingOutlined,
  CalendarOutlined,
  FileOutlined,
  MessageOutlined,
} from '@ant-design/icons-vue';
import { getLoginUser, resolveFilePreviewUrl, userLogout } from '../api';

const router = useRouter();
const route = useRoute();

const collapsed = ref(false);
const selectedKeys = ref<string[]>([route.path]);
const currentUser = ref<any>({});
const headerAvatar = computed(() => resolveFilePreviewUrl(currentUser.value?.userAvatar));

const menuItems = computed(() => [
  {
    key: '/admin/users',
    icon: () => h(UserOutlined),
    label: '用户管理',
  },
  {
    key: '/admin/coach-applications',
    icon: () => h(AuditOutlined),
    label: '教练审核',
  },
  {
    key: '/admin/content-review',
    icon: () => h(FileSearchOutlined),
    label: '内容审核',
  },
  {
    key: '/admin/community-moderation',
    icon: () => h(MessageOutlined),
    label: '社区审核',
  },
  {
    key: '/admin/plans',
    icon: () => h(FileTextOutlined),
    label: '方案管理',
  },
  {
    key: '/admin/content',
    icon: () => h(FileOutlined),
    label: '内容管理',
  },
  {
    key: '/admin/solar-terms',
    icon: () => h(CalendarOutlined),
    label: '节气管理',
  },
  {
    key: '/admin/points',
    icon: () => h(GiftOutlined),
    label: '积分管理',
  },
  {
    key: '/admin/statistics',
    icon: () => h(BarChartOutlined),
    label: '数据统计',
  },
  {
    key: '/admin/settings',
    icon: () => h(SettingOutlined),
    label: '系统设置',
  },
  {
    key: '/admin/profile',
    icon: () => h(IdcardOutlined),
    label: '个人中心',
  },
]);

const go = (path: string) => {
  router.push(path);
};

const onMenuClick = ({ key }: { key: string }) => {
  go(key);
};

const fetchLoginUser = async () => {
  try {
    const res = await getLoginUser();
    currentUser.value = res.data || {};
  } catch (error) {
    currentUser.value = JSON.parse(localStorage.getItem('user') || '{}');
  }
};

const handleUserUpdated = () => {
  currentUser.value = JSON.parse(localStorage.getItem('user') || '{}');
  fetchLoginUser();
};

const handleLogout = async () => {
  try {
    await userLogout();
  } catch (error) {
    // ignore
  }
  localStorage.removeItem('user');
  message.success('已退出登录');
  router.replace('/login');
};

watch(
  () => route.path,
  (path) => {
    selectedKeys.value = [path];
    fetchLoginUser();
  },
  { immediate: true }
);

onMounted(() => {
  window.addEventListener('fitpal-user-updated', handleUserUpdated);
});

onBeforeUnmount(() => {
  window.removeEventListener('fitpal-user-updated', handleUserUpdated);
});
</script>

<style scoped>
.layout-root {
  min-height: 100vh;
}

.sider {
  background: #ffffff;
  border-right: 1px solid #f0f0f0;
}

.brand {
  height: 56px;
  margin: 12px;
  border-radius: 10px;
  background: #f8fafc;
  color: #111827;
  border: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  font-weight: 600;
}

.brand-dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #2563eb;
}

.side-menu {
  background: #ffffff;
}

:deep(.side-menu .ant-menu-item-selected) {
  background: #e6f4ff;
  color: #1677ff;
}

.header {
  background: #fff;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #f0f0f0;
}

.user-link {
  color: #111827;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.content {
  padding: 16px;
  background: #f5f7fb;
}
</style>
