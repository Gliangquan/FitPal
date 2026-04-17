<template>
  <a-card title="内容审核" :bordered="false">
    <a-space style="margin-bottom: 12px" wrap>
      <a-select v-model:value="query.status" allow-clear placeholder="状态" style="width: 180px">
        <a-select-option value="draft">草稿</a-select-option>
        <a-select-option value="pending">待审核</a-select-option>
        <a-select-option value="published">已发布</a-select-option>
        <a-select-option value="rejected">已驳回</a-select-option>
      </a-select>
      <a-input v-model:value="query.keyword" placeholder="标题关键词" allow-clear style="width: 220px" />
      <a-input v-model:value="query.stageTag" placeholder="阶段标签" allow-clear style="width: 160px" />
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
        <template v-if="column.key === 'publishStatus'">
          <a-tag :color="statusColor(record.publishStatus)">{{ statusLabel(record.publishStatus) }}</a-tag>
        </template>
        <template v-if="column.key === 'action'">
          <a-space>
            <a-button size="small" @click="openModal(record)">编辑</a-button>
            <a-popconfirm title="确认删除该内容？" @confirm="doDelete(record)">
              <a-button size="small" danger>删除</a-button>
            </a-popconfirm>
            <a-button size="small" @click="review(record, 'publish')">发布</a-button>
            <a-button size="small" danger @click="review(record, 'reject')">驳回</a-button>
            <a-button size="small" @click="review(record, 'reset')">重置</a-button>
          </a-space>
        </template>
      </template>
    </a-table>

    <a-modal v-model:open="modalOpen" :title="editing ? '编辑内容' : '新增内容'" @ok="submit" :confirm-loading="saving" width="760px">
      <a-form layout="vertical">
        <a-row :gutter="12">
          <a-col :span="12">
            <a-form-item label="标题" required>
              <a-input v-model:value="form.title" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="内容类型">
              <a-select v-model:value="form.contentType">
                <a-select-option value="article">文章</a-select-option>
                <a-select-option value="video">视频</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="12">
          <a-col :span="12">
            <a-form-item label="阶段标签">
              <a-input v-model:value="form.stageTag" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="体型标签">
              <a-input v-model:value="form.bodyTag" />
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="摘要">
          <a-textarea v-model:value="form.summary" :rows="2" />
        </a-form-item>
        <a-form-item label="内容链接">
          <a-input v-model:value="form.contentUrl" />
        </a-form-item>
        <a-form-item label="内容正文">
          <a-textarea v-model:value="form.contentBody" :rows="4" />
        </a-form-item>
        <a-form-item label="标签（逗号分隔）">
          <a-input v-model:value="form.tags" />
        </a-form-item>
        <a-form-item label="发布状态">
          <a-select v-model:value="form.publishStatus">
            <a-select-option value="draft">草稿</a-select-option>
            <a-select-option value="pending">待审核</a-select-option>
            <a-select-option value="published">已发布</a-select-option>
            <a-select-option value="rejected">已驳回</a-select-option>
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>
  </a-card>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { message } from 'ant-design-vue';
import {
  addAdminContent,
  deleteAdminContent,
  listAdminContents,
  reviewContent,
  updateAdminContent,
} from '../../api';

const loading = ref(false);
const saving = ref(false);
const rows = ref<any[]>([]);

const query = reactive<any>({
  status: undefined,
  keyword: '',
  stageTag: '',
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
  { title: '标题', dataIndex: 'title', key: 'title' },
  { title: '类型', dataIndex: 'contentType', key: 'contentType', width: 120 },
  { title: '阶段标签', dataIndex: 'stageTag', key: 'stageTag', width: 120 },
  { title: '状态', dataIndex: 'publishStatus', key: 'publishStatus', width: 120 },
  { title: '摘要', dataIndex: 'summary', key: 'summary' },
  { title: '创建时间', dataIndex: 'createTime', key: 'createTime', width: 180 },
  { title: '操作', key: 'action', width: 360 },
];

const statusLabelMap: Record<string, string> = {
  draft: '草稿',
  pending: '待审核',
  published: '已发布',
  rejected: '已驳回',
};

const statusLabel = (status?: string) => statusLabelMap[status || ''] || status || '-';

const statusColor = (status: string) => {
  if (status === 'published') return 'success';
  if (status === 'rejected') return 'error';
  if (status === 'pending') return 'warning';
  return 'processing';
};

const modalOpen = ref(false);
const editing = ref<any>(null);
const form = reactive<any>({
  id: undefined,
  title: '',
  contentType: 'article',
  stageTag: '',
  bodyTag: '',
  summary: '',
  contentUrl: '',
  contentBody: '',
  tags: '',
  publishStatus: 'draft',
});

const load = async () => {
  loading.value = true;
  try {
    const res = await listAdminContents(query.status, pagination.current, pagination.pageSize);
    let records = res.data?.records || [];
    if (query.keyword) {
      const kw = query.keyword.toLowerCase();
      records = records.filter((item: any) => String(item.title || '').toLowerCase().includes(kw));
    }
    if (query.stageTag) {
      const stage = query.stageTag.toLowerCase();
      records = records.filter((item: any) => String(item.stageTag || '').toLowerCase().includes(stage));
    }
    rows.value = records;
    pagination.total = query.keyword || query.stageTag ? records.length : (res.data?.total || 0);
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
  query.stageTag = '';
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
      title: row.title || '',
      contentType: row.contentType || 'article',
      stageTag: row.stageTag || '',
      bodyTag: row.bodyTag || '',
      summary: row.summary || '',
      contentUrl: row.contentUrl || '',
      contentBody: row.contentBody || '',
      tags: row.tags || '',
      publishStatus: row.publishStatus || 'draft',
    });
  } else {
    Object.assign(form, {
      id: undefined,
      title: '',
      contentType: 'article',
      stageTag: '',
      bodyTag: '',
      summary: '',
      contentUrl: '',
      contentBody: '',
      tags: '',
      publishStatus: 'draft',
    });
  }
  modalOpen.value = true;
};

const submit = async () => {
  if (!String(form.title || '').trim()) {
    message.warning('请输入标题');
    return;
  }
  saving.value = true;
  try {
    const payload = {
      id: form.id,
      title: String(form.title || '').trim(),
      contentType: form.contentType,
      stageTag: String(form.stageTag || '').trim() || undefined,
      bodyTag: String(form.bodyTag || '').trim() || undefined,
      summary: String(form.summary || '').trim() || undefined,
      contentUrl: String(form.contentUrl || '').trim() || undefined,
      contentBody: String(form.contentBody || '').trim() || undefined,
      tags: String(form.tags || '').trim() || undefined,
      publishStatus: form.publishStatus,
    };

    if (editing.value) {
      await updateAdminContent(payload);
      message.success('更新成功');
    } else {
      await addAdminContent(payload);
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
    await deleteAdminContent(row.id);
    message.success('删除成功');
    load();
  } catch (error: any) {
    message.error(error?.message || '删除失败');
  }
};

const review = async (row: any, action: 'publish' | 'reject' | 'reset') => {
  try {
    let reason = '';
    if (action === 'reject') {
      reason = window.prompt('请输入驳回原因', '内容不符合规范') || '内容不符合规范';
    }
    await reviewContent(row.id, { action, reason });
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
