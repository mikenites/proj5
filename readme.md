# Overview
Chefpad is a recipe application that is similar to "All Recipes" and the NYT Cooking application. At the highest level, users are able to post their own recipes, filter through already posted recipes, and then add all the ingredients for multiple recipes into an aggregated shopping cart of ingredients. Users can also comment and review recipes anonymously. Basic user login/register/logout pages are included.

# Distinctiveness & Complexity
The project is distinct in both technical and user features.

First, I spent a significant amount of effort learning both Class Based Views as well as the Django Rest Framework. I utilized both within this project. Additionally, I had to dig into the source code of the Django Rest framework to modify a parent generic rest viewset to allow me to identify an object given two non-primary key variables.

Second, the website is significantly more dynamic than in previous projects. For example, you search via filtering by cuisine and course (e.g., breakfast or lunch) using checkboxes, similar to how you can filter down onto an Amazon web page. The admin can add and remove cuisine and course types, and the search page will dynamically pull those filters from the database. These also come into play when creating a recipe, which include dynamic select input field options for both cuisine and course types. By enforcing data integrity constraints onto ingredients, the app can then aggregate amounts of different ingredients across recipes (fourth feature).

Third, when "adding a recipe," the user can click a button to add additional ingredients and the DOM is updated to add these additional fields via javascript. Fourth, the shopping cart aggregates amounts of ingredients across multiple recipes that the user has saved and outputs it via a list. 

Finally, when including a feature that we've learned about in past, I attempted to increase the amount of compexity for that feature. For example, the core models include significantly more fields than previous projects, so whereas a "post" in the social network app had a single field, a recipe has many. Another example, is ratings "extend" comments by including a title and a rating score rather than just a single comment box. Finally, the project has significantly more views and API calls than previous projects.

To make the webpage mobile responsive, I am utilizing bootstrap's javascript addons and grid layout features. 

# Information in Each File
```
chefpad
- Static \ Chefpad
---- index.js: this includes all the javascript for the project front end
---- style.css: empty, utilizing bootstrap with no modifications
- templates \ chefpad
---- index.html: Primary html page
---- layout.html: High level structure for the page including a responsive navbar
---- login.html: re-used Project 4's and then edited to be responsive
---- register.html: re-used Project 4's and then edited to be responsive
- admin.py: Registers all models onto admin panel
- apps.py: used django defaults
- models.py: Includes all models for the project
- serializers.py: Includes all serializers for the project
- tests.py: No edits
- urls.py: Includes all URLs for the project
- views.py: Includes all views for the project, including the re-used user views

project5
- asgi.py: No edits
- settings.py: Edited to include rest framework and some minor settings changes related
- urls.py: Edited to just import chefpad app urls
- wsgi.py: No edits

db.sqlite3: pre-populated database
manage.py: default django
requirements.txt: just utilizes django and django rest framework
```

# How to Run the Application
You will need to install both Django and the Django Rest Framework for this application to work. You can then copy and paste the file directory to your directory of choice and run the program via python manage.py runserver. The files on github include the pre-loaded database shown in the video. Upon running the code, you can register an account locally or use the provided username and password called "test" and "test".

# Attribution
Some of the recipe description text comes from Wikipedia and other blogs. Other recipes are just made up for fun. All of the ingredients are made up for fun.