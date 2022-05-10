from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Recipe(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=False)
    text = models.TextField(max_length=500, blank=True)
    created_by_user = models.ForeignKey(
        User, unique=False, on_delete=models.SET_NULL, null=True, blank=False
    )
    created_at = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return "%s %s %s" % (self.name, self.created_by_user, self.created_at)


class Ingredient(models.Model):
    name = models.CharField(
        max_length=50,
        blank=False,
        unique=True,
        help_text="Specify the name of ingredient used in recipe. Max 50 chars.",
    )
    created_by_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, unique=False
    )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    quantity = models.CharField(
        max_length=50,
        blank=True,
        unique=False,
        help_text="Quantity of said ingredient that goes into recipe. "
        "Write also unit of measurement. Max length of 50.",
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, null=False, blank=False
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, null=False, blank=False
    )

    def __str__(self):
        return "%s - %s - Recipe: %s" % (
            self.ingredient.name,
            self.quantity,
            self.recipe.name,
        )


class UserReview(models.Model):
    reviewed_on = models.DateTimeField(default=timezone.now, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    stars = models.DecimalField(
        max_digits=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        decimal_places=2,
        help_text="Rating for recipe. Can go from 1 to 5.",
    )
    description = models.TextField(
        max_length=500, blank=True, null=True, help_text="Write more details"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, null=False, blank=False
    )

    def __str__(self):
        return "%s - Recipe: %s - %s" % (
            self.user.username,
            self.recipe.name,
            self.stars,
        )
