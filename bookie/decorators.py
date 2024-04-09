from django.shortcuts import redirect


def allowed_users(allowed_roles: list):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            current_role = None

            if request.user.is_superuser:
                current_role = 'superuser'
            elif request.user.is_staff:
                current_role = 'staff'
            elif request.user.is_authenticated:
                current_role = 'auth user'

            else:
                return redirect('not allowed')

            if current_role in allowed_roles:
                return view_func(request, *args, **kwargs)
        return wrapper_func

    return decorator


def custom_login_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login bookie')