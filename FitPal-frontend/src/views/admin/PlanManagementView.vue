<template>
  <a-card title="方案管理" :bordered="false">
    <a-space style="margin-bottom: 12px" wrap>
      <a-select v-model:value="query.status" allow-clear placeholder="方案类型" style="width: 180px">
        <a-select-option value="system">系统方案</a-select-option>
        <a-select-option value="coached">教练优化</a-select-option>
      </a-select>
      <a-input v-model:value="query.userId" placeholder="用户ID" allow-clear style="width: 130px" />
      <a-input v-model:value="query.keyword" placeholder="用户昵称关键词" allow-clear style="width: 220px" />
      <a-button type="primary" @click="handleSearch">查询</a-button>
      <a-button @click="resetSearch">重置</a-button>
      <a-divider type="vertical" />
      <a-button @click="openEditModal(null)">新增</a-button>
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
        <template v-if="column.key === 'status'">
          <a-tag :color="record.status === 'coached' ? 'blue' : 'default'">{{ statusLabel(record.status) }}</a-tag>
        </template>
        <template v-if="column.key === 'action'">
          <a-space>
            <a-button size="small" @click="openEditModal(record)">编辑</a-button>
            <a-popconfirm title="确认删除该方案？" @confirm="doDelete(record)">
              <a-button size="small" danger>删除</a-button>
            </a-popconfirm>
            <a-button size="small" @click="openOptimize(record)">优化</a-button>
          </a-space>
        </template>
      </template>
    </a-table>

    <a-modal v-model:open="editModalOpen" :title="editing ? '编辑方案' : '新增方案'" @ok="submitEdit" :confirm-loading="saving" width="760px">
      <a-form layout="vertical">
        <a-form-item label="用户ID" required>
          <a-input-number v-model:value="editForm.userId" :min="1" style="width: 100%" />
        </a-form-item>
        <a-form-item label="目标热量（kcal）">
          <a-input-number v-model:value="editForm.targetCalories" :min="0" style="width: 100%" />
        </a-form-item>
        <a-form-item label="饮食建议">
          <a-textarea v-model:value="editForm.dietPlan" :rows="3" />
        </a-form-item>
        <a-form-item label="运动建议">
          <a-textarea v-model:value="editForm.exercisePlan" :rows="3" />
        </a-form-item>
        <a-form-item label="生活建议">
          <a-textarea v-model:value="editForm.lifestyleTips" :rows="3" />
        </a-form-item>
        <a-form-item label="来源类型">
          <a-select v-model:value="editForm.source">
            <a-select-option value="mifflin-st-jeor">系统计算</a-select-option>
            <a-select-option value="coach-optimize">教练优化</a-select-option>
            <a-select-option value="admin-manual">管理员录入</a-select-option>
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>

    <a-modal v-model:open="optimizeModalOpen" title="优化方案" @ok="submitOptimize" :confirm-loading="optimizing">
      <a-form layout="vertical">
        <a-form-item label="饮食建议">
          <a-textarea v-model:value="optimizeForm.dietPlan" :rows="3" />
        </a-form-item>
        <a-form-item label="运动建议">
          <a-textarea v-model:value="optimizeForm.exercisePlan" :rows="3" />
        </a-form-item>
        <a-form-item label="生活建议">
          <a-textarea v-model:value="optimizeForm.lifestyleTips" :rows="3" />
        </a-form-item>
        <a-form-item label="教练备注">
          <a-input v-model:value="optimizeForm.coachNote" />
        </a-form-item>
      </a-form>
    </a-modal>
  </a-card>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { message } from 'ant-design-vue';
import {
  addAdminPlan,
  deleteAdminPlan,
  listCoachPlans,
  optimizePlan,
  updateAdminPlan,
} from '../../api';

const loading = ref(false);
const saving = ref(false);
const optimizing = ref(false);
const rows = ref<any[]>([]);

const query = reactive<any>({
  status: undefined,
  userId: '',
  keyword: '',
});

const pagination = reactive<any>({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
});

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 90 },
  { title: '用户ID', dataIndex: 'userId', key: 'userId', width: 100 },
  { title: '用户昵称', dataIndex: 'userNickname', key: 'userNickname' },
  { title: '目标热量', dataIndex: 'targetCalories', key: 'targetCalories', width: 120 },
  { title: '状态', dataIndex: 'status', key: 'status', width: 120 },
  { title: '创建时间', dataIndex: 'createdAt', key: 'createdAt', width: 180 },
  { title: '操作', key: 'action', width: 240 },
];

const statusLabelMap: Record<string, string> = {
  system: '系统方案',
  coached: '教练优化',
};

const statusLabel = (status?: string) => statusLabelMap[status || ''] || status || '-';

const editModalOpen = ref(false);
const editing = ref<any>(null);
const editForm = reactive<any>({
  id: undefined,
  userId: undefined,
  targetCalories: undefined,
  dietPlan: '',
  exercisePlan: '',
  lifestyleTips: '',
  source: 'admin-manual',
});

const optimizeModalOpen = ref(false);
const selectedOptimizeId = ref<number | null>(null);
const optimizeForm = reactive<any>({
  dietPlan: '',
  exercisePlan: '',
  lifestyleTips: '',
  coachNote: '',
});

const load = async () => {
  loading.value = true;
  try {
    const res = await listCoachPlans(
      query.status,
      query.userId ? Number(query.userId) : undefined,
      pagination.current,
      pagination.pageSize
    );

    let records = res.data?.records || [];
    if (query.keyword) {
      const kw = query.keyword.toLowerCase();
      records = records.filter((item: any) => String(item.userNickname || '').toLowerCase().includes(kw));
    }

    rows.value = records;
    pagination.total = query.keyword ? records.length : (res.data?.total || 0);
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
  query.status = undefined;
  query.userId = '';
  query.keyword = '';
  pagination.current = 1;
  load();
};

const onTableChange = (p: any) => {
  pagination.current = p.current;
  pagination.pageSize = p.pageSize;
  load();
};

const openEditModal = (row: any | null) => {
  editing.value = row;
  if (row) {
    Object.assign(editForm, {
      id: row.id,
      userId: row.userId,
      targetCalories: row.targetCalories,
      dietPlan: row.dietPlan || '',
      exercisePlan: row.exercisePlan || '',
      lifestyleTips: row.lifestyleTips || '',
      source: row.status === 'coached' ? 'coach-optimize' : 'admin-manual',
    });
  } else {
    Object.assign(editForm, {
      id: undefined,
      userId: undefined,
      targetCalories: undefined,
      dietPlan: '',
      exercisePlan: '',
      lifestyleTips: '',
      source: 'admin-manual',
    });
  }
  editModalOpen.value = true;
};

const submitEdit = async () => {
  if (!editForm.userId) {
    message.warning('请输入用户ID');
    return;
  }
  saving.value = true;
  try {
    const payload = {
      id: editForm.id,
      userId: Number(editForm.userId),
      targetCalories: editForm.targetCalories,
      dietPlan: String(editForm.dietPlan || '').trim() || undefined,
      exercisePlan: String(editForm.exercisePlan || '').trim() || undefined,
      lifestyleTips: String(editForm.lifestyleTips || '').trim() || undefined,
      source: editForm.source,
    };

    if (editing.value) {
      await updateAdminPlan(payload);
      message.success('更新成功');
    } else {
      await addAdminPlan(payload);
      message.success('新增成功');
    }
    editModalOpen.value = false;
    load();
  } catch (error: any) {
    message.error(error?.message || '保存失败');
  } finally {
    saving.value = false;
  }
};

const doDelete = async (row: any) => {
  try {
    await deleteAdminPlan(row.id);
    message.success('删除成功');
    load();
  } catch (error: any) {
    message.error(error?.message || '删除失败');
  }
};

const openOptimize = (row: any) => {
  selectedOptimizeId.value = row.id;
  optimizeForm.dietPlan = row.dietPlan || '';
  optimizeForm.exercisePlan = row.exercisePlan || '';
  optimizeForm.lifestyleTips = row.lifestyleTips || '';
  optimizeForm.coachNote = '';
  optimizeModalOpen.value = true;
};

const submitOptimize = async () => {
  if (!selectedOptimizeId.value) return;
  optimizing.value = true;
  try {
    await optimizePlan(selectedOptimizeId.value, {
      dietPlan: optimizeForm.dietPlan,
      exercisePlan: optimizeForm.exercisePlan,
      lifestyleTips: optimizeForm.lifestyleTips,
      coachNote: optimizeForm.coachNote,
    });
    message.success('优化成功');
    optimizeModalOpen.value = false;
    load();
  } catch (error: any) {
    message.error(error?.message || '优化失败');
  } finally {
    optimizing.value = false;
  }
};

onMounted(() => {
  load();
});
</script>
