from django.contrib.auth.decorators import user_passes_test

def manager_or_admin_required(view_func):
    def check(user):
        return user.is_authenticated and (user.is_staff or user.groups.filter(name='manager').exists())

    return user_passes_test(check)(view_func)