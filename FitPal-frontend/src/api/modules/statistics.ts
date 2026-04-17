import request from '../request';
import type { BaseResponse, PageData } from '../types';

export interface StatisticsOverview {
  totalUsers: number;
  activeUsers: number;
  certifiedCoaches: number;
  communityContent: number;
}

export interface UserGrowthData {
  date: string;
  totalUsers: number;
}

export interface UserRoleDistribution {
  role: string;
  count: number;
}

export interface DailyActiveData {
  date: string;
  activeUsers: number;
}

export interface ContentReviewData {
  date: string;
  newContent: number;
  pending: number;
  approved: number;
  rejected: number;
}

export interface UserStatData {
  date: string;
  newUsers: number;
  activeUsers: number;
  retentionRate: string;
}

export interface ContentStatData {
  date: string;
  newContent: number;
  pending: number;
  approved: number;
  rejected: number;
}

export interface CoachStatData {
  date: string;
  newApplications: number;
  certified: number;
  pending: number;
}

export interface StatisticsDateRangeRequest {
  startDate?: string;
  endDate?: string;
}

// 获取统计概览
export function getStatisticsOverview(): Promise<BaseResponse<StatisticsOverview>> {
  return request.get('/statistics/overview') as Promise<BaseResponse<StatisticsOverview>>;
}

// 获取用户增长趋势
export function getUserGrowthTrend(
  data: StatisticsDateRangeRequest
): Promise<BaseResponse<UserGrowthData[]>> {
  return request.post('/statistics/user-growth', data) as Promise<BaseResponse<UserGrowthData[]>>;
}

// 获取用户角色分布
export function getUserRoleDistribution(): Promise<BaseResponse<UserRoleDistribution[]>> {
  return request.get('/statistics/user-role-distribution') as Promise<
    BaseResponse<UserRoleDistribution[]>
  >;
}

// 获取每日活跃用户
export function getDailyActiveUsers(
  data: StatisticsDateRangeRequest
): Promise<BaseResponse<DailyActiveData[]>> {
  return request.post('/statistics/daily-active', data) as Promise<BaseResponse<DailyActiveData[]>>;
}

// 获取内容审核统计
export function getContentReviewStats(
  data: StatisticsDateRangeRequest
): Promise<BaseResponse<ContentReviewData[]>> {
  return request.post('/statistics/content-review', data) as Promise<
    BaseResponse<ContentReviewData[]>
  >;
}

// 获取用户统计数据
export function getUserStats(
  data: StatisticsDateRangeRequest
): Promise<BaseResponse<UserStatData[]>> {
  return request.post('/statistics/user-stats', data) as Promise<BaseResponse<UserStatData[]>>;
}

// 获取内容统计数据
export function getContentStats(
  data: StatisticsDateRangeRequest
): Promise<BaseResponse<ContentStatData[]>> {
  return request.post('/statistics/content-stats', data) as Promise<BaseResponse<ContentStatData[]>>;
}

// 获取教练统计数据
export function getCoachStats(
  data: StatisticsDateRangeRequest
): Promise<BaseResponse<CoachStatData[]>> {
  return request.post('/statistics/coach-stats', data) as Promise<BaseResponse<CoachStatData[]>>;
}
