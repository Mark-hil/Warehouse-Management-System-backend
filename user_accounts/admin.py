from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Permission, Notification

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'assigned_branch', 'is_active', 'is_staff', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff', 'assigned_branch')
    search_fields = ('username', 'email', 'assigned_branch')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('role', 'assigned_branch')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'created_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'assigned_branch'),
        }),
    )
    
    readonly_fields = ('created_at',)

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = (
        'role',
        'can_view_inventory',
        'can_manage_inventory',
        'can_approve_inventory',
        'can_view_procurement',
        'can_create_request',
        'can_approve_request',
        'can_manage_users'
    )
    list_filter = ('role',)
    
    fieldsets = (
        (_('Role'), {'fields': ('role',)}),
        (_('Inventory Permissions'), {
            'fields': ('can_view_inventory', 'can_manage_inventory', 'can_approve_inventory'),
        }),
        (_('Procurement Permissions'), {
            'fields': ('can_view_procurement', 'can_create_request', 'can_approve_request'),
        }),
        (_('Warehouse Permissions'), {
            'fields': ('can_manage_transfers', 'can_manage_returns', 'can_view_reports'),
        }),
        (_('User Management'), {
            'fields': ('can_manage_users', 'can_assign_roles'),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new permission
            default_permissions = Permission.get_default_permissions(obj.role)
            for field, value in default_permissions.items():
                setattr(obj, field, value)
        super().save_model(request, obj, form, change)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
    ordering = ('-created_at',)
