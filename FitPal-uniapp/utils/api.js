import { request, setToken, getToken, BASE_URL } from '@/utils/request';

const uploadByBiz = (filePath, biz) => {
  return new Promise((resolve, reject) => {
    const token = getToken();
    uni.uploadFile({
      url: `${BASE_URL}/file/upload?biz=${encodeURIComponent(biz)}`,
      filePath,
      name: 'file',
      header: token ? { Authorization: `Bearer ${token}` } : {},
      success: (res) => {
        let payload = {};
        try {
          payload = JSON.parse(res.data || '{}');
        } catch (error) {
          reject(new Error('图片上传响应解析失败'));
          return;
        }
        if (res.statusCode >= 200 && res.statusCode < 300 && payload.code === 0) {
          resolve(payload.data);
        } else {
          reject(new Error(payload.message || '图片上传失败'));
        }
      },
      fail: (error) => reject(error)
    });
  });
};

const userApi = {
  login(payload) {
    return request({
      url: '/user/login',
      method: 'POST',
      data: payload
    });
  },
  register(payload) {
    return request({
      url: '/user/register',
      method: 'POST',
      data: payload
    });
  },
  fetchCurrentUser() {
    return request({
      url: '/user/get/login',
      method: 'GET'
    });
  },
  updateProfile(payload) {
    return request({
      url: '/user/update/my',
      method: 'POST',
      data: payload
    });
  },
  logout() {
    return request({
      url: '/user/logout',
      method: 'POST'
    });
  },
  changePassword(payload) {
    return request({
      url: '/user/update/password',
      method: 'POST',
      data: payload
    });
  },
  activateMembership(payload) {
    return request({
      url: '/user/membership/activate',
      method: 'POST',
      data: payload
    });
  },
  uploadAvatar(filePath) {
    return uploadByBiz(filePath, 'user_avatar');
  }
};

const fitApi = {
  addHealthRecord(payload) {
    return request({
      url: '/fit/health/record',
      method: 'POST',
      data: payload
    });
  },
  listHealthRecords(days = 30) {
    return request({
      url: '/fit/health/records',
      method: 'GET',
      params: { days }
    });
  },
  getHealthReport(days = 30) {
    return request({
      url: '/fit/health/report',
      method: 'GET',
      params: { days }
    });
  },
  submitQuestionnaire(payload) {
    return request({
      url: '/fit/questionnaire/submit',
      method: 'POST',
      data: payload
    });
  },
  generatePlan() {
    return request({
      url: '/fit/plan/generate',
      method: 'POST'
    });
  },
  getLatestPlan() {
    return request({
      url: '/fit/plan/latest',
      method: 'GET'
    });
  },
  getCurrentSeasonTopic() {
    return request({
      url: '/fit/season/topic/current',
      method: 'GET'
    });
  },
  recommendContent(stageTag, limit = 8) {
    return request({
      url: '/fit/content/recommend',
      method: 'GET',
      params: { stageTag, limit }
    });
  },
  getContentDetail(id) {
    return request({
      url: `/fit/content/${id}`,
      method: 'GET'
    });
  },
  addCommunityPost(payload) {
    return request({
      url: '/fit/community/post',
      method: 'POST',
      data: payload
    });
  },
  listCommunityPosts(params) {
    return request({
      url: '/fit/community/posts',
      method: 'GET',
      params
    });
  },
  getCommunityPostDetail(postId) {
    return request({
      url: `/fit/community/post/${postId}`,
      method: 'GET'
    });
  },
  likeCommunityPost(postId) {
    return request({
      url: `/fit/community/post/${postId}/like`,
      method: 'POST'
    });
  },
  commentCommunityPost(postId, payload) {
    return request({
      url: `/fit/community/post/${postId}/comment`,
      method: 'POST',
      data: payload
    });
  },
  listCommunityComments(postId, size = 30) {
    return request({
      url: `/fit/community/post/${postId}/comments`,
      method: 'GET',
      params: { size }
    });
  },
  uploadCommunityImage(filePath) {
    return uploadByBiz(filePath, 'community_post');
  },
  checkin() {
    return request({
      url: '/fit/points/checkin',
      method: 'POST'
    });
  },
  myPoints() {
    return request({
      url: '/fit/points/me',
      method: 'GET'
    });
  },
  getCheckinCalendar(month) {
    return request({
      url: '/fit/points/checkin/calendar',
      method: 'GET',
      params: { month }
    });
  },
  listPointBadges() {
    return request({
      url: '/fit/points/badges',
      method: 'GET'
    });
  },
  myPointBadges() {
    return request({
      url: '/fit/points/badges/me',
      method: 'GET'
    });
  },
  exchangePointBadge(badgeId) {
    return request({
      url: `/fit/points/badges/${badgeId}/exchange`,
      method: 'POST'
    });
  },
  applyCoachCertification(payload) {
    return request({
      url: '/fit/coach/certification/apply',
      method: 'POST',
      data: payload
    });
  },
  myCoachCertification() {
    return request({
      url: '/fit/coach/certification/me',
      method: 'GET'
    });
  },
  createConsultation(payload) {
    return request({
      url: '/fit/coach/consultation/create',
      method: 'POST',
      data: payload
    });
  },
  myConsultations() {
    return request({
      url: '/fit/coach/consultations',
      method: 'GET'
    });
  },
  coachTodoConsultations() {
    return request({
      url: '/fit/coach/consultation/todo',
      method: 'GET'
    });
  },
  coachReplyConsultation(id, payload) {
    return request({
      url: `/fit/coach/consultation/${id}/reply`,
      method: 'POST',
      data: payload
    });
  },
  listCoachPlans(params = {}) {
    return request({
      url: '/fit/coach/plans',
      method: 'GET',
      params
    });
  },
  optimizeCoachPlan(id, payload) {
    return request({
      url: `/fit/coach/plans/${id}/optimize`,
      method: 'PUT',
      data: payload
    });
  },
  getMyCoach() {
    return request({
      url: '/fit/coach/my',
      method: 'GET'
    });
  },
  rateCoach(payload) {
    return request({
      url: '/fit/coach/rate',
      method: 'POST',
      data: payload
    });
  },
  getMyCoachReviews() {
    return request({
      url: '/fit/coach/reviews/my',
      method: 'GET'
    });
  },
  getCoachReceivedReviews() {
    return request({
      url: '/fit/coach/reviews/received',
      method: 'GET'
    });
  },
  getCoachUsersData() {
    return request({
      url: '/fit/coach/users-data',
      method: 'GET'
    });
  },
  getCommunityPost(id) {
    return request({
      url: `/fit/community/post/${id}`,
      method: 'GET'
    });
  },
  getPostComments(postId) {
    return request({
      url: `/fit/community/post/${postId}/comments`,
      method: 'GET'
    });
  },
  addPostComment(postId, payload) {
    return request({
      url: `/fit/community/post/${postId}/comment`,
      method: 'POST',
      data: payload
    });
  }
};

export {
  userApi,
  fitApi,
  setToken
};
