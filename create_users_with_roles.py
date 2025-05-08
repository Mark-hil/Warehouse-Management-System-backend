from user_accounts.models import User, Permission

# Create users with different roles
users = [
    {
        'username': 'john_manager',
        'email': 'john@warehouse.com',
        'password': 'manager123',
        'first_name': 'John',
        'last_name': 'Manager',
        'role': User.Roles.WAREHOUSE_MANAGER,
        'assigned_branch': 'Main Warehouse'
    },
    {
        'username': 'sarah_lead',
        'email': 'sarah@team.com',
        'password': 'lead123',
        'first_name': 'Sarah',
        'last_name': 'Lead',
        'role': User.Roles.TEAM_LEAD,
        'assigned_branch': 'Main Warehouse'
    },
    {
        'username': 'mike_approver',
        'email': 'mike@approvals.com',
        'password': 'approver123',
        'first_name': 'Mike',
        'last_name': 'Approver',
        'role': User.Roles.APPROVER,
        'assigned_branch': 'Main Warehouse'
    }
]

# Create users and their permissions
for user_data in users:
    try:
        # Create user
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            role=user_data['role'],
            assigned_branch=user_data['assigned_branch']
        )
        
        # Get default permissions for the role
        permissions = Permission.get_default_permissions(user_data['role'])
        
        # Create permission entry
        Permission.objects.create(
            role=user_data['role'],
            **permissions
        )
        
        print(f"Created user: {user.username} with role: {user.role}")
        
    except Exception as e:
        print(f"Error creating user {user_data['username']}: {str(e)}")

print("\nAll users in the system:")
for user in User.objects.all().order_by('username'):
    print(f"Username: {user.username}")
    print(f"Role: {user.get_role_display()}")
    print(f"Email: {user.email}")
    print(f"Name: {user.first_name} {user.last_name}")
    print(f"Branch: {user.assigned_branch}")
    print("---")
