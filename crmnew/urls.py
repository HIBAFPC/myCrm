from django.urls import path
# from rest_framework.routers import DefaultRouter
from . import views
from .views import LoginView,RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    
  
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),

   
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),

    path('leads/', views.LeadListCreateView.as_view(), name='lead-list-create'),
    path('leads/<int:pk>/', views.LeadDetailView.as_view(), name='lead-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    
    path('activities/', views.ActivityListCreateView.as_view(), name='activity-list-create'),
    path('activities/<int:pk>/', views.ActivityDetailView.as_view(), name='activity-detail'),


    path('deals/', views.DealListCreateView.as_view(), name='deal-list-create'),
    path('deals/<int:pk>/', views.DealDetailView.as_view(), name='deal-detail'),

    path('tasks/', views.TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    
    path('lead-status/', views.LeadStatusListCreateView.as_view(), name='lead-status-list'),
    path('lead-status/<int:pk>/', views.LeadStatusDetailView.as_view(), name='lead-status-detail'),
   
    path('deal-stages/', views.DealStageListCreateView.as_view(), name='deal-stage-list'),
    path('deal-stages/<int:pk>/', views.DealStageDetailView.as_view(), name='deal-stage-detail'),
    
    path('task-status/', views.TaskStatusListCreateView.as_view(), name='task-status-list'),
    
    path('contactinfos/', views.ContactInfoListCreateView.as_view(), name='contactinfo-list'),
    path('contactinfos/<int:pk>/', views.ContactInfoDetailView.as_view(), name='contactinfo-detail'),
    
] 