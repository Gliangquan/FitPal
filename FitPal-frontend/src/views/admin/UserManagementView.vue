<template>
  <a-card title="用户账号管理" :bordered="false">
    <a-space style="margin-bottom: 12px" wrap>
      <a-input v-model:value="query.userName" placeholder="昵称" allow-clear style="width: 180px" />
      <a-select v-model:value="query.userRole" placeholder="角色" allow-clear style="width: 140px">
        <a-select-option value="user">普通用户</a-select-option>
        <a-select-option value="coach">教练</a-select-option>
        <a-select-option value="admin">管理员</a-select-option>
        <a-select-option value="ban">封禁</a-select-option>
      </a-select>
      <a-button type="primary" @click="handleSearch">查询</a-button>
      <a-button @click="resetSearch">重置</a-button>
      <a-divider type="vertical" />
      <a-button @click="openModal(null)">新增</a-button>
      <a-select v-model:value="exportFormat" style="width: 120px">
        <a-select-option value="excel">excel</a-select-option>
        <a-select-option value="csv">csv</a-select-option>
        <a-select-option value="json">json</a-select-option>
      </a-select>
      <a-button @click="doExport">导出</a-button>
      <a-button :loading="importing" @click="triggerImport">导入</a-button>
      <input ref="importRef" type="file" style="display:none" accept=".csv,.xls,.xlsx" @change="onImportChange" />
    </a-space>

    <a-table
      :columns="columns"
      :data-source="rows"
      :loading="loading"
      :pagination="pagination"
      row-key="id"
      @change="onTableChange"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'userAvatar'">
          <a-avatar
            :size="40"
            :src="resolveFilePreviewUrl(record.userAvatar)"
          >
            <template #icon>
              <user-outlined />
            </template>
          </a-avatar>
        </template>
        <template v-else-if="column.key === 'userRole'">
          <a-tag :color="roleColor(record.userRole)">{{ roleLabel(record.userRole) }}</a-tag>
        </template>
        <template v-if="column.key === 'action'">
          <a-space>
            <a-button size="small" @click="openModal(record)">编辑</a-button>
            <a-popconfirm title="确认删除该用户？" @confirm="doDelete(record)">
              <a-button size="small" danger>删除</a-button>
            </a-popconfirm>
          </a-space>
        </template>
      </template>
    </a-table>

    <a-modal v-model:open="modalOpen" :title="editing ? '编辑用户' : '新增用户'" @ok="submit" :confirm-loading="saving">
      <a-form layout="vertical">
        <a-form-item label="账号" required>
          <a-input v-model:value="form.userAccount" :disabled="!!editing" />
        </a-form-item>
        <a-form-item label="昵称">
          <a-input v-model:value="form.userName" />
        </a-form-item>
        <a-form-item label="简介">
          <a-textarea v-model:value="form.userProfile" :rows="2" />
        </a-form-item>
        <a-form-item label="角色">
          <a-select v-model:value="form.userRole">
            <a-select-option value="user">普通用户</a-select-option>
            <a-select-option value="coach">教练</a-select-option>
            <a-select-option value="admin">管理员</a-select-option>
            <a-select-option value="ban">封禁</a-select-option>
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>
  </a-card>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { message } from 'ant-design-vue';
import { UserOutlined } from '@ant-design/icons-vue';
import {
  addUser,
  deleteUser,
  exportUser,
  importUser,
  listUserByPage,
  updateUser,
  resolveFilePreviewUrl,
} from '../../api';

const loading = ref(false);
const saving = ref(false);
const importing = ref(false);

const rows = ref<any[]>([]);
const query = reactive<any>({
  userName: '',
  userRole: undefined,
});
const exportFormat = ref<'excel' | 'csv' | 'json'>('excel');

const pagination = reactive<any>({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
});

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 90 },
  { title: '头像', dataIndex: 'userAvatar', key: 'userAvatar', width: 80 },
  { title: '账号', dataIndex: 'userAccount', key: 'userAccount' },
  { title: '昵称', dataIndex: 'userName', key: 'userName' },
  { title: '角色', dataIndex: 'userRole', key: 'userRole', width: 120 },
  { title: '状态', dataIndex: 'status', key: 'status', width: 100 },
  { title: '创建时间', dataIndex: 'createTime', key: 'createTime', width: 180 },
  { title: '操作', key: 'action', width: 180 },
];

const roleLabelMap: Record<string, string> = {
  user: '普通用户',
  coach: '教练',
  admin: '管理员',
  ban: '封禁',
};

const roleLabel = (role?: string) => roleLabelMap[role || ''] || role || '-';

const roleColor = (role?: string) => {
  if (role === 'admin') return 'red';
  if (role === 'coach') return 'blue';
  if (role === 'ban') return 'default';
  return 'green';
};

const modalOpen = ref(false);
const editing = ref<any>(null);
const form = reactive<any>({
  id: undefined,
  userAccount: '',
  userName: '',
  userProfile: '',
  userRole: 'user',
});

const importRef = ref<HTMLInputElement | null>(null);

const load = async () => {
  loading.value = true;
  try {
    const res = await listUserByPage({
      current: pagination.current,
      pageSize: pagination.pageSize,
      userName: query.userName || undefined,
      userRole: query.userRole || undefined,
    });
    rows.value = res.data?.records || [];
    pagination.total = res.data?.total || 0;
    pagination.current = res.data?.current || pagination.current;
    pagination.pageSize = res.data?.size || pagination.pageSize;
  } catch (error: any) {
    message.error(error?.message || '加载失败');
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  pagination.current = 1;
  load();
};

const resetSearch = () => {
  query.userName = '';
  query.userRole = undefined;
  pagination.current = 1;
  load();
};

const onTableChange = (p: any) => {
  pagination.current = p.current;
  pagination.pageSize = p.pageSize;
  load();
};

const openModal = (row: any | null) => {
  editing.value = row;
  if (row) {
    Object.assign(form, {
      id: row.id,
      userAccount: row.userAccount,
      userName: row.userName,
      userProfile: row.userProfile,
      userRole: row.userRole,
    });
  } else {
    Object.assign(form, {
      id: undefined,
      userAccount: '',
      userName: '',
      userProfile: '',
      userRole: 'user',
    });
  }
  modalOpen.value = true;
};

const submit = async () => {
  if (!editing.value && !String(form.userAccount || '').trim()) {
    message.warning('请输入账号');
    return;
  }
  saving.value = true;
  try {
    if (editing.value) {
      await updateUser({
        id: form.id,
        userName: form.userName,
        userProfile: form.userProfile,
        userRole: form.userRole,
      });
      message.success('更新成功');
    } else {
      await addUser({
        userAccount: form.userAccount,
        userName: form.userName,
        userRole: form.userRole,
      });
      message.success('新增成功');
    }
    modalOpen.value = false;
    load();
  } catch (error: any) {
    message.error(error?.message || '保存失败');
  } finally {
    saving.value = false;
  }
};

const doDelete = async (row: any) => {
  try {
    await deleteUser({ id: row.id });
    message.success('删除成功');
    load();
  } catch (error: any) {
    message.error(error?.message || '删除失败');
  }
};

const doExport = async () => {
  try {
    const res = await exportUser({
      format: exportFormat.value,
      userName: query.userName || undefined,
      userRole: query.userRole || undefined,
      exportAll: true,
    });
    message.success(`导出任务已生成：${res.data}`);
  } catch (error: any) {
    message.error(error?.message || '导出失败');
  }
};

const triggerImport = () => {
  importRef.value?.click();
};

const fileToBase64 = (file: File): Promise<string> =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const content = String(reader.result || '');
      resolve(content.includes(',') ? content.split(',')[1] : content);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });

const onImportChange = async (event: Event) => {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];
  if (!file) return;

  importing.value = true;
  try {
    const fileContent = await fileToBase64(file);
    const fileType = file.name.toLowerCase().endsWith('.csv') ? 'csv' : 'excel';
    const res = await importUser({
      fileContent,
      fileType,
      skipDuplicate: true,
      defaultPassword: '12345678',
      defaultRole: 'user',
    });
    message.success(`导入完成，新增 ${res.data || 0} 条`);
    load();
  } catch (error: any) {
    message.error(error?.message || '导入失败');
  } finally {
    importing.value = false;
    if (input) input.value = '';
  }
};

onMounted(() => {
  load();
});
</script>
