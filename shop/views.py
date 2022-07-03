from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem, Collection, Customer, OrderItem, Product, Review
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, CustomerSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from .permissions import IsAdminOrReadOnly
from .pagination import DefaultPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated


# CBV
class ProductViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)



class CollectionViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Collection.objects.annotate(
            products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)



class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin, 
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = AddCartItemSerializer(data=request.data, context={'cart_id': self.kwargs['cart_pk']})
        serializer.is_valid(raise_exception=True)
        serializer = serializer.save()
        serializer = CartItemSerializer(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])


class CustomerViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)



#     FBV

#@api_view(['GET', 'POST'])
#def product_list(request):
#    if request.method == 'GET':
#        queryset = Product.objects.all()
#        serializer = ProductSerializer(queryset, many=True, context={'request': request})
#        return Response(serializer.data)
#    elif request.method == 'POST':
#        serializer = ProductSerializer(data=request.data)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()
#        return Response(serializer.data, status=status.HTTP_201_CREATED)#

#@api_view(['GET', 'PUT', 'DELETE'])
#def product_detail(request, id):
#    product = get_object_or_404(Product, pk=id)
#    if request.method == 'GET':
#        serializer = ProductSerializer(product)
#        return Response(serializer.data)
#    elif request.method == 'PUT':
#        serializer = ProductSerializer(product, data=request.data)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()
#        return Response(serializer.data)
#    elif request.method == 'DELETE':
#        if product.orderitems.count() > 0:
#            return Response({'error': 'Product cannot be deleted because it is associated with an order #item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#        product.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)

#@api_view(['GET', 'POST'])
#def collection_list(request):
#    if request.method == 'GET':
#        queryset = Collection.objects.annotate(
#            products_count=Count('products')).all()
#        serializer = CollectionSerializer(queryset, many=True)
#        return Response(serializer.data)
#    elif request.method == 'POST':
#        serializer = CollectionSerializer(data=request.data)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()
#        return Response(serializer.data, status=status.HTTP_201_CREATED)#

#@api_view(['GET', 'PUT', 'DELETE'])
#def collection_detail(request, pk):
#    collection = get_object_or_404(Collection.objects.annotate(
#        products_count=Count('products')), pk=pk) 
#    if request.method == 'GET':
#        serializer = CollectionSerializer(collection)
#        return Response(serializer.data)
#    elif request.method == 'PUT':
#        serializer = CollectionSerializer(collection, data=request.data)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()
#        return Response(serializer.data)
#    elif request.method == 'DELETE':
#        if collection.products.count() > 0:
#            return Response({'error': 'Collection cannot be deleted because it includes one or more #products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#        collection.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)