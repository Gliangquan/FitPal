const BASE_URL = '/api';
const TOKEN_KEY = 'fitpal_token';

const showLoading = (show = true) => {
  if (show) {
    uni.showLoading({ title: '加载中...' });
  }
};

const hideLoading = (show = true) => {
  if (show) {
    uni.hideLoading();
  }
};

const buildQuery = (params = {}) => {
  const entries = Object.entries(params).filter(([, value]) => value !== undefined && value !== null && value !== '');
  if (!entries.length) return '';
  const query = entries.map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`).join('&');
  return `?${query}`;
};

const request = ({ url, method = 'GET', data = {}, params = {}, header = {}, showLoading: loading = true }) => {
  return new Promise((resolve, reject) => {
    showLoading(loading);
    const token = uni.getStorageSync(TOKEN_KEY);
    const finalUrl = `${BASE_URL}${url}${buildQuery(params)}`;
    const body = method === 'GET' ? undefined : data;
    uni.request({
      url: finalUrl,
      method,
      header: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...header
      },
      data: body,
      success: (res) => {
        hideLoading(loading);
        const { statusCode, data: response } = res;
        if (statusCode === 401 || response?.code === 40100) {
          uni.clearStorageSync();
          uni.showToast({ title: '登录过期，请重新登录', icon: 'none' });
          setTimeout(() => {
            uni.reLaunch({ url: '/pages/login/index' });
          }, 800);
          reject(new Error('未登录'));
          return;
        }
        if (statusCode >= 200 && statusCode < 300 && response) {
          if (response.code === 0) {
            resolve(response.data);
          } else {
            reject(new Error(response.message || '请求失败'));
          }
        } else {
          reject(new Error(response?.message || `请求失败 ${statusCode}`));
        }
      },
      fail: (error) => {
        hideLoading(loading);
        reject(error);
      }
    });
  });
};

const setToken = (token) => {
  if (token) {
    uni.setStorageSync(TOKEN_KEY, token);
  } else {
    uni.removeStorageSync(TOKEN_KEY);
  }
};

const getToken = () => uni.getStorageSync(TOKEN_KEY);

const getApiOrigin = () => {
  const url = String(BASE_URL || '');
  const apiIndex = url.indexOf('/api');
  if (apiIndex > 0) {
    return url.slice(0, apiIndex);
  }
  return url.replace(/\/+$/, '');
};

const resolveFileUrl = (url) => {
  if (!url) return '';
  const raw = String(url).trim();
  if (!raw) return '';
  if (raw.startsWith('http://') || raw.startsWith('https://') || raw.startsWith('data:')) {
    return raw;
  }
  if (raw.startsWith('blob:') || raw.startsWith('wxfile://') || raw.startsWith('file://')) {
    return raw;
  }

  if (raw.startsWith('/files/')) {
    const segments = raw.split('/').filter(Boolean);
    if (segments.length >= 4) {
      const biz = segments[1];
      const userId = Number(segments[2]);
      const filename = segments.slice(3).join('/');
      if (!Number.isNaN(userId) && filename) {
        return `${BASE_URL}/file/preview/${biz}/${userId}/${encodeURIComponent(filename)}`;
      }
    }
  }

  if (raw.startsWith('/api/')) {
    return `${getApiOrigin()}${raw}`;
  }

  if (raw.startsWith('/')) {
    return `${BASE_URL}${raw}`;
  }

  return `${BASE_URL}/${raw}`;
};

export { request, setToken, getToken, BASE_URL, resolveFileUrl };
