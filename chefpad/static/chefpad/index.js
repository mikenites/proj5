document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#feed-link').addEventListener('click',load_feed);
    document.querySelector('#search-link').addEventListener('click',load_search);
    document.querySelector('#cart-link').addEventListener('click',load_cart);
    document.querySelector('#create-recipe-link').addEventListener('click',load_create_recipe);
    generateIngredientHMTL();
    load_feed();
});

let currentIngredientField = 0;

function switch_view(viewName) {
    document.querySelector('#feed-view').style.display = 'none';
    document.querySelector('#search-view').style.display = 'none';
    document.querySelector('#cart-view').style.display = 'none';
    document.querySelector('#create-recipe-view').style.display = 'none';
    document.querySelector('#view-recipe-view').style.display = 'none';
    document.querySelector('#user-view').style.display = 'none';

    let view = undefined;

    if (viewName == 'feed-view') {
        view = document.querySelector('#feed-view'); 
        document.querySelector('#feed-view-port').innerHTML = "";
    } else if (viewName == 'search-view') {
        view = document.querySelector('#search-view');
        document.querySelector('#search-filter-cuisine-list').innerHTML = "";
        document.querySelector('#search-filter-course-list').innerHTML = "";
        document.querySelector('#search-results').innerHTML = "";
    } else if (viewName == 'cart-view') {
        view = document.querySelector('#cart-view');
        document.querySelector('#cart-recipe-list').innerHTML = "";
        document.querySelector('#cart-shopping-list').innerHTML = "";
    } else if (viewName == 'create-recipe-view') {
        document.querySelector('#titleInput').value = "";
        document.querySelector('#imageInput').value = "";
        document.querySelector('#cookTimeInput').value = "";
        document.querySelector('#prepTimeInput').value = "";
        document.querySelector('#servingsInput').value = "";
        document.querySelector('#descriptionTextArea').value = "";
        document.querySelector('#instructionTextArea').value = "";
        view = document.querySelector('#create-recipe-view');
        currentIngredientField = 0;
    } else if (viewName == 'view-recipe') {
        view = document.querySelector('#view-recipe-view');
        document.querySelector('#recipe-view-info').innerHTML = "";
        document.querySelector('#recipe-view-ingredients').innerHTML = "";
        document.querySelector('#recipe-view-right').innerHTML = "";
        document.querySelector('#view-recipe-rating').innerHTML = "";
        document.querySelector('#ratingTitleInput').value = "";
        document.querySelector('#ratingNumberInput').value = "";
        document.querySelector('#ratingTextArea').value = "";
    } else if (viewName == 'user-view') {
        view = document.querySelector('#user-view');
    }

    view.style.display = 'block';
    return view;
};

function load_recipe(recipeId) {
    let view = switch_view('view-recipe');
    let recipeViewInfo = view.querySelector('#recipe-view-info');
    let recipeViewIngredients = view.querySelector('#recipe-view-ingredients');
    let recipeViewRight = view.querySelector('#recipe-view-right');

    fetch('recipe/' + recipeId)
    .then(response => response.json())
    .then(data => {
        recipeViewInfo.innerHTML = `
            <p><b>Cuisine:</b> ${data['recipe']['cuisine']}</p>
            <p><b>Course:</b> ${data['recipe']['meal_course']}</p>
            <p><b>Prep Time:</b> ${data['recipe']['prep_time']} minutes<p>
            <p><b>Cook Time:</b> ${data['recipe']['cook_time']} minutes<p>
        `;

        view.querySelector('#recipe-view-name').innerHTML = data['recipe']['name'];
        view.querySelector('#recipe-view-description').innerHTML = data['recipe']['description']
        view.querySelector('#recipe-view-image').src = data['recipe']['image']
        
        let numIngredients = data['ingredients'].length
        recipeViewIngredients.innerHTML = `
        <h5>Ingredients</h5>
        <ul>`
        data['ingredients'].forEach((ingObj) => {
            recipeViewIngredients.innerHTML += `<li>${ingObj['name']}: ${ingObj['quantity']} grams</li>`
        })
        recipeViewIngredients.innerHTML += "</ul>"

        recipeViewRight.innerHTML = `
            <h5>Instructions</h5>
            <p>${data['recipe']['instructions']}</p>`;

        let toggleCartBtn = document.createElement('button');
        toggleCartBtn.id = "toggle";
        toggleCartBtn.className = "btn btn-secondary"
        
        fetch('recipe/' + data['recipe']['id'] +'/toggle-cart', {
            method: 'GET',
        })
        .then(response => response.json())
        .then(data => {
            if (data['inCart'] == false) {
                toggleCartBtn.innerHTML = "Add to Cart"
            } else {
                toggleCartBtn.innerHTML = "Remove from Cart"
            }
        })
        
        recipeViewRight.append(toggleCartBtn)

        toggleCartBtn.addEventListener('click',() => {
            fetch('recipe/' + data['recipe']['id'] +'/toggle-cart', {
                method: 'POST',
            })
            .then(response => response.json())
            .then(data => {
                load_cart()
            })
        })

        fetch('recipe/' + data['recipe']['id'] +'/rating', {
            method: 'GET',
        }).then(response => response.json())
        .then(data => {
            let ratingView = document.querySelector('#view-recipe-rating')
            let numRatings = data.length

            for (let i = 0; i < data.length; i++) {
                let ratingCard = document.createElement('div')
                ratingCard.className = "card w-75";
                ratingCard.style = "margin-bottom: 15px";
                ratingCard.innerHTML = `
                    <div class="card-body">
                        <h5 class="card-title">${data[i]['comment_headline']}</h5>
                        <p class="card-text">Rating: ${data[i]['rating']}/5</span></p>
                        <p class="card-text">${data[i]['comment_body']}</p>
                    </div>
                `
                ratingView.append(ratingCard)
            }
        })

        let ratingSubBtn = document.querySelector('#submit-rating-btn');
        ratingSubBtn.addEventListener('click',() => {

            let title = document.querySelector('#ratingTitleInput').value;
            let ratingNum = document.querySelector('#ratingNumberInput').value;
            let comment = document.querySelector('#ratingTextArea').value;

            let ratingJson = {
                'rating':ratingNum,
                'comment_headline':title,
                'comment_body':comment,
                'recipe_id':data['recipe']['id']
            }

            fetch('recipe/' + data['recipe']['id'] +'/submit-rating', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(ratingJson)
            })
            load_recipe(data['recipe']['id'])
        })


    })
}

function load_feed() {
    let view = switch_view('feed-view');
    let subView = view.querySelector('#feed-view-port');
    fetch_all(subView);
};

function fetch_all(view) {
    fetch('/search/all')
    .then(response => response.json())
    .then(data => {
        for (let i = 0; i < data.length; i++) {
            
            let recipeObj = {
                'id':data[i]['id'],
                'name': data[i]['name'],
                'author': data[i]['author_name'],
                'author_id': data[i]['author_id'],
                'desc': data[i]['description'],
                'image': data[i]['image'],
                'publishDate': data[i]['publish_date']
            }
            let recipeItem = generate_feed_item_html(recipeObj);
            view.append(recipeItem);
        }

        let recipeBtns = view.querySelectorAll('.view-recipe-btn');
        recipeBtns.forEach((recipeBtn) => {
            recipeBtn.addEventListener('click',() => {
                let recipeId = recipeBtn.id.split('-')[2]
                load_recipe(recipeId)
            })
        })

        let authorLinks = view.querySelectorAll('.view-author-link');

        authorLinks.forEach((authorLink) => {
            authorLink.addEventListener('click',() => {
                let authorId = authorLink.id.split('-')[2]
                let userName = authorLink.innerHTML
                load_user_view(authorId,userName)
            })
        })
    })
}

function load_user_view(userId,userName) {
    let view = switch_view('user-view');
    let subView = view.querySelector('#user-feed-view-port');
    let subViewHeader = view.querySelector('#user-view-title');
    subViewHeader.innerHTML = userName + "'s Recipes";
    fetch_user_feed(subView,userId);
}

function fetch_user_feed(view,userId) {

    fetch('/user/' + userId)
    .then(response => response.json())
    .then(data => {
        
        console.log(data)
        for (let i = 0; i < data.length; i++) {
            
            let recipeObj = {
                'id':data[i]['id'],
                'name': data[i]['name'],
                'author': data[i]['author_name'],
                'author_id':data[i]['author_id'],
                'desc': data[i]['description'],
                'image': data[i]['image'],
                'publishDate': data[i]['publish_date']
            }
            let recipeItem = generate_feed_item_html(recipeObj);
            view.append(recipeItem);
        }

        let recipeBtns = view.querySelectorAll('.view-recipe-btn');
        recipeBtns.forEach((recipeBtn) => {
            recipeBtn.addEventListener('click',() => {
                let recipeId = recipeBtn.id.split('-')[2]
                load_recipe(recipeId)
            })
        })
    })
}

function fetch_feed(url,view) {
    fetch('/search/'+url)
    .then(response => response.json())
    .then(data => {
        for (let i = 0; i < data.length; i++) {
            
            let recipeObj = {
                'id':data[i]['id'],
                'name': data[i]['name'],
                'author': data[i]['author_name'],
                'desc': data[i]['description'],
                'image': data[i]['image'],
                'publishDate': data[i]['publish_date']
            }
            let recipeItem = generate_feed_item_html(recipeObj);
            view.append(recipeItem);
        }

        let recipeBtns = view.querySelectorAll('.view-recipe-btn');
        recipeBtns.forEach((recipeBtn) => {
            recipeBtn.addEventListener('click',() => {
                let recipeId = recipeBtn.id.split('-')[2]
                load_recipe(recipeId)
            })
        })
    })
}


function generate_feed_item_html(recipeObj) {
    let recipeItem = document.createElement('div');
    recipeItem.className = 'row';
    recipeItem.id = 'recipe-list-item-';
    recipeItem.innerHTML = `
        <div class="card" style="flex-direction: row; width: 100%; margin-bottom: 25px;">
            <img style="width: 200px" src="${recipeObj['image']}" class="card-img-top">
            <div class="card-body">
                <h5 class="card-title">${recipeObj['name']}</h5>
                <p class="card-text">${recipeObj['desc']}</p>
                <a href="#" class="btn btn-primary view-recipe-btn" id="view-recipe-${recipeObj['id']}">View Recipe</a>
                <p class="card-text"><small class="text-muted">Written by <a href='#' class='view-author-link' id='view-author-${recipeObj['author_id']}'>${recipeObj['author']}</a> on ${recipeObj['publishDate']}</small></p
            </div>
        </div>
    `;

    return recipeItem
}

function load_search() {
    let view = switch_view('search-view');
    let subview = document.querySelector('#search-results');
    let cuisineFilterDiv = document.querySelector('#search-filter-cuisine-list');
    fetch_cuisine_list(cuisineFilterDiv);
    let courseFilterDiv = document.querySelector('#search-filter-course-list');
    
    fetch_course_list(courseFilterDiv);    

    let searchFiltersDiv = document.querySelector('#search-filters')
    fetch_all(subview)

    searchFiltersDiv.addEventListener('click', () => {
        
        let cuisineListCheckbox = cuisineFilterDiv.getElementsByTagName('input');
        let cuisineArray = [];
        let cuisineParemeter = ""; 
        let i = 0;

        for (let cuisineCheckbox of cuisineListCheckbox) {
            let dict = {
                'name': cuisineCheckbox.id.split('-')[0],
                'id': cuisineCheckbox.id.split('-')[1],
                'checked': cuisineCheckbox.checked
            }
            cuisineArray[i] = dict;
            if (cuisineCheckbox.checked == true) {
                cuisineParemeter += cuisineCheckbox.id.split('-')[1] + ','
            }
            
            i++;
        }

        let courseListCheckbox = courseFilterDiv.getElementsByTagName('input');
        let courseArray = [];
        let courseParameter = "";
        let j = 0;

        for (let courseCheckbox of courseListCheckbox) {
            let dict = {
                'name': courseCheckbox.id.split('-')[0],
                'id': courseCheckbox.id.split('-')[1],
                'checked': courseCheckbox.checked
            }
            courseArray[j] = dict;
            if (courseCheckbox.checked == true) {
                courseParameter += courseCheckbox.id.split('-')[1] + ','
            }
            j++;
        }     
        
        let url = '?cuisineId=' + cuisineParemeter.slice(0,-1) + '&courseId=' + courseParameter.slice(0,-1);
        subview.innerHTML = '';
        fetch_feed(url,subview)

    })

    function fetch_cuisine_list(cuisineFilterDiv) {
        fetch('/cuisine')
        .then(response => response.json())
        .then(data => {
            for (let i = 0; i < data.length; i++) {
                let cuisineObj = {
                    'id':data[i]['id'],
                    'name': data[i]['name']
                }
                let cuisineItem = generate_search_filter_html(cuisineObj);
                cuisineFilterDiv.append(cuisineItem);
            }
        })
    }

    function fetch_course_list(courseFilterDiv) {
        fetch('/course')
        .then(response => response.json())
        .then(data => {
            for (let i = 0; i < data.length; i++) {
                let cuisineObj = {
                    'id':data[i]['id'],
                    'name': data[i]['name']
                }
                let cuisineItem = generate_search_filter_html(cuisineObj);
                courseFilterDiv.append(cuisineItem);
            }
        })
    }

    function generate_search_filter_html(cuisineObj) {
        let newListItem = document.createElement('li');

        let newCheckbox = document.createElement('input');
        newCheckbox.setAttribute("type","checkbox")
        newCheckbox.setAttribute("checked","true")
        newCheckbox.id = cuisineObj['name'] + '-' + cuisineObj['id'];
        newListItem.append(newCheckbox);
        
        let listItemText = document.createElement('span');
        listItemText.innerHTML = " " + cuisineObj['name'];
        newListItem.append(listItemText);

        return newListItem;
    }
};

function load_cart() {
    let view = switch_view('cart-view');
    create_cart_recipe_list();
    create_shopping_list();

    function create_cart_recipe_list() {
        let cartRecipeListView = document.querySelector('#cart-recipe-list');
        
        fetch('shopping-cart/recipes')
        .then(response => response.json())
        .then(data => {
            let numRecipes = data.length;
            let tableRecipe = document.createElement('table');
            tableRecipe.className = 'table table-striped';
            tableRecipe.innerHTML = `
                <thead>
                    <tr>
                        <th scope="col">Recipe Name</th>
                        <th scope="col">Cuisine</th>
                        <th scope="col">Description</th>
                        <th scope="col">Remove from Shopping Cart</th>
                    </tr>
                </thead>
                <tbody>
            `;

            for (let i = 0; i < numRecipes; i++) {
                let id = data[i]['id'];
                tableRecipe.innerHTML += `
                    <tr scope="row">
                        <td>${data[i]['name']}</td>
                        <td>${data[i]['cuisine']}</td>
                        <td>${data[i]['description']}</td>
                        <td><button type="button" class="btn btn-secondary remove-btn" id="remove-btn-${id}">Remove</button></td>
                    </tr>
                `;
            }

            tableRecipe.innerHTML += '</tbody>';

            cartRecipeListView.append(tableRecipe)
            
            let removeBtns = document.querySelectorAll('.remove-btn')
            removeBtns.forEach((removeBtn) => {
                removeBtn.addEventListener('click', () => {

                    let recipeId = removeBtn.id.split('-')[2];
                    toggle_shopping_cart(recipeId)

                    load_feed();

                })
            })
            
        })
    }

    function toggle_shopping_cart(recipe_id) {
        fetch('recipe/' + recipe_id +'/toggle-cart', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            
        })
    }

    function create_shopping_list() {
        let cartShoppingListView = document.querySelector('#cart-shopping-list');       
        
        fetch('shopping-cart/items')
        .then(response => response.json())
        .then(data => {
            let tableIngredients = document.createElement('table');
            tableIngredients.className = 'table table-striped';
            tableIngredients.innerHTML = `
                <thead>
                    <tr>
                        <th>Ingredient</th>
                        <th>Amount (grams)</th>
                    </tr>
                </thead>
                <tbody>
            `;

            for (let key in data) {
                tableIngredients.innerHTML += `
                    <tr>
                        <td>${key}</td>
                        <td>${data[key]}</td>
                    </tr>
                `;
            }

            cartShoppingListView.append(tableIngredients)
        })

    }
};

function load_create_recipe() {
    let view = switch_view('create-recipe-view');
    let ingredientTBody = document.querySelector('#ingredient-tbody');
    let addIngBtn = document.querySelector('#add-ingredient-btn');

    fetch('/cuisine/')
    .then(response => response.json())
    .then(data => {
        let cuisineSelect = document.querySelector('#cuisineSelect');
        let optionHTML = "";

        for (let cuisine of data) {
            optionHTML += `<option value="${cuisine['id']}">${cuisine['name']}</option>`
        }

        cuisineSelect.innerHTML = optionHTML;
    })  

    fetch('/course/')
    .then(response => response.json())
    .then(data => {
        let courseSelect = document.querySelector('#courseSelect');
        let optionHTML = "";

        for (let course of data) {
            optionHTML += `<option value="${course['id']}">${course['name']}</option>`
        }

        courseSelect.innerHTML = optionHTML;
    })

    addIngBtn.addEventListener('click',() => {
        let rowToShow = document.getElementById('ingredient-row-'+currentIngredientField)
        rowToShow.style = "display: block"
        currentIngredientField++
    })
    
    recipeSubmit();
}

function recipeSubmit() {
    let recipeSubmitBtn = document.querySelector('#submit-recipe-btn');
    recipeSubmitBtn.addEventListener('click', () => {
        
        let ingredientJson = [];

        let ingredientNameArray = document.getElementsByClassName('ingredient-select');
        let ingredientAmountArray = document.getElementsByClassName('ingredient-amount');
        
        for (let i = 0; i < 20; i++) {
            if (ingredientAmountArray[i].value != "") {
                ingredientJson.push({'id' : ingredientNameArray[i].value,'quantity':ingredientAmountArray[i].value})
            }
        }

        let recipeJson = {
            'name': document.querySelector('#titleInput').value,
            'description': document.querySelector('#descriptionTextArea').value,
            'image': document.querySelector('#imageInput').value,
            'instructions': document.querySelector('#instructionTextArea').value,
            'prep_time': document.querySelector('#prepTimeInput').value,
            'cook_time': document.querySelector('#cookTimeInput').value,
            'servings': document.querySelector('#servingsInput').value,
            'cuisine_id': document.querySelector('#cuisineSelect').value,
            'course_id': document.querySelector('#courseSelect').value,
            'ingredients': ingredientJson
        }
        
        fetch('recipe/submit',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(recipeJson)
        })

        load_feed();

    })
}

function generateIngredientHMTL() {
    fetch('/ingredient/')
    .then(response => response.json())
    .then(data => {
        let ingredientTBody = document.querySelector('#ingredient-tbody');

        for (let i = 0; i < 20; i++) { 
            let newRow = document.createElement('tr');
            newRow.id = 'ingredient-row-' + i;
            newRow.style = 'display:none';

            let optionHTML = `<td><select class="form-control ingredient-select"><option value="0"> </option>`;

            for (let ingredient of data) {
                optionHTML += `<option value="${ingredient['id']}">${ingredient['name']}</option>`
            }

            optionHTML += `</select></td><td><input type='input' class='ingredient-amount form-control'></td></tr>`
            newRow.innerHTML = optionHTML;

            ingredientTBody.append(newRow)
        }
    })
}
