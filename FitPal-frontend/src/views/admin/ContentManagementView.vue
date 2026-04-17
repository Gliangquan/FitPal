<template>
  <div class="content-management">
    <a-card title="内容管理" :bordered="false">
      <template #extra>
        <a-space>
          <a-button type="primary" @click="showAddModal = true">
            <template #icon><plus-outlined /></template>
            新增内容
          </a-button>
        </a-space>
      </template>

      <a-space style="margin-bottom: 16px">
        <a-select v-model:value="filterType" style="width: 150px" placeholder="选择内容类型" @change="handleSearch">
          <a-select-option value="">全部类型</a-select-option>
          <a-select-option value="article">科普文章</a-select-option>
          <a-select-option value="video">视频课程</a-select-option>
          <a-select-option value="recipe">食谱</a-select-option>
          <a-select-option value="exercise">运动指南</a-select-option>
        </a-select>
        <a-select v-model:value="filterStatus" style="width: 150px" placeholder="选择发布状态" @change="handleSearch">
          <a-select-option value="">全部状态</a-select-option>
          <a-select-option value="published">已发布</a-select-option>
          <a-select-option value="draft">草稿</a-select-option>
          <a-select-option value="archived">已归档</a-select-option>
        </a-select>
        <a-input-search
          v-model:value="searchKeyword"
          placeholder="搜索内容标题"
          style="width: 200px"
          @search="handleSearch"
        />
      </a-space>

      <a-table
        :columns="columns"
        :data-source="tableData"
        :loading="loading"
        :pagination="pagination"
        @change="handleTableChange"
        rowKey="id"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'coverImage'">
            <a-image
              v-if="record.coverImage"
              :width="60"
              :height="60"
              :src="resolveFilePreviewUrl(record.coverImage)"
              :preview="true"
              style="object-fit: cover; border-radius: 4px;"
            />
            <span v-else style="color: #999;">无封面</span>
          </template>
          <template v-else-if="column.key === 'contentType'">
            <a-tag :color="getTypeColor(record.contentType)">
              {{ getTypeName(record.contentType) }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'targetAudience'">
            <a-tag :color="getAudienceColor(record.targetAudience)">
              {{ getAudienceName(record.targetAudience) }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'status'">
            <a-tag :color="getStatusColor(record.status)">
              {{ getStatusName(record.status) }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'action'">
            <a-space>
              <a-button type="link" size="small" @click="handleEdit(record)">编辑</a-button>
              <a-button type="link" size="small" @click="handlePreview(record)">预览</a-button>
              <a-popconfirm
                title="确定删除?"
                ok-text="确定"
                cancel-text="取消"
                @confirm="handleDelete(record.id)"
              >
                <a-button type="link" danger size="small">删除</a-button>
              </a-popconfirm>
            </a-space>
          </template>
        </template>
      </a-table>
    </a-card>

    <!-- 新增/编辑模态框 -->
    <a-modal
      v-model:visible="showAddModal"
      :title="editingContent ? '编辑内容' : '新增内容'"
      width="900px"
      ok-text="保存"
      cancel-text="取消"
      @ok="handleSaveContent"
      :confirm-loading="saveLoading"
    >
      <a-form :model="contentForm" layout="vertical">
        <a-form-item label="内容类型" required>
          <a-select v-model:value="contentForm.contentType" placeholder="选择内容类型">
            <a-select-option value="article">科普文章</a-select-option>
            <a-select-option value="video">视频课程</a-select-option>
            <a-select-option value="recipe">食谱</a-select-option>
            <a-select-option value="exercise">运动指南</a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item label="内容标题" required>
          <a-input v-model:value="contentForm.title" placeholder="输入内容标题" />
        </a-form-item>

        <a-form-item label="内容描述" required>
          <a-textarea v-model:value="contentForm.description" placeholder="输入内容描述" :rows="3" />
        </a-form-item>

        <a-form-item label="内容详情" required>
          <a-textarea v-model:value="contentForm.content" placeholder="输入详细内容" :rows="6" />
        </a-form-item>

        <a-form-item label="封面图片">
          <a-upload
            list-type="picture-card"
            :file-list="coverImageList"
            :before-upload="handleCoverUpload"
            @remove="handleCoverRemove"
            :max-count="1"
            accept="image/*"
          >
            <div v-if="coverImageList.length < 1">
              <plus-outlined />
              <div style="margin-top: 8px">上传封面</div>
            </div>
          </a-upload>
          <div style="color: #999; font-size: 12px; margin-top: 8px">
            支持 jpg/png/webp，建议尺寸 800x600，大小不超过 5MB
          </div>
        </a-form-item>

        <a-form-item label="目标用户" required>
          <a-select v-model:value="contentForm.targetAudience" placeholder="选择目标用户">
            <a-select-option value="all">全部用户</a-select-option>
            <a-select-option value="newbie">新手用户</a-select-option>
            <a-select-option value="office">办公室人群</a-select-option>
            <a-select-option value="beginner">初级用户</a-select-option>
            <a-select-option value="intermediate">中级用户</a-select-option>
            <a-select-option value="advanced">高级用户</a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item label="标签">
          <a-select v-model:value="contentForm.tags" mode="tags" placeholder="输入标签，按Enter添加" />
        </a-form-item>

        <a-form-item label="发布状态">
          <a-radio-group v-model:value="contentForm.status">
            <a-radio value="draft">草稿</a-radio>
            <a-radio value="published">发布</a-radio>
            <a-radio value="archived">归档</a-radio>
          </a-radio-group>
        </a-form-item>

        <a-form-item label="推荐指数">
          <a-rate v-model:value="contentForm.recommendScore" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 预览模态框 -->
    <a-modal
      v-model:visible="showPreviewModal"
      title="内容预览"
      width="800px"
      :footer="null"
    >
      <div class="preview-content">
        <h2>{{ previewContent.title }}</h2>
        <p><strong>类型：</strong> {{ getTypeName(previewContent.contentType) }}</p>
        <p><strong>描述：</strong> {{ previewContent.description }}</p>
        <div style="margin-top: 20px; padding: 20px; background: #f5f5f5; border-radius: 4px">
          <p>{{ previewContent.content }}</p>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { PlusOutlined } from '@ant-design/icons-vue';
import type { UploadProps } from 'ant-design-vue';
import {
  listContentByPage,
  addContent,
  updateContent,
  deleteContent,
  uploadFile,
  resolveFilePreviewUrl,
} from '../../api';

const loading = ref(false);
const saveLoading = ref(false);
const showAddModal = ref(false);
const showPreviewModal = ref(false);
const editingContent = ref(null);
const filterType = ref('');
const filterStatus = ref('');
const searchKeyword = ref('');
const previewContent = ref({});

const columns = [
  {
    title: '封面图片',
    dataIndex: 'coverImage',
    key: 'coverImage',
    width: 100,
  },
  {
    title: '内容标题',
    dataIndex: 'title',
    key: 'title',
  },
  {
    title: '内容类型',
    dataIndex: 'contentType',
    key: 'contentType',
  },
  {
    title: '目标用户',
    dataIndex: 'targetAudience',
    key: 'targetAudience',
  },
  {
    title: '发布状态',
    dataIndex: 'status',
    key: 'status',
  },
  {
    title: '推荐指数',
    dataIndex: 'recommendScore',
    key: 'recommendScore',
  },
  {
    title: '创建时间',
    dataIndex: 'createdAt',
    key: 'createdAt',
  },
  {
    title: '操作',
    key: 'action',
  },
];

const tableData = ref([]);

const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
});

const contentForm = reactive({
  contentType: 'article',
  title: '',
  description: '',
  content: '',
  targetAudience: 'all',
  tags: [],
  status: 'draft',
  recommendScore: 3,
  coverImage: '',
});

const coverImageList = ref<UploadProps['fileList']>([]);

const getTypeName = (type) => {
  const typeMap = {
    article: '科普文章',
    video: '视频课程',
    recipe: '食谱',
    exercise: '运动指南',
  };
  return typeMap[type] || type;
};

const getTypeColor = (type) => {
  const colorMap = {
    article: 'blue',
    video: 'red',
    recipe: 'green',
    exercise: 'orange',
  };
  return colorMap[type] || 'default';
};

const getStatusName = (status) => {
  const statusMap = {
    published: '已发布',
    draft: '草稿',
    archived: '已归档',
  };
  return statusMap[status] || status;
};

const getStatusColor = (status) => {
  const colorMap = {
    published: 'green',
    draft: 'orange',
    archived: 'gray',
  };
  return colorMap[status] || 'default';
};

const getAudienceName = (audience) => {
  const audienceMap = {
    all: '全部用户',
    newbie: '新手用户',
    office: '办公室人群',
    beginner: '初级用户',
    intermediate: '中级用户',
    advanced: '高级用户',
  };
  return audienceMap[audience] || audience;
};

const getAudienceColor = (audience) => {
  const colorMap = {
    all: 'purple',
    newbie: 'green',
    office: 'orange',
    beginner: 'cyan',
    intermediate: 'blue',
    advanced: 'gold',
  };
  return colorMap[audience] || 'default';
};

const handleCoverUpload = async (file: File) => {
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

  try {
    const res = await uploadFile(file, 'content_cover');
    contentForm.coverImage = res.data || '';
    
    coverImageList.value = [{
      uid: '-1',
      name: file.name,
      status: 'done',
      url: resolveFilePreviewUrl(contentForm.coverImage),
    }];
    
    message.success('封面上传成功');
  } catch (error: any) {
    message.error(error?.message || '封面上传失败');
  }
  return false;
};

const handleCoverRemove = () => {
  contentForm.coverImage = '';
  coverImageList.value = [];
};

const fetchContent = async () => {
  loading.value = true;
  try {
    const res = await listContentByPage({
      contentType: filterType.value || undefined,
      status: filterStatus.value || undefined,
      title: searchKeyword.value || undefined,
      current: pagination.current,
      pageSize: pagination.pageSize,
    });
    if (res.data) {
      tableData.value = res.data.records || [];
      pagination.total = res.data.total || 0;
    }
  } catch (error) {
    message.error('获取内容失败');
  } finally {
    loading.value = false;
  }
};

const handleTableChange = (pag) => {
  pagination.current = pag.current;
  pagination.pageSize = pag.pageSize;
  fetchContent();
};

const handleSearch = () => {
  pagination.current = 1;
  fetchContent();
};

const handleEdit = (record) => {
  editingContent.value = record;
  Object.assign(contentForm, record);
  
  // 加载封面图片
  if (record.coverImage) {
    coverImageList.value = [{
      uid: '-1',
      name: 'cover.jpg',
      status: 'done',
      url: resolveFilePreviewUrl(record.coverImage),
    }];
  } else {
    coverImageList.value = [];
  }
  
  showAddModal.value = true;
};

const handleDelete = async (id) => {
  try {
    await deleteContent(id);
    message.success('删除成功');
    fetchContent();
  } catch (error) {
    message.error('删除失败');
  }
};

const handlePreview = (record) => {
  previewContent.value = record;
  showPreviewModal.value = true;
};

const handleSaveContent = async () => {
  if (!contentForm.title || !contentForm.description || !contentForm.content) {
    message.error('请填写必填项');
    return;
  }

  saveLoading.value = true;
  try {
    if (editingContent.value) {
      await updateContent({
        id: editingContent.value.id,
        ...contentForm,
      });
      message.success('更新成功');
    } else {
      await addContent(contentForm);
      message.success('新增成功');
    }
    showAddModal.value = false;
    editingContent.value = null;
    Object.assign(contentForm, {
      contentType: 'article',
      title: '',
      description: '',
      content: '',
      targetAudience: 'all',
      tags: [],
      status: 'draft',
      recommendScore: 3,
      coverImage: '',
    });
    coverImageList.value = [];
    fetchContent();
  } catch (error) {
    message.error('保存失败');
  } finally {
    saveLoading.value = false;
  }
};

onMounted(() => {
  fetchContent();
});
</script>

<style scoped>
.content-management {
  padding: 0;
}

.preview-content {
  padding: 20px;
}

.preview-content h2 {
  margin-bottom: 20px;
}

.preview-content p {
  margin-bottom: 10px;
}
</style>
