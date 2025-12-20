test_user_register = {
    'username': 'Test',
    'email': 'test@test.com',
    'password': '123456',
}

test_admin_user_register = {
    'username': 'Test_admin',
    'email': 'admin@admin.com',
    'password': '123456',
    'is_staff': True,
}

test_other_user_register = {
    'username': 'Otheruser',
    'email': 'other@user.com',
    'password': 'otherpass',
}

test_user_login = {
    'email': 'test@test.com',
    'password': '123456',
}

test_admin_user_login = {
    'email': 'admin@admin.com',
    'password': '123456',
}

test_user_login_ivalid_data = {
    'email': 'doesnot@exist.com',
    'password': '12345',
}

test_tasks = {
    'title': 'Test',
    'description': 'Test description',
}

test_tasks2 = {
    'title': 'Test2',
    'description': 'Test description2',
}
