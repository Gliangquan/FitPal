<template>
  <a-card title="社区内容审核" :bordered="false">
    <a-space style="margin-bottom: 12px" wrap>
      <a-select v-model:value="query.status" allow-clear placeholder="状态" style="width: 160px">
        <a-select-option value="published">已发布</a-select-option>
        <a-select-option value="hidden">已隐藏</a-select-option>
        <a-select-option value="rejected">已驳回</a-select-option>
      </a-select>
      <a-select v-model:value="query.category" allow-clear placeholder="分类" style="width: 160px">
        <a-select-option value="weight-loss">减脂心得</a-select-option>
        <a-select-option value="diet">饮食分享</a-select-option>
        <a-select-option value="workout">运动打卡</a-select-option>
        <a-select-option value="achievement">成果展示</a-select-option>
        <a-select-option value="help">问题求助</a-select-option>
        <a-select-option value="mindset">心态分享</a-select-option>
      </a-select>
      <a-input v-model:value="query.keyword" placeholder="标题/内容关键词" allow-clear style="width: 220px" />
      <a-button type="primary" @click="handleSearch">查询</a-button>
      <a-button @click="resetSearch">重置</a-button>
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
        <template v-if="column.key === 'imageUrls'">
          <a-image-preview-group v-if="record.imageList && record.imageList.length > 0">
            <a-image
              v-for="(url, index) in record.imageList.slice(0, 3)"
              :key="index"
              :width="30"
              :height="30"
              :src="resolveFilePreviewUrl(url)"
              style="object-fit: cover; border-radius: 4px; margin-right: 4px;"
            />
            <span v-if="record.imageList.length > 3" style="color: #999; font-size: 12px;">
              +{{ record.imageList.length - 3 }}
            </span>
          </a-image-preview-group>
          <span v-else style="color: #999;">无图片</span>
        </template>
        <template v-else-if="column.key === 'category'">
          <a-tag>{{ categoryLabel(record.category) }}</a-tag>
        </template>
        <template v-if="column.key === 'status'">
          <a-tag :color="statusColor(record.status)">{{ statusLabel(record.status) }}</a-tag>
        </template>
        <template v-if="column.key === 'action'">
          <a-space>
            <a-button size="small" @click="review(record, 'publish')">通过</a-button>
            <a-button size="small" @click="review(record, 'hide')">隐藏</a-button>
            <a-button size="small" danger @click="review(record, 'reject')">驳回</a-button>
          </a-space>
        </template>
      </template>
    </a-table>
  </a-card>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { message } from 'ant-design-vue';
import { listAdminCommunityPosts, reviewCommunityPost, resolveFilePreviewUrl } from '../../api';

const loading = ref(false);
const rows = ref<any[]>([]);

const query = reactive<any>({
  status: undefined,
  category: undefined,
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
  { title: '图片', dataIndex: 'imageUrls', key: 'imageUrls', width: 120 },
  { title: '标题', dataIndex: 'title', key: 'title' },
  { title: '作者', dataIndex: 'authorName', key: 'authorName', width: 140 },
  { title: '分类', dataIndex: 'category', key: 'category', width: 120 },
  { title: '点赞', dataIndex: 'likeCount', key: 'likeCount', width: 90 },
  { title: '评论', dataIndex: 'commentCount', key: 'commentCount', width: 90 },
  { title: '浏览', dataIndex: 'viewCount', key: 'viewCount', width: 90 },
  { title: '状态', dataIndex: 'status', key: 'status', width: 120 },
  { title: '创建时间', dataIndex: 'createTime', key: 'createTime', width: 180 },
  { title: '操作', key: 'action', width: 220 },
];

const categoryMap: Record<string, string> = {
  'weight-loss': '减脂心得',
  diet: '饮食分享',
  workout: '运动打卡',
  achievement: '成果展示',
  help: '问题求助',
  mindset: '心态分享',
};

const categoryLabel = (value?: string) => categoryMap[value || ''] || value || '-';

const statusMap: Record<string, string> = {
  published: '已发布',
  hidden: '已隐藏',
  rejected: '已驳回',
};

const statusLabel = (value?: string) => statusMap[value || ''] || value || '-';

const statusColor = (value?: string) => {
  if (value === 'published') return 'success';
  if (value === 'rejected') return 'error';
  return 'default';
};

const load = async () => {
  loading.value = true;
  try {
    const res = await listAdminCommunityPosts(
      query.status,
      query.category,
      query.keyword || undefined,
      pagination.current,
      pagination.pageSize
    );
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
  query.status = undefined;
  query.category = undefined;
  query.keyword = '';
  pagination.current = 1;
  load();
};

const onTableChange = (p: any) => {
  pagination.current = p.current;
  pagination.pageSize = p.pageSize;
  load();
};

const review = async (row: any, action: 'publish' | 'hide' | 'reject') => {
  try {
    let reason = '';
    if (action === 'reject') {
      reason = window.prompt('请输入驳回原因', '内容不符合社区规范') || '内容不符合社区规范';
    }
    await reviewCommunityPost(row.id, { action, reason });
    message.success('操作成功');
    load();
  } catch (error: any) {
    message.error(error?.message || '操作失败');
  }
};

onMounted(() => {
  load();
});
</script>
