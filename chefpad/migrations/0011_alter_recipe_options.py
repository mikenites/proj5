# Generated by Django 4.0.3 on 2022-04-12 04:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chefpad', '0010_alter_recipeingredient_ingredient_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-publish_date']},
        ),
    ]