import { createRouter, createWebHistory } from 'vue-router';
import { getLoginUser } from '../api';

import LayoutView from '../views/LayoutView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import UserManagementView from '../views/admin/UserManagementView.vue';
import CoachApplicationView from '../views/admin/CoachApplicationView.vue';
import ContentReviewView from '../views/admin/ContentReviewView.vue';
import PlanManagementView from '../views/admin/PlanManagementView.vue';
import ProfileCenterView from '../views/admin/ProfileCenterView.vue';
import CommunityModerationView from '../views/admin/CommunityModerationView.vue';
import PointsManagementView from '../views/admin/PointsManagementView.vue';
import StatisticsView from '../views/admin/StatisticsView.vue';
import SystemSettingsView from '../views/admin/SystemSettingsView.vue';
import SolarTermManagementView from '../views/admin/SolarTermManagementView.vue';
import ContentManagementView from '../views/admin/ContentManagementView.vue';

const routes = [
  {
    path: '/login',
    component: LoginView,
    meta: { public: true },
  },
  {
    path: '/register',
    component: RegisterView,
    meta: { public: true },
  },
  {
    path: '/',
    redirect: '/admin/users',
  },
  {
    path: '/admin',
    component: LayoutView,
    children: [
      {
        path: 'users',
        component: UserManagementView,
      },
      {
        path: 'coach-applications',
        component: CoachApplicationView,
      },
      {
        path: 'content-review',
        component: ContentReviewView,
      },
      {
        path: 'community-moderation',
        component: CommunityModerationView,
      },
      {
        path: 'plans',
        component: PlanManagementView,
      },
      {
        path: 'points',
        component: PointsManagementView,
      },
      {
        path: 'statistics',
        component: StatisticsView,
      },
      {
        path: 'settings',
        component: SystemSettingsView,
      },
      {
        path: 'solar-terms',
        component: SolarTermManagementView,
      },
      {
        path: 'content',
        component: ContentManagementView,
      },
      {
        path: 'profile',
        component: ProfileCenterView,
      },
      {
        path: '',
        redirect: '/admin/users',
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/admin/users',
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, _from, next) => {
  if (to.meta.public) {
    next();
    return;
  }

  try {
    const res = await getLoginUser();
    const loginUser = res?.data;
    if (!loginUser || !loginUser.id) {
      next('/login');
      return;
    }

    let cachedToken;
    try {
      const cachedUser = JSON.parse(localStorage.getItem('user') || '{}');
      cachedToken = cachedUser?.token;
    } catch (_error) {
      cachedToken = undefined;
    }
    const nextUser = loginUser?.token ? loginUser : { ...loginUser, token: cachedToken };
    localStorage.setItem('user', JSON.stringify(nextUser));

    if (loginUser.userRole !== 'admin') {
      next('/login');
      return;
    }

    next();
  } catch (error) {
    localStorage.removeItem('user');
    next('/login');
  }
});

export default router;
