from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from .models import User, Permission, Notification
from .serializers import UserSerializer, PermissionSerializer, NotificationSerializer

from rest_framework.exceptions import PermissionDenied

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['me', 'list', 'dashboard_stats']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def check_permissions(self, request):
        super().check_permissions(request)
        
        # Allow users to access their own data and dashboard stats
        if self.action in ['me', 'dashboard_stats']:
            return
            
        user = request.user
        if not user.is_authenticated:
            raise PermissionDenied('Authentication required')

        # Admin can do everything
        if user.is_admin:
            return

        # Warehouse managers can view users
        if self.action == 'list' and user.is_warehouse_manager:
            return

        # Team leads can only view their team members
        if self.action == 'list' and user.is_team_lead:
            self.queryset = self.queryset.filter(assigned_branch=user.assigned_branch)
            return

        # Approvers can view users for approval purposes
        if self.action == 'list' and user.is_approver:
            return

        raise PermissionDenied('You do not have permission to perform this action')

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='dashboard-stats')
    def dashboard_stats(self, request):

        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        staff_users = User.objects.filter(is_staff=True).count()

        # Get user activity data for the last 7 days
        from datetime import datetime, timedelta
        from django.utils import timezone
        from django.db.models import Count

        today = timezone.now().date()
        last_week = today - timedelta(days=7)
        
        # Get daily active users
        daily_activity = User.objects.filter(
            created_at__date__gte=last_week
        ).annotate(
            day=models.functions.TruncDate('created_at')
        ).values('day').annotate(
            active=Count('id', filter=models.Q(is_active=True))
        ).order_by('day')

        # Initialize activity data for all days
        activity_by_day = {}
        for i in range(8):
            day = last_week + timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            activity_by_day[day_str] = {
                'day': day_str,
                'active': 0,
                'new': 0,
                'inactive': 0
            }

        # Fill in actual values
        for entry in daily_activity:
            day_str = entry['day'].strftime('%Y-%m-%d')
            if day_str in activity_by_day:
                activity_by_day[day_str]['active'] = entry['active']

        # Get new users per day
        new_users = User.objects.filter(
            created_at__date__gte=last_week
        ).annotate(
            day=models.functions.TruncDate('created_at')
        ).values('day').annotate(
            new=Count('id')
        ).order_by('day')

        for entry in new_users:
            day_str = entry['day'].strftime('%Y-%m-%d')
            if day_str in activity_by_day:
                activity_by_day[day_str]['new'] = entry['new']

        # Calculate inactive users
        for day_data in activity_by_day.values():
            day_data['inactive'] = total_users - day_data['active']

        return Response({
            'total_users': total_users,
            'active_users': active_users,
            'staff_users': staff_users,
            'monthly_stats': [
                {'month': 'Jan', 'users': total_users - 20},
                {'month': 'Feb', 'users': total_users - 15},
                {'month': 'Mar', 'users': total_users - 10},
                {'month': 'Apr', 'users': total_users - 5},
                {'month': 'May', 'users': total_users}
            ],
            'role_distribution': [
                {'role': 'Admin', 'count': staff_users},
                {'role': 'Requester', 'count': total_users - staff_users}
            ],
            'user_activity': list(activity_by_day.values())
        })

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
