from django.contrib import admin

from . import models

admin.site.register(models.Ingredient)
admin.site.register(models.Recipe)
admin.site.register(models.RecipeIngredient)
admin.site.register(models.Rating)
admin.site.register(models.MealCourse)
admin.site.register(models.Cuisine)
admin.site.register(models.ShoppingCart)