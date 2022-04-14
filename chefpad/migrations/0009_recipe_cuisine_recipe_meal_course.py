# Generated by Django 4.0.3 on 2022-04-09 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chefpad', '0008_cuisine_mealcourse_recipe_cook_time_recipe_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='cuisine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chefpad.cuisine'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='meal_course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chefpad.mealcourse'),
        ),
    ]