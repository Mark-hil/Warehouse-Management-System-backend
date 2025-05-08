from user_accounts.models import User, Permission

# Update admin user's role
admin = User.objects.get(username='admin')
admin.role = User.Roles.ADMIN
admin.save()

# Create admin permissions if they don't exist
try:
    Permission.objects.create(
        role=User.Roles.ADMIN,
        **Permission.get_default_permissions(User.Roles.ADMIN)
    )
except Exception as e:
    print(f"Note: Admin permissions already exist or error occurred: {str(e)}")

print(f"\nUpdated admin user:")
print(f"Username: {admin.username}")
print(f"Role: {admin.get_role_display()}")
print(f"Is Superuser: {admin.is_superuser}")
print(f"Is Staff: {admin.is_staff}")

# Show admin permissions
permissions = Permission.objects.filter(role=User.Roles.ADMIN).first()
if permissions:
    print("\nAdmin Permissions:")
    for field in permissions._meta.fields:
        if field.name.startswith('can_'):
            value = getattr(permissions, field.name)
            print(f"{field.name}: {value}")
