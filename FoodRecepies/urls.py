"""FoodRecepies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path  # , include

from Recipes import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('/', include('Recipes.urls')),
    # path('', views.login, name = 'login'),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("home/", views.recipes_list, name="home"),
    path("my-recipes/", views.recipes_list_own, name="own"),
    path("item-detial/<int:id>/", views.item_detail, name="item_detail"),
    path("edit-recipe/<int:id>/", views.edit_recipe_request, name="edit_recipe"),
    path("ingredients", views.view_ingredients, name="ingredients"),
    path(
        "recipe-ingredients", views.view_recipe_ingredients, name="recipe_ingredients"
    ),
    path("top-ingredients", views.view_top_ingredients, name="recipe_ingredients"),
    path("review-recipe/<int:id>/", views.review_recipe, name="review_recipe"),
]
