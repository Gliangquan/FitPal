import request from '../request';
import type { BaseResponse, PageData } from '../types';

export interface UserLoginRequest {
  loginType: 'phone' | 'account';
  userPhone?: string;
  userAccount?: string;
  userPassword: string;
}

export interface UserRegisterRequest {
  userAccount: string;
  userPassword: string;
  checkPassword: string;
  userPhone: string;
}

export interface LoginUserVO {
  id: number;
  userAccount: string;
  userName?: string;
  userAvatar?: string;
  userProfile?: string;
  userRole: 'user' | 'coach' | 'admin' | 'ban';
  token?: string;
  createTime?: string;
  updateTime?: string;
  isNewUser?: boolean;
}

export interface UserVO {
  id: number;
  userName?: string;
  userAvatar?: string;
  userProfile?: string;
  userRole: string;
  createTime?: string;
}

export interface User {
  id: number;
  userAccount: string;
  userName?: string;
  userAvatar?: string;
  userProfile?: string;
  userRole: string;
  userPhone?: string;
  userEmail?: string;
  status?: number;
  createTime?: string;
  updateTime?: string;
}

export interface UserQueryRequest {
  id?: number;
  unionId?: string;
  mpOpenId?: string;
  userName?: string;
  userProfile?: string;
  userRole?: string;
  current?: number;
  pageSize?: number;
  sortField?: string;
  sortOrder?: string;
}

export interface UserAddRequest {
  userAccount: string;
  userName?: string;
  userAvatar?: string;
  userRole?: string;
}

export interface UserUpdateRequest {
  id: number;
  userName?: string;
  userAvatar?: string;
  userProfile?: string;
  userRole?: string;
}

export interface UserUpdateMyRequest {
  userName?: string;
  userAvatar?: string;
  userProfile?: string;
}

export interface DeleteRequest {
  id: number;
}

export interface UserBatchDeleteRequest {
  ids: number[];
  softDelete?: boolean;
}

export interface UserBatchUpdateRequest {
  ids: number[];
  userName?: string;
  userRole?: string;
  status?: number;
  userProfile?: string;
}

export interface UserStatisticsVO {
  totalUsers: number;
  activeUsers: number;
  newUsers: number;
  adminCount: number;
  userCount: number;
  banCount: number;
  enabledCount: number;
  disabledCount: number;
  todayLoginCount: number;
  weekLoginCount: number;
  monthLoginCount: number;
}

export interface UserExportRequest {
  format?: string;
  userName?: string;
  userAccount?: string;
  userRole?: string;
  status?: number;
  exportAll?: boolean;
  fields?: string;
}

export interface UserImportRequest {
  fileContent: string;
  fileType: string;
  skipDuplicate?: boolean;
  defaultPassword?: string;
  defaultRole?: string;
}

export function userLogin(data: UserLoginRequest): Promise<BaseResponse<LoginUserVO>> {
  return request.post('/user/login', data) as Promise<BaseResponse<LoginUserVO>>;
}

export function userRegister(data: UserRegisterRequest): Promise<BaseResponse<number>> {
  return request.post('/user/register', data) as Promise<BaseResponse<number>>;
}

export function userLogout(): Promise<BaseResponse<boolean>> {
  return request.post('/user/logout') as Promise<BaseResponse<boolean>>;
}

export function getLoginUser(): Promise<BaseResponse<LoginUserVO>> {
  return request.get('/user/get/login') as Promise<BaseResponse<LoginUserVO>>;
}

export function updateMyUser(data: UserUpdateMyRequest): Promise<BaseResponse<boolean>> {
  return request.post('/user/update/my', data) as Promise<BaseResponse<boolean>>;
}

export function addUser(data: UserAddRequest): Promise<BaseResponse<number>> {
  return request.post('/user/add', data) as Promise<BaseResponse<number>>;
}

export function updateUser(data: UserUpdateRequest): Promise<BaseResponse<boolean>> {
  return request.post('/user/update', data) as Promise<BaseResponse<boolean>>;
}

export function deleteUser(data: DeleteRequest): Promise<BaseResponse<boolean>> {
  return request.post('/user/delete', data) as Promise<BaseResponse<boolean>>;
}

export function getUserById(id: number): Promise<BaseResponse<User>> {
  return request.get('/user/get', { params: { id } }) as Promise<BaseResponse<User>>;
}

export function getUserVOById(id: number): Promise<BaseResponse<UserVO>> {
  return request.get('/user/get/vo', { params: { id } }) as Promise<BaseResponse<UserVO>>;
}

export function listUserByPage(data: UserQueryRequest): Promise<BaseResponse<PageData<User>>> {
  return request.post('/user/list/page', data) as Promise<BaseResponse<PageData<User>>>;
}

export function listUserVOByPage(data: UserQueryRequest): Promise<BaseResponse<PageData<UserVO>>> {
  return request.post('/user/list/page/vo', data) as Promise<BaseResponse<PageData<UserVO>>>;
}

export function batchDeleteUser(data: UserBatchDeleteRequest): Promise<BaseResponse<number>> {
  return request.post('/user/batch-delete', data) as Promise<BaseResponse<number>>;
}

export function batchUpdateUser(data: UserBatchUpdateRequest): Promise<BaseResponse<number>> {
  return request.post('/user/batch-update', data) as Promise<BaseResponse<number>>;
}

export function getUserStatistics(): Promise<BaseResponse<UserStatisticsVO>> {
  return request.get('/user/statistics') as Promise<BaseResponse<UserStatisticsVO>>;
}

export function exportUser(data: UserExportRequest): Promise<BaseResponse<string>> {
  return request.post('/user/export', data) as Promise<BaseResponse<string>>;
}

export function importUser(data: UserImportRequest): Promise<BaseResponse<number>> {
  return request.post('/user/import', data) as Promise<BaseResponse<number>>;
}
