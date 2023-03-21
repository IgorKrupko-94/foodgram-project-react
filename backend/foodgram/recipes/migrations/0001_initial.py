# Generated by Django 2.2.19 on 2023-03-21 16:00

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Укажите наименование ингредиента', max_length=200, unique=True, verbose_name='Наименование ингредиента')),
                ('measurement_unit', models.CharField(help_text='Укажите единицу измерения ингредиента', max_length=200, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Ingredient', verbose_name='Ингредиент, связанный с рецептом')),
            ],
            options={
                'verbose_name': 'Ингредиенты с количеством',
                'verbose_name_plural': 'Ингредиенты с количеством',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Укажите наименование рецепта', max_length=200, verbose_name='Наименование рецепта')),
                ('text', models.TextField(help_text='Укажите описание рецепта', verbose_name='Описание рецепта')),
                ('image', models.ImageField(help_text='Добавьте картинку рецепта', upload_to='recipes/images/', verbose_name='Картинка рецепта')),
                ('cooking_time', models.PositiveIntegerField(help_text='Укажите время приготовления рецепта (в минутах)', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта')),
                ('ingredients', models.ManyToManyField(related_name='recipes', to='recipes.IngredientRecipe', verbose_name='Ингредиенты')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Укажите наименование тега', max_length=200, unique=True, verbose_name='Наименование тега')),
                ('color', models.CharField(help_text='Укажите цвет тега', max_length=7, null=True, unique=True, verbose_name='Цвет')),
                ('slug', models.SlugField(help_text='Укажите слаг тега', max_length=200, null=True, unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='TagRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe', verbose_name='Рецепт, связанный с тегом')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Tag', verbose_name='Тег, связанный с рецептом')),
            ],
            options={
                'verbose_name': 'Связь тегов и рецептов',
                'verbose_name_plural': 'Связь тегов и рецептов',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(through='recipes.TagRecipe', to='recipes.Tag', verbose_name='Теги'),
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='recipes.Recipe', verbose_name='Рецепт, добавленный в Избранное')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, добавляющий продукты в Избранное')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
            },
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='baskets', to='recipes.Recipe', verbose_name='Рецепты, добавленные в Корзину')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='baskets', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, добавляющий рецепты в корзину')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзина',
            },
        ),
        migrations.AddConstraint(
            model_name='tagrecipe',
            constraint=models.UniqueConstraint(fields=('tag', 'recipe'), name='Связь между тегом и рецептом должна быть уникальна'),
        ),
        migrations.AddConstraint(
            model_name='ingredientrecipe',
            constraint=models.UniqueConstraint(fields=('ingredient', 'amount'), name='Связь ингредиента и его количества должна быть уникальна'),
        ),
        migrations.AddConstraint(
            model_name='favorites',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='Пользователь не может добавить рецепт в Избранное дважды'),
        ),
        migrations.AddConstraint(
            model_name='basket',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='Пользователь не может добавить рецепт в Корзину дважды'),
        ),
    ]
