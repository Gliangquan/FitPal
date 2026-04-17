import request from '../request';
import type { BaseResponse } from '../types';

export type FileBizType = 'user_avatar' | 'community_post' | 'content_cover';

export function uploadFile(file: File, biz: FileBizType = 'user_avatar'): Promise<BaseResponse<string>> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('biz', biz);
  return request.post('/file/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }) as Promise<BaseResponse<string>>;
}

export function getFilePreviewUrl(biz: string, userId: number, filename: string): string {
  return `/api/file/preview/${biz}/${userId}/${encodeURIComponent(filename)}`;
}

export function getFileDownloadUrl(biz: string, userId: number, filename: string): string {
  return `/api/file/download/${biz}/${userId}/${encodeURIComponent(filename)}`;
}

export function resolveFilePreviewUrl(filePath?: string): string {
  if (!filePath) return '';
  if (filePath.startsWith('http://') || filePath.startsWith('https://') || filePath.startsWith('data:')) {
    return filePath;
  }
  if (filePath.startsWith('/api/file/')) {
    return filePath;
  }
  if (filePath.startsWith('/files/')) {
    const segments = filePath.split('/').filter(Boolean);
    if (segments.length >= 4) {
      const biz = segments[1];
      const userId = Number(segments[2]);
      const filename = segments.slice(3).join('/');
      if (!Number.isNaN(userId) && filename) {
        return getFilePreviewUrl(biz, userId, filename);
      }
    }
  }
  return filePath;
}
