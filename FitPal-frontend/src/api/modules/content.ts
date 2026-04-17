import request from '../request';
import type { BaseResponse, PageData } from '../types';

export interface Content {
  id: number;
  contentType: 'article' | 'video' | 'recipe' | 'exercise';
  title: string;
  description: string;
  content: string;
  targetAudience: string;
  tags: string[];
  coverImage?: string;
  status: 'draft' | 'published' | 'archived';
  recommendScore: number;
  createdAt: string;
  updatedAt: string;
}

export interface ContentQueryRequest {
  contentType?: string;
  status?: string;
  title?: string;
  current?: number;
  pageSize?: number;
}

export interface ContentAddRequest {
  contentType: 'article' | 'video' | 'recipe' | 'exercise';
  title: string;
  description: string;
  content: string;
  targetAudience: string;
  tags: string[];
  coverImage?: string;
  status: 'draft' | 'published' | 'archived';
  recommendScore: number;
}

export interface ContentUpdateRequest {
  id: number;
  contentType?: 'article' | 'video' | 'recipe' | 'exercise';
  title?: string;
  description?: string;
  content?: string;
  targetAudience?: string;
  tags?: string[];
  coverImage?: string;
  status?: 'draft' | 'published' | 'archived';
  recommendScore?: number;
}

// 获取内容列表
export function listContentByPage(
  data: ContentQueryRequest
): Promise<BaseResponse<PageData<Content>>> {
  return request.post('/content/list/page', data) as Promise<BaseResponse<PageData<Content>>>;
}

// 获取内容详情
export function getContentById(id: number): Promise<BaseResponse<Content>> {
  return request.get('/content/get', { params: { id } }) as Promise<BaseResponse<Content>>;
}

// 新增内容
export function addContent(data: ContentAddRequest): Promise<BaseResponse<number>> {
  return request.post('/content/add', data) as Promise<BaseResponse<number>>;
}

// 更新内容
export function updateContent(data: ContentUpdateRequest): Promise<BaseResponse<boolean>> {
  return request.post('/content/update', data) as Promise<BaseResponse<boolean>>;
}

// 删除内容
export function deleteContent(id: number): Promise<BaseResponse<boolean>> {
  return request.post('/content/delete', { id }) as Promise<BaseResponse<boolean>>;
}

// 发布内容
export function publishContent(id: number): Promise<BaseResponse<boolean>> {
  return request.post('/content/publish', { id }) as Promise<BaseResponse<boolean>>;
}

// 归档内容
export function archiveContent(id: number): Promise<BaseResponse<boolean>> {
  return request.post('/content/archive', { id }) as Promise<BaseResponse<boolean>>;
}

// 批量删除内容
export function batchDeleteContent(ids: number[]): Promise<BaseResponse<number>> {
  return request.post('/content/batch-delete', { ids }) as Promise<BaseResponse<number>>;
}

// 获取推荐内容
export function getRecommendedContent(limit?: number): Promise<BaseResponse<Content[]>> {
  return request.get('/content/recommended', { params: { limit } }) as Promise<
    BaseResponse<Content[]>
  >;
}
