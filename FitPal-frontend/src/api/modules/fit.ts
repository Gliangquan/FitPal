import request from '../request';
import type { BaseResponse, PageData } from '../types';

export interface FitHealthRecord {
  id?: number;
  userId?: number;
  recordDate?: string;
  weightKg: number;
  bodyFatRate?: number;
  calorieIntake?: number;
  calorieBurn?: number;
  sleepHours?: number;
  note?: string;
  createTime?: string;
  updateTime?: string;
}

export interface HealthReportSummary {
  recordCount: number;
  startWeight?: number;
  endWeight?: number;
  weightDelta?: number;
  avgBodyFatRate?: number;
}

export interface HealthReport {
  records: FitHealthRecord[];
  summary: HealthReportSummary;
}

export interface QuestionnaireSubmitRequest {
  age?: number;
  gender?: string;
  heightCm?: number;
  currentWeightKg: number;
  targetWeightKg: number;
  goalCycleDays?: number;
  dietPreference?: string;
  sportPreference?: string;
  intensity?: string;
  healthCondition?: string;
  answerJson?: string;
}

export interface FitUserQuestionnaire extends QuestionnaireSubmitRequest {
  id?: number;
  userId?: number;
  createTime?: string;
  updateTime?: string;
}

export interface FitPersonalizedPlan {
  id?: number;
  userId?: number;
  questionnaireId?: number;
  planType?: string;
  bmr?: number;
  dailyCalorieTarget?: number;
  dietSuggestion?: string;
  workoutSuggestion?: string;
  seasonTips?: string;
  source?: string;
  effectiveFrom?: string;
  effectiveTo?: string;
  createTime?: string;
  updateTime?: string;
}

export interface FitSolarTermTopic {
  id: number;
  termName?: string;
  title?: string;
  recipeText?: string;
  sportGuide?: string;
  routineAdvice?: string;
  startDate?: string;
  endDate?: string;
  status?: string;
  createTime?: string;
  updateTime?: string;
}

export interface FitRecommendationContent {
  id: number;
  title: string;
  contentType?: string;
  stageTag?: string;
  bodyTag?: string;
  summary?: string;
  contentUrl?: string;
  contentBody?: string;
  tags?: string;
  publishStatus?: string;
  createTime?: string;
  updateTime?: string;
}

export interface CommunityPostAddRequest {
  title: string;
  content: string;
  category?: string;
  imageUrls?: string;
}

export interface FitCommunityPost {
  id: number;
  userId: number;
  title: string;
  content: string;
  category?: string;
  imageUrls?: string;
  imageList?: string[];
  likeCount?: number;
  commentCount?: number;
  viewCount?: number;
  status?: string;
  createTime?: string;
  updateTime?: string;
  authorName?: string;
  authorAvatar?: string;
  userName?: string;
  userAvatar?: string;
}

export interface FitCommunityCommentView {
  id: number;
  postId: number;
  userId: number;
  content: string;
  createTime?: string;
  authorName?: string;
  authorAvatar?: string;
}

export interface FitUserPointAccount {
  id?: number;
  userId?: number;
  totalPoint?: number;
  availablePoint?: number;
  levelName?: string;
  createTime?: string;
  updateTime?: string;
}

export interface FitUserPointLog {
  id?: number;
  userId?: number;
  taskCode?: string;
  taskName?: string;
  pointChange?: number;
  bizDate?: string;
  remark?: string;
  createTime?: string;
}

export interface PointInfo {
  account: FitUserPointAccount;
  logs: FitUserPointLog[];
}

export interface CoachCertificationApplyRequest {
  realName: string;
  certificateType: string;
  certificateNo: string;
  specialties?: string;
  introduction?: string;
}

export interface FitCoachProfile {
  id?: number;
  userId?: number;
  realName?: string;
  certificateType?: string;
  certificateNo?: string;
  specialties?: string;
  introduction?: string;
  status?: string;
  passedTime?: string;
  rejectReason?: string;
  createTime?: string;
  updateTime?: string;
}

export interface ConsultationCreateRequest {
  coachUserId?: number;
  question: string;
}

export interface ConsultationReplyRequest {
  reply: string;
}

export interface FitCoachConsultation {
  id: number;
  userId: number;
  coachUserId?: number;
  question: string;
  reply?: string;
  status?: string;
  createTime?: string;
  replyTime?: string;
  updateTime?: string;
}

export interface AdminDashboard {
  userCount: number;
  coachCount: number;
  healthLogCount: number;
  communityPostCount: number;
  coachApplicationStats: Record<string, number>;
  contentStats: Record<string, number>;
}

export interface ReviewPayload {
  action: string;
  reason?: string;
}

export interface CoachApplicationCrudRequest {
  id?: number;
  userId?: number;
  realName?: string;
  certificateType?: string;
  certificateNo?: string;
  specialties?: string;
  introduction?: string;
  status?: string;
  rejectReason?: string;
}

export interface ContentCrudRequest {
  id?: number;
  title?: string;
  contentType?: string;
  stageTag?: string;
  bodyTag?: string;
  summary?: string;
  contentUrl?: string;
  contentBody?: string;
  tags?: string;
  publishStatus?: string;
}

export interface PlanCrudRequest {
  id?: number;
  userId?: number;
  questionnaireId?: number;
  planType?: string;
  targetCalories?: number;
  dietPlan?: string;
  exercisePlan?: string;
  lifestyleTips?: string;
  source?: string;
  effectiveFrom?: string;
  effectiveTo?: string;
}

export interface CoachPlanItem {
  id: number;
  userId: number;
  userNickname: string;
  targetCalories?: number;
  status: string;
  createdAt?: string;
  dietPlan?: string;
  exercisePlan?: string;
  lifestyleTips?: string;
  coachNote?: string;
}

export interface CoachPlanListResult {
  records: CoachPlanItem[];
  total: number;
  current: number;
  size: number;
}

export interface OptimizePlanPayload {
  dietPlan?: string;
  exercisePlan?: string;
  lifestyleTips?: string;
  coachNote?: string;
}

export function addHealthRecord(data: FitHealthRecord): Promise<BaseResponse<FitHealthRecord>> {
  return request.post('/fit/health/record', data) as Promise<BaseResponse<FitHealthRecord>>;
}

export function listHealthRecords(days = 30): Promise<BaseResponse<FitHealthRecord[]>> {
  return request.get('/fit/health/records', { params: { days } }) as Promise<BaseResponse<FitHealthRecord[]>>;
}

export function getHealthReport(days = 30): Promise<BaseResponse<HealthReport>> {
  return request.get('/fit/health/report', { params: { days } }) as Promise<BaseResponse<HealthReport>>;
}

export function submitQuestionnaire(data: QuestionnaireSubmitRequest): Promise<BaseResponse<FitUserQuestionnaire>> {
  return request.post('/fit/questionnaire/submit', data) as Promise<BaseResponse<FitUserQuestionnaire>>;
}

export function generatePlan(): Promise<BaseResponse<FitPersonalizedPlan>> {
  return request.post('/fit/plan/generate') as Promise<BaseResponse<FitPersonalizedPlan>>;
}

export function getLatestPlan(): Promise<BaseResponse<FitPersonalizedPlan>> {
  return request.get('/fit/plan/latest') as Promise<BaseResponse<FitPersonalizedPlan>>;
}

export function getCurrentSeasonTopic(): Promise<BaseResponse<FitSolarTermTopic | FitSolarTermTopic[]>> {
  return request.get('/fit/season/topic/current') as Promise<BaseResponse<FitSolarTermTopic | FitSolarTermTopic[]>>;
}

export function recommendContent(stageTag?: string, limit = 8): Promise<BaseResponse<FitRecommendationContent[]>> {
  return request.get('/fit/content/recommend', { params: { stageTag, limit } }) as Promise<BaseResponse<FitRecommendationContent[]>>;
}

export function addCommunityPost(data: CommunityPostAddRequest): Promise<BaseResponse<FitCommunityPost>> {
  return request.post('/fit/community/post', data) as Promise<BaseResponse<FitCommunityPost>>;
}

export function listCommunityPosts(current = 1, size = 10): Promise<BaseResponse<PageData<FitCommunityPost>>> {
  return request.get('/fit/community/posts', { params: { current, size } }) as Promise<BaseResponse<PageData<FitCommunityPost>>>;
}

export function getCommunityPostDetail(postId: number): Promise<BaseResponse<FitCommunityPost>> {
  return request.get(`/fit/community/post/${postId}`) as Promise<BaseResponse<FitCommunityPost>>;
}

export function likeCommunityPost(postId: number): Promise<BaseResponse<boolean>> {
  return request.post(`/fit/community/post/${postId}/like`) as Promise<BaseResponse<boolean>>;
}

export function commentCommunityPost(postId: number, content: string): Promise<BaseResponse<boolean>> {
  return request.post(`/fit/community/post/${postId}/comment`, { content }) as Promise<BaseResponse<boolean>>;
}

export function listCommunityComments(postId: number, size = 20): Promise<BaseResponse<FitCommunityCommentView[]>> {
  return request.get(`/fit/community/post/${postId}/comments`, { params: { size } }) as Promise<BaseResponse<FitCommunityCommentView[]>>;
}

export function dailyCheckin(): Promise<BaseResponse<FitUserPointAccount>> {
  return request.post('/fit/points/checkin') as Promise<BaseResponse<FitUserPointAccount>>;
}

export function myPoints(): Promise<BaseResponse<PointInfo>> {
  return request.get('/fit/points/me') as Promise<BaseResponse<PointInfo>>;
}

export function applyCoachCertification(data: CoachCertificationApplyRequest): Promise<BaseResponse<FitCoachProfile>> {
  return request.post('/fit/coach/certification/apply', data) as Promise<BaseResponse<FitCoachProfile>>;
}

export function myCoachCertification(): Promise<BaseResponse<FitCoachProfile>> {
  return request.get('/fit/coach/certification/me') as Promise<BaseResponse<FitCoachProfile>>;
}

export function createConsultation(data: ConsultationCreateRequest): Promise<BaseResponse<FitCoachConsultation>> {
  return request.post('/fit/coach/consultation/create', data) as Promise<BaseResponse<FitCoachConsultation>>;
}

export function myConsultations(): Promise<BaseResponse<FitCoachConsultation[]>> {
  return request.get('/fit/coach/consultations') as Promise<BaseResponse<FitCoachConsultation[]>>;
}

export function todoConsultations(): Promise<BaseResponse<FitCoachConsultation[]>> {
  return request.get('/fit/coach/consultation/todo') as Promise<BaseResponse<FitCoachConsultation[]>>;
}

export function replyConsultation(id: number, data: ConsultationReplyRequest): Promise<BaseResponse<boolean>> {
  return request.post(`/fit/coach/consultation/${id}/reply`, data) as Promise<BaseResponse<boolean>>;
}

export function adminDashboard(): Promise<BaseResponse<AdminDashboard>> {
  return request.get('/fit/admin/dashboard') as Promise<BaseResponse<AdminDashboard>>;
}

export function listCoachApplications(status?: string, current = 1, size = 20): Promise<BaseResponse<PageData<FitCoachProfile>>> {
  return request.get('/fit/admin/coach/applications', { params: { status, current, size } }) as Promise<BaseResponse<PageData<FitCoachProfile>>>;
}

export function reviewCoachApplication(id: number, data: ReviewPayload): Promise<BaseResponse<boolean>> {
  return request.post(`/fit/admin/coach/${id}/review`, data) as Promise<BaseResponse<boolean>>;
}

export function addCoachApplication(data: CoachApplicationCrudRequest): Promise<BaseResponse<number>> {
  return request.post('/fit/admin/coach/applications/add', data) as Promise<BaseResponse<number>>;
}

export function updateCoachApplication(data: CoachApplicationCrudRequest): Promise<BaseResponse<boolean>> {
  return request.post('/fit/admin/coach/applications/update', data) as Promise<BaseResponse<boolean>>;
}

export function deleteCoachApplication(id: number): Promise<BaseResponse<boolean>> {
  return request.post('/fit/admin/coach/applications/delete', { id }) as Promise<BaseResponse<boolean>>;
}

export function listAdminContents(status?: string, current = 1, size = 20): Promise<BaseResponse<PageData<FitRecommendationContent>>> {
  return request.get('/fit/admin/contents', { params: { status, current, size } }) as Promise<BaseResponse<PageData<FitRecommendationContent>>>;
}

export function reviewContent(id: number, data: ReviewPayload): Promise<BaseResponse<boolean>> {
  return request.post(`/fit/admin/contents/${id}/review`, data) as Promise<BaseResponse<boolean>>;
}

export function addAdminContent(data: ContentCrudRequest): Promise<BaseResponse<number>> {
  return request.post('/fit/admin/contents/add', data) as Promise<BaseResponse<number>>;
}

export function updateAdminContent(data: ContentCrudRequest): Promise<BaseResponse<boolean>> {
  return request.post('/fit/admin/contents/update', data) as Promise<BaseResponse<boolean>>;
}

export function deleteAdminContent(id: number): Promise<BaseResponse<boolean>> {
  return request.post('/fit/admin/contents/delete', { id }) as Promise<BaseResponse<boolean>>;
}

export function listAdminCommunityPosts(
  status?: string,
  category?: string,
  keyword?: string,
  current = 1,
  size = 20
): Promise<BaseResponse<PageData<FitCommunityPost>>> {
  return request.get('/fit/admin/community/posts', {
    params: { status, category, keyword, current, size }
  }) as Promise<BaseResponse<PageData<FitCommunityPost>>>;
}

export function reviewCommunityPost(id: number, data: ReviewPayload): Promise<BaseResponse<boolean>> {
  return request.post(`/fit/admin/community/post/${id}/review`, data) as Promise<BaseResponse<boolean>>;
}

export function listCoachPlans(status?: string, userId?: number, current = 1, size = 10): Promise<BaseResponse<CoachPlanListResult>> {
  return request.get('/fit/coach/plans', { params: { status, userId, current, size } }) as Promise<BaseResponse<CoachPlanListResult>>;
}

export function optimizePlan(id: number, data: OptimizePlanPayload): Promise<BaseResponse<boolean>> {
  return request.put(`/fit/coach/plans/${id}/optimize`, data) as Promise<BaseResponse<boolean>>;
}

export function addAdminPlan(data: PlanCrudRequest): Promise<BaseResponse<number>> {
  return request.post('/fit/admin/plans/add', data) as Promise<BaseResponse<number>>;
}

export function updateAdminPlan(data: PlanCrudRequest): Promise<BaseResponse<boolean>> {
  return request.post('/fit/admin/plans/update', data) as Promise<BaseResponse<boolean>>;
}

export function deleteAdminPlan(id: number): Promise<BaseResponse<boolean>> {
  return request.post('/fit/admin/plans/delete', { id }) as Promise<BaseResponse<boolean>>;
}
