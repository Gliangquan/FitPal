import request from '../request';
import type { BaseResponse } from '../types';

export interface UserSettings {
  id?: number;
  userId: number;
  checkinReminderEnabled?: number;
  communityNotificationEnabled?: number;
  weeklyReportNotificationEnabled?: number;
  coachReplyNotificationEnabled?: number;
  healthDataVisible?: number;
  profileVisible?: number;
  consultationDataRetentionDays?: number;
  createTime?: string;
  updateTime?: string;
  isDelete?: number;
}

export function getUserSettings(userId: number): Promise<BaseResponse<UserSettings>> {
  return request.get('/user-settings/get', { params: { userId } }) as Promise<BaseResponse<UserSettings>>;
}

export function updateNotificationSettings(userId: number, data: Partial<UserSettings>): Promise<BaseResponse<string>> {
  return request.post('/user-settings/notification/update', data, { params: { userId } }) as Promise<BaseResponse<string>>;
}

export function updatePrivacySettings(userId: number, data: Partial<UserSettings>): Promise<BaseResponse<string>> {
  return request.post('/user-settings/privacy/update', data, { params: { userId } }) as Promise<BaseResponse<string>>;
}
