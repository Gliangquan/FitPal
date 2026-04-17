<template>
  <div class="statistics">
    <a-row :gutter="16" style="margin-bottom: 20px">
      <a-col :xs="24" :sm="12" :lg="6">
        <a-statistic title="总用户数" :value="stats.totalUsers" :value-style="{ color: '#1677ff' }" />
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <a-statistic title="活跃用户" :value="stats.activeUsers" :value-style="{ color: '#52c41a' }" />
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <a-statistic title="认证教练" :value="stats.certifiedCoaches" :value-style="{ color: '#faad14' }" />
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <a-statistic title="社区内容" :value="stats.communityContent" :value-style="{ color: '#f5222d' }" />
      </a-col>
    </a-row>

    <a-row :gutter="16">
      <a-col :xs="24" :lg="12">
        <a-card title="用户增长趋势" :bordered="false" :loading="chartsLoading">
          <div id="userGrowthChart" style="height: 300px"></div>
        </a-card>
      </a-col>
      <a-col :xs="24" :lg="12">
        <a-card title="用户角色分布" :bordered="false" :loading="chartsLoading">
          <div id="userRoleChart" style="height: 300px"></div>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16" style="margin-top: 20px">
      <a-col :xs="24" :lg="12">
        <a-card title="每日活跃用户" :bordered="false" :loading="chartsLoading">
          <div id="dailyActiveChart" style="height: 300px"></div>
        </a-card>
      </a-col>
      <a-col :xs="24" :lg="12">
        <a-card title="内容审核统计" :bordered="false" :loading="chartsLoading">
          <div id="contentReviewChart" style="height: 300px"></div>
        </a-card>
      </a-col>
    </a-row>

    <a-card title="详细数据" :bordered="false" style="margin-top: 20px">
      <a-tabs>
        <a-tab-pane key="1" tab="用户统计">
          <a-table
            :columns="userColumns"
            :data-source="userStats"
            :loading="tableLoading"
            :pagination="{ pageSize: 10 }"
            rowKey="id"
          />
        </a-tab-pane>
        <a-tab-pane key="2" tab="内容统计">
          <a-table
            :columns="contentColumns"
            :data-source="contentStats"
            :loading="tableLoading"
            :pagination="{ pageSize: 10 }"
            rowKey="id"
          />
        </a-tab-pane>
        <a-tab-pane key="3" tab="教练统计">
          <a-table
            :columns="coachColumns"
            :data-source="coachStats"
            :loading="tableLoading"
            :pagination="{ pageSize: 10 }"
            rowKey="id"
          />
        </a-tab-pane>
      </a-tabs>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { message } from 'ant-design-vue';
import * as echarts from 'echarts';
import {
  getStatisticsOverview,
  getUserGrowthTrend,
  getUserRoleDistribution,
  getDailyActiveUsers,
  getContentReviewStats,
  getUserStats,
  getContentStats,
  getCoachStats,
} from '../../api';

const stats = ref({
  totalUsers: 0,
  activeUsers: 0,
  certifiedCoaches: 0,
  communityContent: 0,
});

const chartsLoading = ref(false);
const tableLoading = ref(false);

const userColumns = [
  {
    title: '日期',
    dataIndex: 'date',
    key: 'date',
  },
  {
    title: '新增用户',
    dataIndex: 'newUsers',
    key: 'newUsers',
  },
  {
    title: '活跃用户',
    dataIndex: 'activeUsers',
    key: 'activeUsers',
  },
  {
    title: '留存率',
    dataIndex: 'retentionRate',
    key: 'retentionRate',
  },
];

const contentColumns = [
  {
    title: '日期',
    dataIndex: 'date',
    key: 'date',
  },
  {
    title: '新增内容',
    dataIndex: 'newContent',
    key: 'newContent',
  },
  {
    title: '待审核',
    dataIndex: 'pending',
    key: 'pending',
  },
  {
    title: '已通过',
    dataIndex: 'approved',
    key: 'approved',
  },
  {
    title: '已拒绝',
    dataIndex: 'rejected',
    key: 'rejected',
  },
];

const coachColumns = [
  {
    title: '日期',
    dataIndex: 'date',
    key: 'date',
  },
  {
    title: '新增申请',
    dataIndex: 'newApplications',
    key: 'newApplications',
  },
  {
    title: '已认证',
    dataIndex: 'certified',
    key: 'certified',
  },
  {
    title: '待审核',
    dataIndex: 'pending',
    key: 'pending',
  },
];

const userStats = ref([]);
const contentStats = ref([]);
const coachStats = ref([]);
let userGrowthChart: echarts.ECharts | null = null;
let userRoleChart: echarts.ECharts | null = null;
let dailyActiveChart: echarts.ECharts | null = null;
let contentReviewChart: echarts.ECharts | null = null;

const fetchStatistics = async () => {
  try {
    // 获取概览数据
    const overviewRes = await getStatisticsOverview();
    if (overviewRes.data) {
      stats.value = overviewRes.data;
    }
  } catch (error) {
    message.error('获取统计数据失败');
  }
};

const fetchChartData = async () => {
  chartsLoading.value = true;
  try {
    const dateRange = {
      startDate: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      endDate: new Date().toISOString().split('T')[0],
    };

    const [userGrowthRes, userRoleRes, dailyActiveRes, contentReviewRes] = await Promise.allSettled([
      getUserGrowthTrend(dateRange),
      getUserRoleDistribution(),
      getDailyActiveUsers(dateRange),
      getContentReviewStats(dateRange),
    ]);
    const rejectedCount = [userGrowthRes, userRoleRes, dailyActiveRes, contentReviewRes].filter(
      (item) => item.status === 'rejected'
    ).length;
    if (rejectedCount > 0) {
      message.warning('部分图表数据加载失败');
    }
    const userGrowthData = userGrowthRes.status === 'fulfilled' ? userGrowthRes.value.data || [] : [];
    const userRoleData = userRoleRes.status === 'fulfilled' ? userRoleRes.value.data || [] : [];
    const dailyActiveData = dailyActiveRes.status === 'fulfilled' ? dailyActiveRes.value.data || [] : [];
    const contentReviewData = contentReviewRes.status === 'fulfilled' ? contentReviewRes.value.data || [] : [];

    chartsLoading.value = false;
    await nextTick();
    initCharts(userGrowthData, userRoleData, dailyActiveData, contentReviewData);
  } catch (error) {
    message.error('获取图表数据失败');
  } finally {
    if (chartsLoading.value) {
      chartsLoading.value = false;
    }
  }
};

const fetchTableData = async () => {
  tableLoading.value = true;
  try {
    const dateRange = {
      startDate: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      endDate: new Date().toISOString().split('T')[0],
    };

    const [userRes, contentRes, coachRes] = await Promise.all([
      getUserStats(dateRange),
      getContentStats(dateRange),
      getCoachStats(dateRange),
    ]);

    userStats.value = userRes.data || [];
    contentStats.value = contentRes.data || [];
    coachStats.value = coachRes.data || [];
  } catch (error) {
    message.error('获取表格数据失败');
  } finally {
    tableLoading.value = false;
  }
};

const initCharts = (userGrowthData, userRoleData, dailyActiveData, contentReviewData) => {
  const userGrowthDom = document.getElementById('userGrowthChart');
  const userRoleDom = document.getElementById('userRoleChart');
  const dailyActiveDom = document.getElementById('dailyActiveChart');
  const contentReviewDom = document.getElementById('contentReviewChart');
  if (!userGrowthDom || !userRoleDom || !dailyActiveDom || !contentReviewDom) {
    return;
  }

  userGrowthChart?.dispose();
  userRoleChart?.dispose();
  dailyActiveChart?.dispose();
  contentReviewChart?.dispose();

  // 用户增长趋势
  userGrowthChart = echarts.init(userGrowthDom);
  userGrowthChart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: userGrowthData.map((item) => item.date),
    },
    yAxis: { type: 'value' },
    series: [
      {
        data: userGrowthData.map((item) => item.totalUsers),
        type: 'line',
        smooth: true,
        itemStyle: { color: '#1677ff' },
      },
    ],
  });

  // 用户角色分布
  userRoleChart = echarts.init(userRoleDom);
  userRoleChart.setOption({
    tooltip: { trigger: 'item' },
    series: [
      {
        data: userRoleData.map((item) => ({ value: item.count, name: item.role })),
        type: 'pie',
      },
    ],
  });

  // 每日活跃用户
  dailyActiveChart = echarts.init(dailyActiveDom);
  dailyActiveChart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: dailyActiveData.map((item) => item.date),
    },
    yAxis: { type: 'value' },
    series: [
      {
        data: dailyActiveData.map((item) => item.activeUsers),
        type: 'bar',
        itemStyle: { color: '#52c41a' },
      },
    ],
  });

  // 内容审核统计
  contentReviewChart = echarts.init(contentReviewDom);
  contentReviewChart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: contentReviewData.map((item) => item.date),
    },
    yAxis: { type: 'value' },
    series: [
      {
        name: '已通过',
        data: contentReviewData.map((item) => item.approved),
        type: 'bar',
        stack: 'total',
        itemStyle: { color: '#52c41a' },
      },
      {
        name: '待审核',
        data: contentReviewData.map((item) => item.pending),
        type: 'bar',
        stack: 'total',
        itemStyle: { color: '#faad14' },
      },
      {
        name: '已拒绝',
        data: contentReviewData.map((item) => item.rejected),
        type: 'bar',
        stack: 'total',
        itemStyle: { color: '#f5222d' },
      },
    ],
  });
};

onMounted(() => {
  fetchStatistics();
  fetchChartData();
  fetchTableData();
});

onBeforeUnmount(() => {
  userGrowthChart?.dispose();
  userRoleChart?.dispose();
  dailyActiveChart?.dispose();
  contentReviewChart?.dispose();
});
</script>

<style scoped>
.statistics {
  padding: 0;
}
</style>
