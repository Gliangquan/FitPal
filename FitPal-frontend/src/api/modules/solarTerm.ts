import request from '../request';
import type { BaseResponse, PageData } from '../types';

export interface SolarTerm {
  id: number;
  solarTermName: string;
  title: string;
  description: string;
  day1Recipe: string;
  day2Recipe: string;
  day3Recipe: string;
  exerciseGuide: string;
  lifestyleAdvice: string;
  healthKnowledge: string;
  coverImage?: string;
  status: 'draft' | 'published';
  createdAt: string;
  updatedAt: string;
}

export interface SolarTermQueryRequest {
  solarTermName?: string;
  status?: string;
  current?: number;
  pageSize?: number;
}

export interface SolarTermAddRequest {
  solarTermName: string;
  title: string;
  description: string;
  day1Recipe: string;
  day2Recipe: string;
  day3Recipe: string;
  exerciseGuide: string;
  lifestyleAdvice: string;
  healthKnowledge: string;
  coverImage?: string;
  status: 'draft' | 'published';
}

export interface SolarTermUpdateRequest {
  id: number;
  solarTermName?: string;
  title?: string;
  description?: string;
  day1Recipe?: string;
  day2Recipe?: string;
  day3Recipe?: string;
  exerciseGuide?: string;
  lifestyleAdvice?: string;
  healthKnowledge?: string;
  coverImage?: string;
  status?: 'draft' | 'published';
}

// 获取节气列表
export function listSolarTermByPage(
  data: SolarTermQueryRequest
): Promise<BaseResponse<PageData<SolarTerm>>> {
  return request.post('/solar-term/list/page', data) as Promise<BaseResponse<PageData<SolarTerm>>>;
}

// 获取节气详情
export function getSolarTermById(id: number): Promise<BaseResponse<SolarTerm>> {
  return request.get('/solar-term/get', { params: { id } }) as Promise<BaseResponse<SolarTerm>>;
}

// 新增节气
export function addSolarTerm(data: SolarTermAddRequest): Promise<BaseResponse<number>> {
  return request.post('/solar-term/add', data) as Promise<BaseResponse<number>>;
}

// 更新节气
export function updateSolarTerm(data: SolarTermUpdateRequest): Promise<BaseResponse<boolean>> {
  return request.post('/solar-term/update', data) as Promise<BaseResponse<boolean>>;
}

// 删除节气
export function deleteSolarTerm(id: number): Promise<BaseResponse<boolean>> {
  return request.post('/solar-term/delete', { id }) as Promise<BaseResponse<boolean>>;
}

// 发布节气
export function publishSolarTerm(id: number): Promise<BaseResponse<boolean>> {
  return request.post('/solar-term/publish', { id }) as Promise<BaseResponse<boolean>>;
}

// 获取所有节气名称列表
export function listAllSolarTermNames(): Promise<BaseResponse<string[]>> {
  return request.get('/solar-term/names') as Promise<BaseResponse<string[]>>;
}
