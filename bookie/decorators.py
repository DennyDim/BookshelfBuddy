from django.shortcuts import redirect


def allowed_users(allowed_roles: list):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            current_role = None

            if request.user.groups.exists():
                current_role = request.user.groups.all()[0].name

            if current_role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('not allowed')

        return wrapper_func

    return decorator


def custom_login_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login bookie')