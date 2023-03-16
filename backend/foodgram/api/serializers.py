from re import match

from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField,
                                        ValidationError
                                        )

from recipes.models import (Ingredient,
                            Tag,
                            Recipe,
                            TagRecipe,
                            IngredientRecipe,
                            Favorites,
                            Basket
                            )
from users.serializers import CustomUserSerializer


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ShortRecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class IngredientRecipeSerializer(ModelSerializer):
    measurement_unit = SerializerMethodField()

    class Meta:
        model = IngredientRecipe
        fields = '__all__'

    def get_measurement_unit(self, instance):
        return instance.ingredient.measurement_unit


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientRecipeSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            TagRecipe.objects.create(tag=tag, recipe=recipe)
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                ingredient=ingredient['id'],
                recipe=recipe,
                amount=ingredient['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        tags = validated_data.get('tags')
        TagRecipe.objects.filter(recipe=instance).delete()
        for tag in tags:
            TagRecipe.objects.create(tag=tag, recipe=instance)
        ingredients = validated_data.get('ingredients')
        IngredientRecipe.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                ingredient=ingredient['id'],
                recipe=instance,
                amount=ingredient['amount']
            )
        instance.save()
        return instance

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favorites.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Basket.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()
