from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Recipes.models import Recipe, Ingredient, RecipeIngredient, UserReview


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = "__all__"


class IngredientsForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name"]


class EditRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ["created_by_user", "created_at"]


class EditWriteReview(forms.ModelForm):
    class Meta:
        model = UserReview
        fields = ["stars", "description"]
