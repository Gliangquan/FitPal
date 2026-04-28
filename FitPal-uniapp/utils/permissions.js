const ROLE_FEATURES = {
  user: [
    'loginRegister',
    'healthDataRecord',
    'healthQuestionnaire',
    'personalizedFatLossPlan',
    'onlineConsultation',
    'pointsExchange',
    'communityInteraction',
    'membershipService',
    'coachServiceReview',
    'personalInfoManagement'
  ],
  coach: [
    'loginRegister',
    'coachCertification',
    'viewUserData',
    'fatLossPlanOptimization',
    'consultationReply',
    'memberCustomService',
    'viewServiceReviews'
  ],
  admin: ['adminBackstageLogin']
};

const FEATURE_ALLOWED_ROLES = {
  loginRegister: ['user', 'coach'],
  healthDataRecord: ['user'],
  healthQuestionnaire: ['user'],
  personalizedFatLossPlan: ['user'],
  onlineConsultation: ['user'],
  pointsExchange: ['user'],
  communityInteraction: ['user'],
  membershipService: ['user'],
  coachServiceReview: ['user'],
  personalInfoManagement: ['user'],
  coachCertification: ['coach'],
  viewUserData: ['coach'],
  fatLossPlanOptimization: ['coach'],
  consultationReply: ['coach'],
  memberCustomService: ['coach'],
  viewServiceReviews: ['coach'],
  adminBackstageLogin: ['admin']
};

const FEATURE_META = {
  healthDataRecord: {
    label: '健康数据记录',
    path: '/pages/fit/health',
    icon: '/static/icon_fit/zhenduanjilu.png'
  },
  healthQuestionnaire: {
    label: '填写健康问卷',
    path: '/pages/fit/questionnaire',
    icon: '/static/icon_fit/xunwen.png'
  },
  personalizedFatLossPlan: {
    label: '个性化减脂方案',
    path: '/pages/fit/plan',
    icon: '/static/icon_fit/geixnghua.png'
  },
  onlineConsultation: {
    label: '在线咨询',
    path: '/pages/consultation/index',
    icon: '/static/icon_fit/yisheng.png'
  },
  pointsExchange: {
    label: '积分兑换',
    path: '/pages/points-badges/index',
    icon: '/static/icon_fit/jiangbei.png'
  },
  communityInteraction: {
    label: '社区互动',
    path: '/pages/fit/community',
    icon: '/static/icon_fit/xiaoxi.png',
    tab: true
  },
  membershipService: {
    label: '会员服务',
    path: '/pages/membership/index',
    icon: '/static/icon_fit/youhuika.png'
  },
  coachServiceReview: {
    label: '教练服务评价',
    path: '/pages/my-coach/index',
    icon: '/static/icon_fit/zan.png'
  },
  personalInfoManagement: {
    label: '个人信息管理',
    path: '/pages/edit-profile/index',
    icon: '/static/icon_fit/bianji.png'
  },
  coachCertification: {
    label: '教练资质认证',
    path: '/pages/coach-certification/index',
    icon: '/static/icon_fit/xianhua.png'
  },
  viewUserData: {
    label: '查看用户数据',
    path: '/pages/coach-user-data/index',
    icon: '/static/icon_fit/bingli.png'
  },
  fatLossPlanOptimization: {
    label: '减脂方案优化',
    path: '/pages/coach-plan-optimize/index',
    icon: '/static/icon_fit/geixnghua.png'
  },
  consultationReply: {
    label: '在线咨询回复',
    path: '/pages/coach-workbench/index',
    icon: '/static/icon_fit/xiaoxi.png'
  },
  memberCustomService: {
    label: '会员定制服务',
    path: '/pages/coach-member-service/index',
    icon: '/static/icon_fit/youhuika.png'
  },
  viewServiceReviews: {
    label: '查看服务评价',
    path: '/pages/coach-service-reviews/index',
    icon: '/static/icon_fit/zan.png'
  }
};

function getCurrentUser() {
  return uni.getStorageSync('userInfo') || {};
}

function getCurrentRole() {
  const role = String(getCurrentUser()?.userRole || 'user').trim();
  return role || 'user';
}

function hasFeature(featureKey, role = getCurrentRole()) {
  const features = ROLE_FEATURES[role] || [];
  const allowedRoles = FEATURE_ALLOWED_ROLES[featureKey] || [];
  return features.includes(featureKey) && allowedRoles.includes(role);
}

function getFeatureList(role = getCurrentRole(), keys = []) {
  return keys
    .filter((key) => hasFeature(key, role) && FEATURE_META[key])
    .map((key) => ({ key, ...FEATURE_META[key] }));
}

function navigateByFeature(featureKey) {
  const feature = FEATURE_META[featureKey];
  if (!feature) return;
  if (feature.tab) {
    uni.switchTab({ url: feature.path });
    return;
  }
  uni.navigateTo({ url: feature.path });
}

function ensureRoleAccess(allowedRoles = [], message = '暂无权限访问该功能') {
  const role = getCurrentRole();
  if (allowedRoles.includes(role)) return true;
  uni.showToast({ title: message, icon: 'none' });
  setTimeout(() => {
    if (role === 'coach') {
      uni.switchTab({ url: '/pages/index/index' });
    } else {
      uni.switchTab({ url: '/pages/index/index' });
    }
  }, 500);
  return false;
}

export { ROLE_FEATURES, FEATURE_ALLOWED_ROLES, FEATURE_META, getCurrentUser, getCurrentRole, hasFeature, getFeatureList, navigateByFeature, ensureRoleAccess };
