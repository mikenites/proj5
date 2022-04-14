# Overview
Chefpad is a recipe application that is similar to "All Recipes" and the NYT Cooking application. At the highest level, users are able to post their own recipes, filter through already posted recipes, and then add all the ingredients for multiple recipes into an aggregated shopping cart of ingredients. Users can also comment and review recipes.

# Distinctiveness & Complexity
The project is distinct in both technical and user features.

First, I spent a significant amount of effort learning both Class Based Views as well as the Django Rest Framework. I utilzied both within this project. Additionally, I had to dig into the source code of the Django Rest framework to modify a viewset to allow me to identify an object given two non-primary key variables.

Second, the website is significantly more dynamic than in previous projects. For example, you search via filtering by cuisine and course (e.g., breakfast or lunch) via checkboxes, similar to how you can filter down onto an Amazon web page. The admin can add and remove cuisine and course types, and the search page will dynamically pull those filters from the database. These also come into play when creating a recipe, which include dynamic select input field options for both cuisine and course types. Fourth, when "adding a recipe," the user can click a button to add additional ingredients and the DOM is updated to add these additional fields via javascript. Fifth, the shopping cart aggregates amounts of ingredients across multiple recipes that the user has saved and outputs it via a list. Finally, the core models include significantly more fields than previous projects and there are more views.

# Information in Each File
```
Test code

```

# How to Run the Application
You will need to install both Django and the Django Rest Framework for this application to work. You can then copy and paste the file directory to your directory of choice and run the program via python manage.py runserver. The files on github include the pre-loaded database shown in the video. Upon running the code, you can register an account locally or use the provided username and password called "test" and "test".

# Attribution
Some of the recipe description text comes from Wikipedia and other blogs. Other recipes are just made up for fun. All of the ingredients are made up for fun.