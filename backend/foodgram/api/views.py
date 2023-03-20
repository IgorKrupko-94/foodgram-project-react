from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (HTTP_400_BAD_REQUEST,
                                   HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT
                                   )
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .permissions import AuthorOrAdminOrReadOnly, IsAuthenticatedOrAdmin
from .serializers import (IngredientSerializer,
                          TagSerializer,
                          RecipeSerializer,
                          ShortRecipeSerializer
                          )
from recipes.models import (Ingredient,
                            Tag,
                            Recipe,
                            Favorites,
                            Basket,
                            IngredientRecipe
                            )


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrAdminOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, permission_classes=IsAuthenticatedOrAdmin)
    def download_shopping_cart(self, request):
        if not Basket.objects.filter(
                user=request.user
        ).exists():
            return Response(
                {'errors': 'В Корзине отсутствуют рецепты'},
                status=HTTP_400_BAD_REQUEST
            )
        ingredients = IngredientRecipe.objects.filter(
            recipe__baskets__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        shopping_list = ''
        for ingredient in ingredients:
            item = (f'* {ingredient["ingredient__name"]} '
                    f'({ingredient["ingredient__measurement_unit"]}) -- '
                    f'{ingredient["amount"]}\n\n'
                    )
            shopping_list += item
        response = HttpResponse(shopping_list,
                                content_type='text/plain;charset=UTF-8'
                                )
        return response

    @action(methods=['post', 'delete'],
            detail=True,
            permission_classes=IsAuthenticatedOrAdmin
            )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = ShortRecipeSerializer(recipe)
            if Basket.objects.filter(
                user=request.user,
                recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Данный рецепт уже есть в списке покупок'},
                    status=HTTP_400_BAD_REQUEST
                )
            Basket.objects.create(
                user=request.user,
                recipe=recipe
            )
            return Response(serializer.data, status=HTTP_201_CREATED)
        if not Basket.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists():
            return Response(
                {'errors': 'Данный рецепт в Корзине отсутствует'},
                status=HTTP_400_BAD_REQUEST
            )
        Basket.objects.filter(
            user=request.user,
            recipe=recipe
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'],
            detail=True,
            permission_classes=IsAuthenticatedOrAdmin
            )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = ShortRecipeSerializer(recipe)
            if Favorites.objects.filter(
                user=request.user,
                recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Данный рецепт уже добавлен в Избранное'},
                    status=HTTP_400_BAD_REQUEST
                )
            Favorites.objects.create(
                user=request.user,
                recipe=recipe
            )
            return Response(serializer.data, status=HTTP_201_CREATED)
        if not Favorites.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists():
            return Response(
                {'errors': 'Данный рецепт отсутствует в Избранном'},
                status=HTTP_400_BAD_REQUEST
            )
        Favorites.objects.filter(
            user=request.user,
            recipe=recipe
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)
