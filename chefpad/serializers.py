from rest_framework import serializers

from . import models


class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cuisine
        fields = ['id','name']
    
class MealCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MealCourse
        fields = ['id','name']

class RecipeSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    def get_author_name(self,obj):
        return obj.author.username

    class Meta:
        model = models.Recipe
        fields = ['id','name','author','author_name','description','image','instructions','prep_time','cook_time','servings','publish_date','is_public']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = ['id','name']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecipeIngredient
        fields = ['id','recipe','ingredient','quantity']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rating
        fields = ['id','user','recipe','rating','comment_headline','comment_body']