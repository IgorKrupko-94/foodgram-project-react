from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import (IngredientSerializer, TagSerializer)
from recipes.models import Ingredient, Tag, Recipe


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class APIRecipe(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass


class APIRecipeDetail(APIView):
    def get(self, request):
        pass

    def patch(self, request):
        pass

    def delete(self, request):
        pass
