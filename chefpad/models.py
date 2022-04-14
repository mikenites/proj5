from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

class Cuisine(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MealCourse(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ingredient(models.Model):

    GRAM = 'GR'
    TABLESPOON = 'TB'
    TEASPOON = 'TSP'
    MEASUREMENT_UNIT_CHOICES = [
        (GRAM,'grams'),
        (TEASPOON,'Tb'),
        (TEASPOON,'tsp'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    plural_name = models.CharField(max_length=100,null=True)
    measurement_unit = models.CharField(max_length=3,choices=MEASUREMENT_UNIT_CHOICES,default=GRAM)

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            'name':self.name,
            'description':self.description,
            'measurement_unit':self.measurement_unit
        }

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    cuisine = models.ForeignKey(Cuisine,on_delete=models.CASCADE,null=True)
    meal_course = models.ForeignKey(MealCourse,on_delete=models.CASCADE,null=True)
    description = models.TextField(null=True)
    image = models.URLField(null=True)
    instructions = models.TextField(null=True)
    prep_time = models.SmallIntegerField(null=True)
    cook_time = models.SmallIntegerField(null=True)
    servings = models.SmallIntegerField(null=True)
    publish_date = models.DateField(null=True)
    is_public = models.BooleanField(null=True)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.author.username + ' - ' + self.name

    def serialize(self):
        return {
            'id':self.id,
            'name':self.name,
            'author':self.author.username,
            'cuisine':self.cuisine.name,
            'meal_course':self.meal_course.name,
            'description':self.description,
            'image':self.image,
            'instructions':self.instructions,
            'prep_time':self.prep_time,
            'cook_time':self.cook_time,
            'servings':self.servings,
            'publish_date':self.publish_date,
            'is_public':self.is_public
        }

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,related_name='recipeingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,related_name='ingredients')
    quantity = models.DecimalField(max_digits=20,decimal_places=2)

    def __str__(self):
        return self.recipe.author.username + ' - '  + self.recipe.name + ' - '+ self.ingredient.name

    def serialize(self):
        return {
            'quantity':self.quantity,
            'name':self.ingredient.name,
            'description':self.ingredient.description,
            'measurement_unit':self.ingredient.measurement_unit
        }

class Rating(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE,null=True)
    rating = models.PositiveSmallIntegerField(default=5,validators=[MaxValueValidator(5)])
    comment_headline = models.CharField(max_length=100)
    comment_body = models.TextField()

class ShoppingCart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE,null=True)