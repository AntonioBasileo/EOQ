from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth.models import User as AppUser, User
from app.model.eoq_models import Order, Product


class AppUserReadSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = AppUser
        fields = ['username']


class ProductReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

class ProductWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        if data.get('price', 0) < 0:
            raise serializers.ValidationError({'price': 'Il prezzo deve essere positivo.'})

        if data.get('stock', 0) < 0:
            raise serializers.ValidationError({'stock': 'Lo stock deve essere positivo.'})

        if data.get('code', None) is None:
            raise serializers.ValidationError({'code': 'Il codice è obbligatorio.'})

        return data

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        return instance

class OrderReadSerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)
    date = serializers.DateField(read_only=True)
    total_price = serializers.FloatField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ['code', 'date', 'total_price', 'status']


class ProductOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class OrderWriteSerializer(serializers.ModelSerializer):
    products = ProductOrderSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(queryset=AppUser.objects.all())

    class Meta:
        model = Order
        fields = ['id', 'date', 'total_price', 'status', 'user', 'products']

    def create(self, data):
        products_data = data.pop('products')

        if not products_data or len(products_data) == 0:
            raise serializers.ValidationError({'products': "L'ordine deve contenere almeno un prodotto."})

        products_entities = []
        total_price = 0

        for item in products_data:
            product = get_object_or_404(Product, id=item['id'])
            quantity = item['quantity']

            if quantity <= 0:
                raise serializers.ValidationError({'products': f'La quantità del prodotto {product.name} essere positiva.'})

            if product.stock < item['quantity']:
                raise serializers.ValidationError({'products': f'Il prodotto {product.name} non ha abbastanza stock.'})

            total_price += product.price * quantity
            products_entities.append(product)

        return Order.objects.create(products=products_entities, total_price=total_price,
                                     user=get_object_or_404(User, pk=data['user']), **data)
