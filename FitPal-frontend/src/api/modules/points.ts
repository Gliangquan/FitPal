import request from '../request';
import type { BaseResponse, PageData } from '../types';

export interface PointsRule {
  id: number;
  ruleName: string;
  ruleDescription: string;
  points: number;
  ruleType: string;
  enabled: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface UserPoints {
  id: number;
  userId: number;
  userName: string;
  totalPoints: number;
  medalCount: number;
  updatedAt: string;
}

export interface PointsRuleQueryRequest {
  ruleName?: string;
  ruleType?: string;
  enabled?: boolean;
  current?: number;
  pageSize?: number;
}

export interface PointsRuleAddRequest {
  ruleName: string;
  ruleDescription: string;
  points: number;
  ruleType: string;
  enabled: boolean;
}

export interface PointsRuleUpdateRequest {
  id: number;
  ruleName?: string;
  ruleDescription?: string;
  points?: number;
  ruleType?: string;
  enabled?: boolean;
}

export interface UserPointsAdjustRequest {
  userId: number;
  adjustPoints: number;
  reason: string;
}

export interface UserPointsQueryRequest {
  userId?: number;
  userName?: string;
  current?: number;
  pageSize?: number;
}

// 积分规则管理
export function listPointsRuleByPage(
  data: PointsRuleQueryRequest
): Promise<BaseResponse<PageData<PointsRule>>> {
  return request.post('/points/rule/list/page', data) as Promise<BaseResponse<PageData<PointsRule>>>;
}

export function addPointsRule(data: PointsRuleAddRequest): Promise<BaseResponse<number>> {
  return request.post('/points/rule/add', data) as Promise<BaseResponse<number>>;
}

export function updatePointsRule(data: PointsRuleUpdateRequest): Promise<BaseResponse<boolean>> {
  return request.post('/points/rule/update', data) as Promise<BaseResponse<boolean>>;
}

export function deletePointsRule(id: number): Promise<BaseResponse<boolean>> {
  return request.post('/points/rule/delete', { id }) as Promise<BaseResponse<boolean>>;
}

// 用户积分管理
export function listUserPointsByPage(
  data: UserPointsQueryRequest
): Promise<BaseResponse<PageData<UserPoints>>> {
  return request.post('/points/user/list/page', data) as Promise<BaseResponse<PageData<UserPoints>>>;
}

export function getUserPoints(userId: number): Promise<BaseResponse<UserPoints>> {
  return request.get('/points/user/get', { params: { userId } }) as Promise<
    BaseResponse<UserPoints>
  >;
}

export function adjustUserPoints(data: UserPointsAdjustRequest): Promise<BaseResponse<boolean>> {
  return request.post('/points/user/adjust', data) as Promise<BaseResponse<boolean>>;
}
