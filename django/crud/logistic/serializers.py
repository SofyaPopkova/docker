from rest_framework import serializers
from models import Stock, Product, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    model = Stock
    fields = ['id', 'address', 'positions']
    address = serializers.Charfield(max_length=300)
    positions = ProductPositionSerializer(many=True)

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for item in positions:
            StockProduct.objects.create(
                stock=stock,
                product=item.get('product'),
                quantity=item.get('quantity'),
                price=item.get('price')
            )
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        StockProduct.objects.update_or_create(positions)
        return stock
