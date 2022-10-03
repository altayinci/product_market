import json

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import status, viewsets
from rest_framework.response import Response

from product_api.models import Product, DeliveryOptions
from product_api.serializers import ProductSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]

    ordering_fields = '__all__'
    DEFAULT_PER_PAGE = 2

    @method_decorator(cache_page(60 * 15))
    def list(self, request):

        queryset = Product.objects.get_queryset().order_by('id')
        page_number = request.GET.get("page", 1)
        per_page = request.GET.get("per_page", self.DEFAULT_PER_PAGE)

        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page_number)

        serializer = ProductSerializer(page_obj, many=True)
        return Response({"status": "success", "count": len(page_obj), "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        }, "data": serializer.data},
                        status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        product_obj = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(product_obj)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request):
        body = self.request.body
        body_dict = json.loads(body.decode('utf-8'))

        try:
            product_obj = Product.objects.create(name=body_dict.get('name'),
                                                 price=body_dict.get('price'),
                                                 description=body_dict.get('description'),
                                                 currency=body_dict.get('currency'),
                                                 seller_id=body_dict.get('seller_id'),
                                                 in_stock=body_dict.get('in_stock'))
            product_obj.save()

            delivery_options = body_dict.get("delivery_options")
            for option in delivery_options:
                delivery_options_obj = DeliveryOptions(name=option.get('name'),
                                                       price=option.get('price'),
                                                       currency=option.get('currency'),
                                                       product=product_obj,
                                                       )
                delivery_options_obj.save()

        except Exception as e:
            content = {'Error': str(e)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, pk=None):
        body = self.request.body
        body_dict = json.loads(body.decode('utf-8'))

        try:
            product_obj = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if body_dict.get('delivery_options'):
            product_obj.delivery_options.all().delete()
            for option in body_dict.get('delivery_options'):
                delivery_options_obj = DeliveryOptions.objects.create(name=option.get('name'),
                                                                      price=option.get('price'),
                                                                      currency=option.get('currency'),
                                                                      product=product_obj
                                                                      )
                delivery_options_obj.save()

        product_obj.name = body_dict.get('name') if body_dict.get('name') else product_obj.name
        product_obj.price = body_dict.get('price') if body_dict.get('price') else product_obj.price
        product_obj.description = body_dict.get('description') if body_dict.get('description') else product_obj.description
        product_obj.currency = body_dict.get('currency') if body_dict.get('currency') else product_obj.currency
        product_obj.seller_id = body_dict.get('seller_id') if body_dict.get('seller_id') else product_obj.seller_id
        product_obj.in_stock = body_dict.get('in_stock') if body_dict.get('in_stock') else product_obj.in_stock

        product_obj.save()

        return Response(status=status.HTTP_200_OK)

    @transaction.atomic
    def destroy(self, request, pk=None):
        return super(ProductViewSet, self).destroy(request, pk=None)
