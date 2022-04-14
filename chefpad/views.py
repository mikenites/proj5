from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

from . import models
from . import serializers

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

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

class ReturnFeedView(APIView):
    def get(self,request):
        recipes = models.Recipe.objects.filter(is_public=True)
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
        print(request.data)
        return Response({})