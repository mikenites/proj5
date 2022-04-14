from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from datetime import date, datetime

from . import models
from . import serializers

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

@login_required
def index(request):
    return render(request, "chefpad/index.html")

class RecipeRetrieve(generics.RetrieveAPIView):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

class IngredientRetrieve(generics.RetrieveAPIView):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

class IngredientList(generics.ListAPIView):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

class RecipeIngredientViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeIngredientSerializer
    lookup_fields = ('recipe_id','ingredient_id')
    lookup_url_kwargs = ('recipe_id','ingredient_id')

    def get_queryset(self):
        return models.RecipeIngredient.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwargs = self.lookup_url_kwargs or self.lookup_fields

        assert all(
            lookup_kwarg in self.kwargs
            for lookup_kwarg in lookup_url_kwargs
        ), ((self.__class__.__name__, ','.join(lookup_url_kwargs)))

        field_values = (self.kwargs[lookup_kwarg] for lookup_kwarg in lookup_url_kwargs)
        filter_kwargs = dict(zip(self.lookup_fields, field_values))
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj

class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RatingSerializer
    queryset = models.Rating.objects.all()

class SearchView(APIView):
    def get(self,request):
        recipes = models.Recipe.objects.filter(is_public = True)

        courseIdString = request.GET.get('courseId') or None
        cuisineIdString = request.GET.get('cuisineId') or None

        if courseIdString:
            courseIdArray = courseIdString.split(',') 
            recipes = recipes.filter(meal_course_id__in=courseIdArray)
        else:
            return Response({})
        
        if cuisineIdString:
            cuisineIdArray = cuisineIdString.split(',')
            recipes = recipes.filter(cuisine_id__in=cuisineIdArray)
        else:
            return Response({})

        serializer = serializers.RecipeSerializer(recipes,many=True)
        return Response(serializer.data)

class UserSearchView(APIView):
    def get(self,request,user_id):
        recipes = models.Recipe.objects.filter(author_id = user_id)
        serializer = serializers.RecipeSerializer(recipes,many=True)
        print(serializer.data)
        return Response(serializer.data)

class ReturnFeedView(APIView):
    def get(self,request):
        recipes = models.Recipe.objects.filter(is_public=True).order_by('-publish_date')
        serializer = serializers.RecipeSerializer(recipes,many=True)
        return Response(serializer.data)
      
class CuisineList(generics.ListAPIView):
    queryset = models.Cuisine.objects.all()
    serializer_class = serializers.CuisineSerializer

class MealCourseList(generics.ListAPIView):
    queryset = models.MealCourse.objects.all()
    serializer_class = serializers.MealCourseSerializer

class ShoppingCartRecipeView(APIView):
    def get(self,request):
        shoppingCart = models.ShoppingCart.objects.filter(user=request.user)
        recipeDict = []

        for recipe in shoppingCart:
            recipeDict.append({
                'id': recipe.recipe.id,
                'name': recipe.recipe.name,
                'author': recipe.recipe.author.username,
                'cuisine': recipe.recipe.cuisine.name,
                'description': recipe.recipe.description
            })
        return Response(recipeDict)

class RatingsList(APIView):
    def get(self,request,recipe_id):
        queryset = models.Rating.objects.filter(recipe_id=recipe_id).order_by('-date_added')
        serializedInfo = serializers.RatingSerializer(queryset,many=True)
        return Response(serializedInfo.data)

class RatingPost(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self,request,recipe_id):
        newRating = models.Rating(
            recipe_id = recipe_id,
            user = request.user,
            rating = request.data['rating'],
            comment_headline = request.data['comment_headline'],
            comment_body = request.data['comment_body'],
            date_added = date.today()
        )
        newRating.save()
        return Response({})

class ShoppingCartView(APIView):
    def get(self,request):
        shoppingCart = models.ShoppingCart.objects.filter(user=request.user)

        ingredientDict = {}

        for recipe in shoppingCart:
            recipeIngredientList = models.RecipeIngredient.objects.filter(recipe=recipe.recipe)
            for recipeIngredient in recipeIngredientList:
                if recipeIngredient.ingredient.name in ingredientDict:
                    ingredientDict[recipeIngredient.ingredient.name] += recipeIngredient.quantity
                else:
                    ingredientDict[recipeIngredient.ingredient.name] = recipeIngredient.quantity

        return Response(ingredientDict)

class ToggleCart(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self,request,recipe_id):
        shoppingCart = models.ShoppingCart.objects.filter(user=request.user,recipe=recipe_id)
        if shoppingCart:
            inCartValue = True
        else:
            inCartValue = False

        return Response({
            'id':recipe_id,
            'inCart': inCartValue
        })

    def post(self,request,recipe_id):
        shoppingCart = models.ShoppingCart.objects.filter(user=request.user,recipe_id=recipe_id)
        if shoppingCart:
            shoppingCart.delete()
            response = {
                'id':recipe_id,
                'inCart':False
            }
        else:
            newRecipeToAddToCart = models.ShoppingCart(recipe_id=recipe_id,user=request.user)
            newRecipeToAddToCart.save()
            response = {
                'id':recipe_id,
                'inCart':True
            }

        return Response(response)

class VewRecipe(APIView):
    def get(self,request,pk):
        recipes = models.Recipe.objects.get(pk=pk)

        ingredients = models.RecipeIngredient.objects.filter(recipe_id=pk)
        ingList = []
        for ingredient in ingredients:
           ingList.append(ingredient.serialize())
        
        return Response({
            'recipe':recipes.serialize(),
            'ingredients':ingList
        })

class SubmitRecipeView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self,request):
        cuisine = models.Cuisine.objects.get(pk=request.data['cuisine_id'])
        mealCourse = models.MealCourse.objects.get(pk=request.data['course_id'])
        newRecipe = models.Recipe(
            name = request.data['name'],
            author = self.request.user,
            cuisine = cuisine,
            meal_course = mealCourse,
            description = request.data['description'],
            image = request.data['image'],
            instructions = request.data['instructions'],
            prep_time = request.data['prep_time'],
            cook_time = request.data['cook_time'],
            servings =  request.data['servings'],
            publish_date = date.today(),
            is_public = True
        )
        newRecipe.save()

        for ingredient in request.data['ingredients']:
            ingObj = models.Ingredient.objects.get(pk=ingredient['id'])
            newRecipeIng = models.RecipeIngredient(
                recipe = newRecipe,
                ingredient = ingObj,
                quantity = ingredient['quantity']
            )
            newRecipeIng.save()

        return Response({})


###### Login Views from Network Project ######
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "chefpad/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "chefpad/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "chefpad/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "chefpad/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "chefpad/register.html")
