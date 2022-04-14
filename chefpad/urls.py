from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("logout/", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("register/", views.register, name="register"),

    path("search/",views.SearchView.as_view()),
    path("search/all",views.ReturnFeedView.as_view()),

    path("ingredient/<int:pk>", views.IngredientRetrieve.as_view(), name="ingredient"),
    path("ingredient/", views.IngredientList.as_view(), name=""),
    path("cuisine/", views.CuisineList.as_view(), name=""),
    path("course/", views.MealCourseList.as_view(), name=""),
    path("shopping-cart/recipes", views.ShoppingCartRecipeView.as_view(), name=""),
    path("shopping-cart/items", views.ShoppingCartView.as_view(), name=""),

    path("recipe/<int:pk>",views.VewRecipe.as_view()),
    path("recipe/<int:recipe_id>/ingredient",views.RecipeIngredientViewSet.as_view({'get':'list','post':'create'})),
    path("recipe/<int:recipe_id>/ingredient/<int:ingredient_id>",views.RecipeIngredientViewSet.as_view({'get':'retrieve','delete':'destroy','put':'update'})),
    path("recipe/<int:recipe_id>/comment",views.RatingViewSet.as_view({'get':'list','post':'create'})),
    path("recipe/<int:recipe_id>/toggle-cart",views.ToggleCart.as_view()),
    path("recipe/<int:recipe_id>/rating",views.RatingsList.as_view()),
    path("recipe/<int:recipe_id>/submit-rating",views.RatingPost.as_view()),
    path("recipe/submit",views.SubmitRecipeView.as_view()),
    path("user/<int:user_id>",views.UserSearchView.as_view()),
]