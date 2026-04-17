<template>
  <a-card title="教练审核" :bordered="false">
    <a-space style="margin-bottom: 12px" wrap>
      <a-select v-model:value="query.status" allow-clear placeholder="状态" style="width: 180px">
        <a-select-option value="pending">待审核</a-select-option>
        <a-select-option value="approved">已通过</a-select-option>
        <a-select-option value="rejected">已驳回</a-select-option>
      </a-select>
      <a-input v-model:value="query.keyword" placeholder="姓名/证书号" allow-clear style="width: 220px" />
      <a-button type="primary" @click="handleSearch">查询</a-button>
      <a-button @click="resetSearch">重置</a-button>
      <a-divider type="vertical" />
      <a-button @click="openModal(null)">新增</a-button>
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
          <a-tag :color="statusColor(record.status)">{{ statusLabel(record.status) }}</a-tag>
        </template>
        <template v-if="column.key === 'action'">
          <a-space>
            <a-button size="small" @click="openModal(record)">编辑</a-button>
            <a-popconfirm title="确认删除该记录？" @confirm="doDelete(record)">
              <a-button size="small" danger>删除</a-button>
            </a-popconfirm>
            <a-button size="small" @click="review(record, 'approve')">通过</a-button>
            <a-button size="small" danger @click="review(record, 'reject')">驳回</a-button>
            <a-button size="small" @click="review(record, 'reopen')">重开</a-button>
          </a-space>
        </template>
      </template>
    </a-table>

    <a-modal v-model:open="modalOpen" :title="editing ? '编辑教练申请' : '新增教练申请'" @ok="submit" :confirm-loading="saving">
      <a-form layout="vertical">
        <a-form-item label="用户ID" required>
          <a-input-number v-model:value="form.userId" :min="1" style="width: 100%" />
        </a-form-item>
        <a-form-item label="姓名" required>
          <a-input v-model:value="form.realName" />
        </a-form-item>
        <a-form-item label="证书类型" required>
          <a-input v-model:value="form.certificateType" />
        </a-form-item>
        <a-form-item label="证书编号" required>
          <a-input v-model:value="form.certificateNo" />
        </a-form-item>
        <a-form-item label="擅长方向">
          <a-input v-model:value="form.specialties" />
        </a-form-item>
        <a-form-item label="介绍">
          <a-textarea v-model:value="form.introduction" :rows="3" />
        </a-form-item>
        <a-form-item label="状态">
          <a-select v-model:value="form.status">
            <a-select-option value="pending">待审核</a-select-option>
            <a-select-option value="approved">已通过</a-select-option>
            <a-select-option value="rejected">已驳回</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="驳回原因" v-if="form.status === 'rejected'">
          <a-textarea v-model:value="form.rejectReason" :rows="2" />
        </a-form-item>
      </a-form>
    </a-modal>
  </a-card>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { message } from 'ant-design-vue';
import {
  addCoachApplication,
  deleteCoachApplication,
  listCoachApplications,
  reviewCoachApplication,
  updateCoachApplication,
} from '../../api';

const loading = ref(false);
const saving = ref(false);
const rows = ref<any[]>([]);

const query = reactive<any>({
  status: undefined,
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
  { title: '姓名', dataIndex: 'realName', key: 'realName', width: 140 },
  { title: '证书类型', dataIndex: 'certificateType', key: 'certificateType', width: 160 },
  { title: '证书编号', dataIndex: 'certificateNo', key: 'certificateNo' },
  { title: '状态', dataIndex: 'status', key: 'status', width: 120 },
  { title: '提交时间', dataIndex: 'createTime', key: 'createTime', width: 180 },
  { title: '操作', key: 'action', width: 360 },
];

const statusLabelMap: Record<string, string> = {
  pending: '待审核',
  approved: '已通过',
  rejected: '已驳回',
};

const statusLabel = (status?: string) => statusLabelMap[status || ''] || status || '-';

const statusColor = (status: string) => {
  if (status === 'approved') return 'success';
  if (status === 'rejected') return 'error';
  return 'processing';
};

const modalOpen = ref(false);
const editing = ref<any>(null);
const form = reactive<any>({
  id: undefined,
  userId: undefined,
  realName: '',
  certificateType: '',
  certificateNo: '',
  specialties: '',
  introduction: '',
  status: 'pending',
  rejectReason: '',
});

const load = async () => {
  loading.value = true;
  try {
    const res = await listCoachApplications(query.status, pagination.current, pagination.pageSize);
    let records = res.data?.records || [];
    if (query.keyword) {
      const kw = query.keyword.toLowerCase();
      records = records.filter((item: any) =>
        String(item.realName || '').toLowerCase().includes(kw)
        || String(item.certificateNo || '').toLowerCase().includes(kw)
      );
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
  query.keyword = '';
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
      userId: row.userId,
      realName: row.realName,
      certificateType: row.certificateType,
      certificateNo: row.certificateNo,
      specialties: row.specialties || '',
      introduction: row.introduction || '',
      status: row.status || 'pending',
      rejectReason: row.rejectReason || '',
    });
  } else {
    Object.assign(form, {
      id: undefined,
      userId: undefined,
      realName: '',
      certificateType: '',
      certificateNo: '',
      specialties: '',
      introduction: '',
      status: 'pending',
      rejectReason: '',
    });
  }
  modalOpen.value = true;
};

const submit = async () => {
  if (!form.userId || !String(form.realName || '').trim() || !String(form.certificateType || '').trim() || !String(form.certificateNo || '').trim()) {
    message.warning('请完整填写必填项');
    return;
  }
  saving.value = true;
  try {
    const payload = {
      id: form.id,
      userId: Number(form.userId),
      realName: String(form.realName || '').trim(),
      certificateType: String(form.certificateType || '').trim(),
      certificateNo: String(form.certificateNo || '').trim(),
      specialties: String(form.specialties || '').trim() || undefined,
      introduction: String(form.introduction || '').trim() || undefined,
      status: form.status,
      rejectReason: form.status === 'rejected' ? (String(form.rejectReason || '').trim() || '资料不符合要求') : undefined,
    };

    if (editing.value) {
      await updateCoachApplication(payload);
      message.success('更新成功');
    } else {
      await addCoachApplication(payload);
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
    await deleteCoachApplication(row.id);
    message.success('删除成功');
    load();
  } catch (error: any) {
    message.error(error?.message || '删除失败');
  }
};

const review = async (row: any, action: 'approve' | 'reject' | 'reopen') => {
  try {
    let reason = '';
    if (action === 'reject') {
      reason = window.prompt('请输入驳回原因', '资质材料不符合要求') || '资质材料不符合要求';
    }
    await reviewCoachApplication(row.id, { action, reason });
    message.success(`操作成功：${action}`);
    load();
  } catch (error: any) {
    message.error(error?.message || '审核失败');
  }
};

onMounted(() => {
  load();
});
</script>
