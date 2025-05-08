from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views, auth_views

router = DefaultRouter()
router.register(r'', views.UserViewSet, basename='user')
router.register(r'permissions', views.PermissionViewSet)
router.register(r'notifications', views.NotificationViewSet)

urlpatterns = [
    path('auth/token/login/', auth_views.login, name='auth_login'),
    path('auth/token/logout/', auth_views.logout, name='auth_logout'),
    path('dashboard-stats/', views.UserViewSet.as_view({'get': 'dashboard_stats'}), name='dashboard-stats'),
    path('me/', views.UserViewSet.as_view({'get': 'me'}), name='user-me'),
] + router.urls
