from user_accounts.models import User

# Create regular users
users = [
    {
        'username': 'john',
        'email': 'john@example.com',
        'password': 'john123',
        'first_name': 'John',
        'last_name': 'Doe',
        'is_staff': False,
    },
    {
        'username': 'jane',
        'email': 'jane@example.com',
        'password': 'jane123',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'is_staff': True,
    },
    {
        'username': 'warehouse_manager',
        'email': 'manager@example.com',
        'password': 'manager123',
        'first_name': 'Mike',
        'last_name': 'Johnson',
        'is_staff': True,
    }
]

for user_data in users:
    try:
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
        )
        user.is_staff = user_data['is_staff']
        user.save()
        print(f"Created user: {user.username}")
    except Exception as e:
        print(f"Error creating user {user_data['username']}: {str(e)}")

print("\nAll users in the system:")
for user in User.objects.all():
    print(f"Username: {user.username}, Email: {user.email}, Name: {user.first_name} {user.last_name}, Is Staff: {user.is_staff}")
