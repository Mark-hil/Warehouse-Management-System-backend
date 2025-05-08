from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        WAREHOUSE_MANAGER = 'warehouse_manager', 'Warehouse Manager'
        TEAM_LEAD = 'team_lead', 'Team Lead'
        APPROVER = 'approver', 'Approver'

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.TEAM_LEAD
    )
    assigned_branch = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    @property
    def is_warehouse_manager(self):
        return self.role == self.Roles.WAREHOUSE_MANAGER

    @property
    def is_team_lead(self):
        return self.role == self.Roles.TEAM_LEAD

    @property
    def is_approver(self):
        return self.role == self.Roles.APPROVER

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'

class Permission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    role = models.CharField(
        max_length=20,
        choices=User.Roles.choices,
        unique=True
    )
    # Inventory Management
    can_view_inventory = models.BooleanField(default=False)
    can_manage_inventory = models.BooleanField(default=False)
    can_approve_inventory = models.BooleanField(default=False)
    
    # Procurement
    can_view_procurement = models.BooleanField(default=False)
    can_create_request = models.BooleanField(default=False)
    can_approve_request = models.BooleanField(default=False)
    
    # Warehouse Operations
    can_manage_transfers = models.BooleanField(default=False)
    can_manage_returns = models.BooleanField(default=False)
    can_view_reports = models.BooleanField(default=False)
    
    # User Management
    can_manage_users = models.BooleanField(default=False)
    can_assign_roles = models.BooleanField(default=False)

    class Meta:
        db_table = 'permissions'

    @classmethod
    def get_default_permissions(cls, role):
        if role == User.Roles.ADMIN:
            return {
                'can_view_inventory': True,
                'can_manage_inventory': True,
                'can_approve_inventory': True,
                'can_view_procurement': True,
                'can_create_request': True,
                'can_approve_request': True,
                'can_manage_transfers': True,
                'can_manage_returns': True,
                'can_view_reports': True,
                'can_manage_users': True,
                'can_assign_roles': True
            }
        elif role == User.Roles.WAREHOUSE_MANAGER:
            return {
                'can_view_inventory': True,
                'can_manage_inventory': True,
                'can_view_procurement': True,
                'can_create_request': True,
                'can_manage_transfers': True,
                'can_manage_returns': True,
                'can_view_reports': True
            }
        elif role == User.Roles.TEAM_LEAD:
            return {
                'can_view_inventory': True,
                'can_view_procurement': True,
                'can_create_request': True,
                'can_view_reports': True
            }
        elif role == User.Roles.APPROVER:
            return {
                'can_view_inventory': True,
                'can_view_procurement': True,
                'can_approve_request': True,
                'can_view_reports': True
            }
        return {}

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}..."
