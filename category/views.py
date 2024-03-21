from django.contrib.auth import get_user_model
from django.shortcuts import render

from category.models import Category



UserModel = get_user_model()


def main_page(request):

    user_age = None
    filtered_categories = []

    categories = Category.objects.all()

    if request.user.is_authenticated:
        user_age = request.user.age

    for category in categories:
        # handling scenario when we have ar and the user is old enough
        if category.age_restriction and user_age:
            if user_age >= category.age_restriction:
                filtered_categories.append(category)
        # handling a scenario when we don`t have ar
        elif category.age_restriction is None:
            filtered_categories.append(category)

    context = {
        "categories": filtered_categories,
    }

    return render(request, "main_page.html", context)