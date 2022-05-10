import random
from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from Recipes.models import Ingredient, Recipe, RecipeIngredient, UserReview


class Command(BaseCommand):
    def handle(self, **options):
        # if Recipe.objects.first():
        # for r in Recipe.objects.all():
        #     r.delete()
        # for user in User.objects.all()
        # return None

        user = User.objects.create(
            username="super", email="super@user.com", password=make_password("tesT123")
        )
        user.is_superuser = True
        user.save()

        user1 = User.objects.create(
            username="user1", email="use2r@user.com", password=make_password("tesT123")
        )
        user1.is_superuser = False
        user1.save()

        user2 = User.objects.create(
            username="user2", email="user2@user.com", password=make_password("tesT123")
        )
        user2.is_superuser = False
        user2.save()

        recipe1 = Recipe.objects.create(
            name="First Recipe", description="First description", created_by_user=user1
        )
        recipe1.save()

        recipe2 = Recipe.objects.create(
            name="Second Recipe", description="Second description", created_by_user=user
        )
        recipe2.save()

        recipe3 = Recipe.objects.create(
            name="Third Recipe", description="Third description", created_by_user=user2
        )
        recipe3.save()

        for i in range(1, 30):
            if i % 3 == 0:
                u = user
                re = recipe1
            elif i % 3 == 1:
                u = user1
                re = recipe2
            else:
                u = user2
                re = recipe3
            ingredient = Ingredient.objects.create(
                name="Ingredient " + str(i), created_by_user=u
            )
            ingredient.save()
            RecipeIngredient.objects.create(
                quantity=i, recipe=re, ingredient=ingredient
            ).save()

            UserReview.objects.create(
                reviewed_on=make_aware(datetime.now()),
                user=user2,
                stars=random.randrange(100, 500) / 100,
                description="Testing purposes",
                recipe=recipe1,
            )
            UserReview.objects.create(
                reviewed_on=make_aware(datetime.now()),
                user=user,
                stars=random.randrange(100, 500) / 100,
                description="Testing purposes",
                recipe=recipe2,
            )
            UserReview.objects.create(
                reviewed_on=make_aware(datetime.now()),
                user=user1,
                stars=random.randrange(100, 500) / 100,
                description="Testing purposes",
                recipe=recipe3,
            )
