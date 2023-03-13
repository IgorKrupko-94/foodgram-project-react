from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Наименование тега',
        max_length=200,
        unique=True,
        help_text='Укажите наименование тега'
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        null=True,
        unique=True,
        help_text='Укажите цвет тега'
    )
    slug = models.SlugField(
        'Слаг',
        max_length=200,
        unique=True,
        null=True,
        help_text='Укажите слаг тега'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Наименование ингредиента',
        max_length=200,
        help_text='Укажите наименование ингредиента'
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
        help_text='Укажите единицу измерения ингредиента'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        'Наименование рецепта',
        max_length=200,
        help_text='Укажите наименование рецепта'
    )
    text = models.TextField(
        'Описание рецепта',
        help_text='Укажите описание рецепта'
    )
    image = models.ImageField(
        'Картинка рецепта',
        upload_to='recipes/images/',
        help_text='Добавьте картинку рецепта'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        through='TagRecipe'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиент',
        through='IngredientRecipe'
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        validators=(MinValueValidator(1),),
        help_text='Укажите время приготовления рецепта (в минутах)'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=(MinValueValidator(1),)
    )


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='Пользователь, добавляющий продукты в Избранное'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='Рецепт, добавленный в Избранное'
    )

    class Meta:
        verbose_name = 'Избранное'

    def __str__(self):
        return f'{self.user} добавил в Избранное рецепт {self.recipe}'


class Basket(models.Model):
    user = models.ForeignKey(
        User,
        related_name='baskets',
        on_delete=models.CASCADE,
        verbose_name='Пользователь, добавляющий рецепты в корзину'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='baskets',
        on_delete=models.CASCADE,
        verbose_name='Рецепты, добавленные в Корзину'
    )

    class Meta:
        verbose_name = 'Корзина'

    def __str__(self):
        return f'{self.user} добавил в Корзину рецепт {self.recipe}'
