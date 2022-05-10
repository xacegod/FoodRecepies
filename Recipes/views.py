import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from datetime import datetime
from django.utils.timezone import make_aware
from django.db.models import Avg, Count

from .forms import (
    NewUserForm,
    EditRecipeForm,
    IngredientsForm,
    RecipeIngredientForm,
    EditWriteReview,
)
from .models import Ingredient, Recipe, UserReview, RecipeIngredient
from FoodRecepies.settings import HunterIoApiKey
import requests


@login_required(login_url="/login/")
def view_ingredients(request):
    if request.method == "POST":
        form = IngredientsForm(request.POST)
        if not form.is_valid():

            messages.error(request, "Unsuccessful - Invalid information.")
            return render(
                request=request,
                template_name="edit_recipe.html",
                context={"form": form},
            )
        ingredient = form.save(commit=False)
        ingredient.created_by_user = request.user
        ingredient.save()
        messages.success(request, "Successful.")
        return redirect("/recipe-ingredients")

    form = IngredientsForm()
    return render(
        request=request,
        template_name="ingredients.html",
        context={"form": form},
    )


@login_required(login_url="/login/")
def view_top_ingredients(request):
    temp = RecipeIngredient.objects.values('ingredient').annotate(count=Count('ingredient')).values('ingredient','count').order_by('-count').all()[:5]
    data = []
    for each in temp:
        a = Ingredient.objects.filter(id=each['ingredient']).first()
        each['name'] = a.name
        data.append(each)

    return render(
        request=request,
        template_name="top_ingredients.html",
        context={"data": data},
    )


@login_required(login_url="/login/")
def view_recipe_ingredients(request):
    if request.method == "POST":
        form = RecipeIngredientForm(request.POST)
        if request.user != Recipe.objects.filter(id=request.POST["recipe"]):
            messages.error(request, "Unsuccessful - Can only edit your own recipes")
            return render(
                request=request,
                template_name="edit_recipe.html",
                context={"form": form},
            )
        if not form.is_valid():
            messages.error(request, "Unsuccessful - Invalid information.")
            return render(
                request=request,
                template_name="edit_recipe.html",
                context={"form": form},
            )
        form.save()
        messages.success(request, "Successful.")
        return redirect("/recipe-ingredients")

    form = RecipeIngredientForm()
    return render(
        request=request,
        template_name="ingredients.html",
        context={"form": form},
    )


@login_required(login_url="/login/")
def edit_recipe_request(request, id):
    if not id:
        return redirect("/home")

    recipe = Recipe.objects.filter(id=id).first()
    if request.user != recipe.created_by_user:
        return redirect("/home")

    if request.method == "POST":
        form = EditRecipeForm(data=request.POST)
        if not form.is_valid():
            messages.error(request, "Unsuccessful - Invalid information.")
            return render(
                request=request,
                template_name="edit_recipe.html",
                context={"form": form},
            )
        form.save()
        messages.success(request, "Successful.")
        return redirect("/recipe_ingredients")

    form = EditRecipeForm(instance=recipe)
    return render(
        request=request,
        template_name="edit_recipe.html",
        context={"form": form},
    )


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)

        if not form.is_valid():
            messages.error(request, "Unsuccessful registration. Invalid information.")
            return render(
                request=request,
                template_name="register.html",
                context={"form": form},
            )

        response = requests.request(
            "GET",
            params=({"api_key": HunterIoApiKey, "email": form.cleaned_data["email"]}),
            url="https://api.hunter.io/v2/email-verifier",
        )
        if not response:
            messages.error(request, "Unsuccessful registration. Invalid information.")

        email_data = response.json()["data"]

        if (
            not email_data["mx_records"]
            or email_data["gibberish"]
            or email_data["disposable"]
            or email_data["status"] == "invalid"
        ):
            messages.error(request, "Unsuccessful registration. Invalid email.")
            return render(
                request=request,
                template_name="register.html",
                context={"form": form},
            )
        else:
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/home")

    else:
        form = NewUserForm()
        return render(
            request=request,
            template_name="register.html",
            context={"form": form},
        )


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="login.html", context={"login_form": form}
    )


@login_required(login_url="/login/")
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")


@login_required(login_url="/login/")
def recipes_list(request):
    page = request.GET.get("page", 1)
    paginator = Paginator(
        Recipe.objects.order_by("name")
        .annotate(avg_stars=Avg("userreview__stars"))
        .all(),
        10,
    )
    try:
        recipes = paginator.page(page)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)

    return render(request, "recipes_list.html", {"recipes": recipes})


@login_required(login_url="/login/")
def recipes_list_own(request):
    page = request.GET.get("page", 1)
    paginator = Paginator(
        Recipe.objects.filter(created_by_user=request.user)
        .annotate(avg_stars=Avg("userreview__stars"))
        .order_by("name")
        .all(),
        10,
    )
    try:
        recipes = paginator.page(page)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)

    return render(request, "recipes_list.html", {"recipes": recipes})


@login_required(login_url="/login/")
def item_detail(request, id):
    if not id:
        return redirect("/home")

    item = Recipe.objects.filter(id=id).first()
    if not item:
        return redirect("/home")
    return render(request, "ingredient_detail.html", {"item": item})


@login_required(login_url="/login/")
def review_recipe(request, id):
    if not id:
        return redirect("/home")

    recipe = Recipe.objects.filter(id=id).first()
    if not recipe or recipe.created_by_user == request.user:
        return redirect("/home")

    if request.method == "POST":
        form = EditWriteReview(request.POST)
        if request.user == recipe.created_by_user:
            messages.error(request, "Unsuccessful - Can only review other people's recipes")
            return render(
                request=request,
                template_name="review.html",
                context={"form": form, "recipe": recipe},
            )
        if not form.is_valid():
            messages.error(request, "Unsuccessful - Invalid information.")
            return render(
                request=request,
                template_name="review.html",
                context={"form": form, "recipe": recipe},
            )
        user_review = UserReview.objects.filter(recipe=recipe, user=request.user).first()
        if user_review:
            user_review.reviewed_on = make_aware(datetime.now())
            user_review.stars = request.POST['stars']
            user_review.description = request.POST['description']
            user_review.save()
        else:
            review = form.save(commit=False)
            review.recipe = recipe
            review.user = request.user
            review.reviewed_on = make_aware(datetime.now())
            review.save()

        messages.success(request, "Successful.")
        return render(
            request=request,
            template_name="review.html",
            context={"form": form, "recipe": recipe},
        )

    if UserReview.objects.filter(recipe=recipe, user=request.user).first():
        form = EditWriteReview(
            instance=UserReview.objects.filter(recipe=recipe, user=request.user).first()
        )
    else:
        form = EditWriteReview()

    return render(
        request=request,
        template_name="review.html",
        context={"form": form, "recipe": recipe},
    )
