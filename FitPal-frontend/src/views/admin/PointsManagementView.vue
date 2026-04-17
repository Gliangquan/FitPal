<template>
  <div class="points-management">
    <a-card title="积分管理" :bordered="false">
      <template #extra>
        <a-space>
          <a-button type="primary" @click="showAddModal = true">
            <template #icon><plus-outlined /></template>
            新增积分规则
          </a-button>
        </a-space>
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
          <template v-if="column.key === 'action'">
            <a-space>
              <a-button type="link" size="small" @click="handleEdit(record)">编辑</a-button>
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

    <!-- 用户积分查询 -->
    <a-card title="用户积分查询" :bordered="false" style="margin-top: 20px">
      <a-space style="margin-bottom: 16px">
        <a-input-search
          v-model:value="searchUserId"
          placeholder="搜索用户ID或用户名"
          style="width: 200px"
          @search="handleSearchUser"
        />
        <a-button type="primary" @click="handleSearchUser">查询</a-button>
      </a-space>

      <a-table
        :columns="userPointsColumns"
        :data-source="userPointsData"
        :loading="userPointsLoading"
        :pagination="userPointsPagination"
        @change="handleUserPointsTableChange"
        rowKey="id"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <a-button type="link" size="small" @click="handleAdjustPoints(record)">调整积分</a-button>
            </a-space>
          </template>
        </template>
      </a-table>
    </a-card>

    <!-- 新增/编辑规则模态框 -->
    <a-modal
      v-model:visible="showAddModal"
      :title="editingRule ? '编辑积分规则' : '新增积分规则'"
      ok-text="保存"
      cancel-text="取消"
      @ok="handleSaveRule"
      :confirm-loading="saveLoading"
    >
      <a-form :model="ruleForm" layout="vertical">
        <a-form-item label="规则名称" required>
          <a-input v-model:value="ruleForm.ruleName" placeholder="如：每周3次运动记录" />
        </a-form-item>
        <a-form-item label="规则描述" required>
          <a-textarea v-model:value="ruleForm.ruleDescription" placeholder="规则详细描述" />
        </a-form-item>
        <a-form-item label="积分数量" required>
          <a-input-number v-model:value="ruleForm.points" :min="0" />
        </a-form-item>
        <a-form-item label="规则类型" required>
          <a-select v-model:value="ruleForm.ruleType" placeholder="选择规则类型">
            <a-select-option value="task">任务完成</a-select-option>
            <a-select-option value="achievement">成就解锁</a-select-option>
            <a-select-option value="social">社交互动</a-select-option>
            <a-select-option value="other">其他</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="是否启用">
          <a-switch v-model:checked="ruleForm.enabled" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 调整积分模态框 -->
    <a-modal
      v-model:visible="showAdjustModal"
      title="调整用户积分"
      ok-text="确认"
      cancel-text="取消"
      @ok="handleConfirmAdjust"
      :confirm-loading="adjustLoading"
    >
      <a-form :model="adjustForm" layout="vertical">
        <a-form-item label="用户">
          <span>{{ adjustForm.userName }}</span>
        </a-form-item>
        <a-form-item label="当前积分">
          <span>{{ adjustForm.currentPoints }}</span>
        </a-form-item>
        <a-form-item label="调整数量" required>
          <a-input-number v-model:value="adjustForm.adjustPoints" placeholder="正数为增加，负数为减少" />
        </a-form-item>
        <a-form-item label="调整原因" required>
          <a-textarea v-model:value="adjustForm.reason" placeholder="请说明调整原因" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { PlusOutlined } from '@ant-design/icons-vue';
import {
  listPointsRuleByPage,
  addPointsRule,
  updatePointsRule,
  deletePointsRule,
  listUserPointsByPage,
  adjustUserPoints,
} from '../../api';

const loading = ref(false);
const userPointsLoading = ref(false);
const saveLoading = ref(false);
const adjustLoading = ref(false);
const showAddModal = ref(false);
const showAdjustModal = ref(false);
const searchUserId = ref('');
const editingRule = ref(null);

const columns = [
  {
    title: '规则名称',
    dataIndex: 'ruleName',
    key: 'ruleName',
  },
  {
    title: '规则类型',
    dataIndex: 'ruleType',
    key: 'ruleType',
  },
  {
    title: '积分数量',
    dataIndex: 'points',
    key: 'points',
  },
  {
    title: '状态',
    dataIndex: 'enabled',
    key: 'enabled',
    customRender: ({ text }) => (text ? '启用' : '禁用'),
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

const userPointsColumns = [
  {
    title: '用户ID',
    dataIndex: 'userId',
    key: 'userId',
  },
  {
    title: '用户名',
    dataIndex: 'userName',
    key: 'userName',
  },
  {
    title: '当前积分',
    dataIndex: 'totalPoints',
    key: 'totalPoints',
  },
  {
    title: '勋章数',
    dataIndex: 'medalCount',
    key: 'medalCount',
  },
  {
    title: '最后更新',
    dataIndex: 'updatedAt',
    key: 'updatedAt',
  },
  {
    title: '操作',
    key: 'action',
  },
];

const tableData = ref([]);
const userPointsData = ref([]);

const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
});

const userPointsPagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
});

const ruleForm = reactive({
  ruleName: '',
  ruleDescription: '',
  points: 0,
  ruleType: 'task',
  enabled: true,
});

const adjustForm = reactive({
  userId: 0,
  userName: '',
  currentPoints: 0,
  adjustPoints: 0,
  reason: '',
});

const fetchPointsRules = async () => {
  loading.value = true;
  try {
    const res = await listPointsRuleByPage({
      current: pagination.current,
      pageSize: pagination.pageSize,
    });
    if (res.data) {
      tableData.value = res.data.records || [];
      pagination.total = res.data.total || 0;
    }
  } catch (error) {
    message.error('获取积分规则失败');
  } finally {
    loading.value = false;
  }
};

const handleTableChange = (pag) => {
  pagination.current = pag.current;
  pagination.pageSize = pag.pageSize;
  fetchPointsRules();
};

const handleEdit = (record) => {
  editingRule.value = record;
  Object.assign(ruleForm, record);
  showAddModal.value = true;
};

const handleDelete = async (id) => {
  try {
    await deletePointsRule(id);
    message.success('删除成功');
    fetchPointsRules();
  } catch (error) {
    message.error('删除失败');
  }
};

const handleSaveRule = async () => {
  if (!ruleForm.ruleName || !ruleForm.ruleDescription) {
    message.error('请填写必填项');
    return;
  }

  saveLoading.value = true;
  try {
    if (editingRule.value) {
      await updatePointsRule({
        id: editingRule.value.id,
        ...ruleForm,
      });
      message.success('更新成功');
    } else {
      await addPointsRule(ruleForm);
      message.success('新增成功');
    }
    showAddModal.value = false;
    editingRule.value = null;
    Object.assign(ruleForm, {
      ruleName: '',
      ruleDescription: '',
      points: 0,
      ruleType: 'task',
      enabled: true,
    });
    fetchPointsRules();
  } catch (error) {
    message.error('保存失败');
  } finally {
    saveLoading.value = false;
  }
};

const handleSearchUser = async () => {
  if (!searchUserId.value) {
    message.warning('请输入用户ID或用户名');
    return;
  }

  userPointsLoading.value = true;
  try {
    const res = await listUserPointsByPage({
      userId: isNaN(Number(searchUserId.value)) ? undefined : Number(searchUserId.value),
      userName: isNaN(Number(searchUserId.value)) ? searchUserId.value : undefined,
      current: userPointsPagination.current,
      pageSize: userPointsPagination.pageSize,
    });
    if (res.data) {
      userPointsData.value = res.data.records || [];
      userPointsPagination.total = res.data.total || 0;
    }
  } catch (error) {
    message.error('查询失败');
  } finally {
    userPointsLoading.value = false;
  }
};

const handleUserPointsTableChange = (pag) => {
  userPointsPagination.current = pag.current;
  userPointsPagination.pageSize = pag.pageSize;
  handleSearchUser();
};

const handleAdjustPoints = (record) => {
  adjustForm.userId = record.userId;
  adjustForm.userName = record.userName;
  adjustForm.currentPoints = record.totalPoints;
  adjustForm.adjustPoints = 0;
  adjustForm.reason = '';
  showAdjustModal.value = true;
};

const handleConfirmAdjust = async () => {
  if (!adjustForm.adjustPoints || !adjustForm.reason) {
    message.error('请填写调整数量和原因');
    return;
  }

  adjustLoading.value = true;
  try {
    await adjustUserPoints({
      userId: adjustForm.userId,
      adjustPoints: adjustForm.adjustPoints,
      reason: adjustForm.reason,
    });
    message.success('积分调整成功');
    showAdjustModal.value = false;
    handleSearchUser();
  } catch (error) {
    message.error('调整失败');
  } finally {
    adjustLoading.value = false;
  }
};

onMounted(() => {
  fetchPointsRules();
});
</script>

<style scoped>
.points-management {
  padding: 0;
}
</style>
