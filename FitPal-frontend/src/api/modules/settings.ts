import request from '../request';
import type { BaseResponse } from '../types';

export interface BasicSettings {
  platformName: string;
  platformDescription: string;
  contactPhone: string;
  contactEmail: string;
  termsUrl: string;
  privacyUrl: string;
}

export interface FeatureSettings {
  communityEnabled: boolean;
  coachEnabled: boolean;
  pointsEnabled: boolean;
  solarTermEnabled: boolean;
  analyticsEnabled: boolean;
  registrationEnabled: boolean;
}

export interface ReviewSettings {
  autoReviewSensitiveWords: boolean;
  sensitiveWords: string;
  maxContentLength: number;
  maxImageCount: number;
  autoApproveThreshold: number;
}

export interface PointsSettings {
  dailyCheckInPoints: number;
  postContentPoints: number;
  contentLikePoints: number;
  completeTaskPoints: number;
  inviteFriendPoints: number;
  pointsExpireDays: number;
}

export interface EmailSettings {
  smtpServer: string;
  smtpPort: number;
  senderEmail: string;
  senderPassword: string;
  enabled: boolean;
}

export interface SystemLog {
  id: number;
  timestamp: string;
  action: string;
  operator: string;
  details: string;
  status: string;
}

export interface SystemLogQueryRequest {
  action?: string;
  operator?: string;
  status?: string;
  startDate?: string;
  endDate?: string;
  current?: number;
  pageSize?: number;
}

// 基础配置
export function getBasicSettings(): Promise<BaseResponse<BasicSettings>> {
  return request.get('/settings/basic') as Promise<BaseResponse<BasicSettings>>;
}

export function updateBasicSettings(data: BasicSettings): Promise<BaseResponse<boolean>> {
  return request.post('/settings/basic/update', data) as Promise<BaseResponse<boolean>>;
}

// 功能开关
export function getFeatureSettings(): Promise<BaseResponse<FeatureSettings>> {
  return request.get('/settings/features') as Promise<BaseResponse<FeatureSettings>>;
}

export function updateFeatureSettings(data: FeatureSettings): Promise<BaseResponse<boolean>> {
  return request.post('/settings/features/update', data) as Promise<BaseResponse<boolean>>;
}

// 内容审核规则
export function getReviewSettings(): Promise<BaseResponse<ReviewSettings>> {
  return request.get('/settings/review') as Promise<BaseResponse<ReviewSettings>>;
}

export function updateReviewSettings(data: ReviewSettings): Promise<BaseResponse<boolean>> {
  return request.post('/settings/review/update', data) as Promise<BaseResponse<boolean>>;
}

// 积分规则
export function getPointsSettings(): Promise<BaseResponse<PointsSettings>> {
  return request.get('/settings/points') as Promise<BaseResponse<PointsSettings>>;
}

export function updatePointsSettings(data: PointsSettings): Promise<BaseResponse<boolean>> {
  return request.post('/settings/points/update', data) as Promise<BaseResponse<boolean>>;
}

// 邮件通知
export function getEmailSettings(): Promise<BaseResponse<EmailSettings>> {
  return request.get('/settings/email') as Promise<BaseResponse<EmailSettings>>;
}

export function updateEmailSettings(data: EmailSettings): Promise<BaseResponse<boolean>> {
  return request.post('/settings/email/update', data) as Promise<BaseResponse<boolean>>;
}

export function sendTestEmail(email: string): Promise<BaseResponse<boolean>> {
  return request.post('/settings/email/test', { email }) as Promise<BaseResponse<boolean>>;
}

// 系统日志
export function listSystemLogs(
  data: SystemLogQueryRequest
): Promise<BaseResponse<{ records: SystemLog[]; total: number }>> {
  return request.post('/settings/logs', data) as Promise<
    BaseResponse<{ records: SystemLog[]; total: number }>
  >;
}

export function exportSystemLogs(
  data: SystemLogQueryRequest
): Promise<BaseResponse<string>> {
  return request.post('/settings/logs/export', data) as Promise<BaseResponse<string>>;
}

export function clearSystemLogs(): Promise<BaseResponse<boolean>> {
  return request.post('/settings/logs/clear') as Promise<BaseResponse<boolean>>;
}
