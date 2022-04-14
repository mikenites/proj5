# Generated by Django 4.0.3 on 2022-04-09 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chefpad', '0007_ingredient_measurement_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MealCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='cook_time',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='instructions',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='is_public',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='prep_time',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='publish_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='servings',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(null=True),
        ),
    ]