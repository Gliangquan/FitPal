<template>
  <div class="solar-term-management">
    <a-card title="节气管理" :bordered="false">
      <template #extra>
        <a-button type="primary" @click="showAddModal = true">
          <template #icon><plus-outlined /></template>
          新增节气专题
        </a-button>
      </template>

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
          <template v-else-if="column.key === 'status'">
            <a-tag :color="record.status === 'published' ? 'green' : 'orange'">
              {{ record.status === 'published' ? '已发布' : '草稿' }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'action'">
            <a-space>
              <a-button type="link" size="small" @click="handleEdit(record)">编辑</a-button>
              <a-button
                v-if="record.status === 'draft'"
                type="link"
                size="small"
                @click="handlePublish(record.id)"
              >
                发布
              </a-button>
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
      :title="editingTerm ? '编辑节气专题' : '新增节气专题'"
      width="800px"
      ok-text="保存"
      cancel-text="取消"
      @ok="handleSaveTerm"
      :confirm-loading="saveLoading"
    >
      <a-form :model="termForm" layout="vertical">
        <a-form-item label="节气名称" required>
          <a-select v-model:value="termForm.solarTermName" placeholder="选择节气">
            <a-select-option value="立春">立春</a-select-option>
            <a-select-option value="雨水">雨水</a-select-option>
            <a-select-option value="惊蛰">惊蛰</a-select-option>
            <a-select-option value="春分">春分</a-select-option>
            <a-select-option value="清明">清明</a-select-option>
            <a-select-option value="谷雨">谷雨</a-select-option>
            <a-select-option value="立夏">立夏</a-select-option>
            <a-select-option value="小满">小满</a-select-option>
            <a-select-option value="芒种">芒种</a-select-option>
            <a-select-option value="夏至">夏至</a-select-option>
            <a-select-option value="小暑">小暑</a-select-option>
            <a-select-option value="大暑">大暑</a-select-option>
            <a-select-option value="立秋">立秋</a-select-option>
            <a-select-option value="处暑">处暑</a-select-option>
            <a-select-option value="白露">白露</a-select-option>
            <a-select-option value="秋分">秋分</a-select-option>
            <a-select-option value="寒露">寒露</a-select-option>
            <a-select-option value="霜降">霜降</a-select-option>
            <a-select-option value="立冬">立冬</a-select-option>
            <a-select-option value="小雪">小雪</a-select-option>
            <a-select-option value="大雪">大雪</a-select-option>
            <a-select-option value="冬至">冬至</a-select-option>
            <a-select-option value="小寒">小寒</a-select-option>
            <a-select-option value="大寒">大寒</a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item label="专题标题" required>
          <a-input v-model:value="termForm.title" placeholder="如：春分养生减脂指南" />
        </a-form-item>

        <a-form-item label="专题描述" required>
          <a-textarea v-model:value="termForm.description" placeholder="专题详细描述" :rows="3" />
        </a-form-item>

        <a-divider>三日减脂食谱</a-divider>

        <a-form-item label="第一天食谱" required>
          <a-textarea v-model:value="termForm.day1Recipe" placeholder="输入第一天的食谱" :rows="3" />
        </a-form-item>

        <a-form-item label="第二天食谱" required>
          <a-textarea v-model:value="termForm.day2Recipe" placeholder="输入第二天的食谱" :rows="3" />
        </a-form-item>

        <a-form-item label="第三天食谱" required>
          <a-textarea v-model:value="termForm.day3Recipe" placeholder="输入第三天的食谱" :rows="3" />
        </a-form-item>

        <a-divider>节气特色运动指南</a-divider>

        <a-form-item label="运动指南" required>
          <a-textarea v-model:value="termForm.exerciseGuide" placeholder="输入节气特色运动指南" :rows="3" />
        </a-form-item>

        <a-divider>起居调整建议</a-divider>

        <a-form-item label="起居建议" required>
          <a-textarea v-model:value="termForm.lifestyleAdvice" placeholder="输入起居调整建议" :rows="3" />
        </a-form-item>

        <a-form-item label="养生知识" required>
          <a-textarea v-model:value="termForm.healthKnowledge" placeholder="输入传统养生知识" :rows="3" />
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

        <a-form-item label="发布状态">
          <a-radio-group v-model:value="termForm.status">
            <a-radio value="draft">草稿</a-radio>
            <a-radio value="published">发布</a-radio>
          </a-radio-group>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { PlusOutlined } from '@ant-design/icons-vue';
import type { UploadProps } from 'ant-design-vue';
import {
  listSolarTermByPage,
  addSolarTerm,
  updateSolarTerm,
  deleteSolarTerm,
  publishSolarTerm,
  uploadFile,
  resolveFilePreviewUrl,
} from '../../api';

const loading = ref(false);
const saveLoading = ref(false);
const showAddModal = ref(false);
const editingTerm = ref(null);

const columns = [
  {
    title: '封面图片',
    dataIndex: 'coverImage',
    key: 'coverImage',
    width: 100,
  },
  {
    title: '节气名称',
    dataIndex: 'solarTermName',
    key: 'solarTermName',
  },
  {
    title: '专题标题',
    dataIndex: 'title',
    key: 'title',
  },
  {
    title: '发布状态',
    dataIndex: 'status',
    key: 'status',
  },
  {
    title: '创建时间',
    dataIndex: 'createdAt',
    key: 'createdAt',
  },
  {
    title: '更新时间',
    dataIndex: 'updatedAt',
    key: 'updatedAt',
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

const termForm = reactive({
  solarTermName: '',
  title: '',
  description: '',
  day1Recipe: '',
  day2Recipe: '',
  day3Recipe: '',
  exerciseGuide: '',
  lifestyleAdvice: '',
  healthKnowledge: '',
  coverImage: '',
  status: 'draft',
});

const coverImageList = ref<UploadProps['fileList']>([]);

const fetchSolarTerms = async () => {
  loading.value = true;
  try {
    const res = await listSolarTermByPage({
      current: pagination.current,
      pageSize: pagination.pageSize,
    });
    if (res.data) {
      tableData.value = res.data.records || [];
      pagination.total = res.data.total || 0;
    }
  } catch (error) {
    message.error('获取节气专题失败');
  } finally {
    loading.value = false;
  }
};

const handleTableChange = (pag) => {
  pagination.current = pag.current;
  pagination.pageSize = pag.pageSize;
  fetchSolarTerms();
};

const handleEdit = (record) => {
  editingTerm.value = record;
  Object.assign(termForm, record);
  
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
    await deleteSolarTerm(id);
    message.success('删除成功');
    fetchSolarTerms();
  } catch (error) {
    message.error('删除失败');
  }
};

const handlePublish = async (id) => {
  try {
    await publishSolarTerm(id);
    message.success('发布成功');
    fetchSolarTerms();
  } catch (error) {
    message.error('发布失败');
  }
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
    termForm.coverImage = res.data || '';
    
    coverImageList.value = [{
      uid: '-1',
      name: file.name,
      status: 'done',
      url: resolveFilePreviewUrl(termForm.coverImage),
    }];
    
    message.success('封面上传成功');
  } catch (error: any) {
    message.error(error?.message || '封面上传失败');
  }
  return false;
};

const handleCoverRemove = () => {
  termForm.coverImage = '';
  coverImageList.value = [];
};

const handleSaveTerm = async () => {
  if (
    !termForm.solarTermName ||
    !termForm.title ||
    !termForm.description ||
    !termForm.day1Recipe ||
    !termForm.day2Recipe ||
    !termForm.day3Recipe ||
    !termForm.exerciseGuide ||
    !termForm.lifestyleAdvice ||
    !termForm.healthKnowledge
  ) {
    message.error('请填写所有必填项');
    return;
  }

  saveLoading.value = true;
  try {
    if (editingTerm.value) {
      await updateSolarTerm({
        id: editingTerm.value.id,
        ...termForm,
      });
      message.success('更新成功');
    } else {
      await addSolarTerm(termForm);
      message.success('新增成功');
    }
    showAddModal.value = false;
    editingTerm.value = null;
    Object.assign(termForm, {
      solarTermName: '',
      title: '',
      description: '',
      day1Recipe: '',
      day2Recipe: '',
      day3Recipe: '',
      exerciseGuide: '',
      lifestyleAdvice: '',
      healthKnowledge: '',
      coverImage: '',
      status: 'draft',
    });
    coverImageList.value = [];
    fetchSolarTerms();
  } catch (error) {
    message.error('保存失败');
  } finally {
    saveLoading.value = false;
  }
};

onMounted(() => {
  fetchSolarTerms();
});
</script>

<style scoped>
.solar-term-management {
  padding: 0;
}
</style>
