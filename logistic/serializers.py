from rest_framework import serializers

from .models import Product, Stock, StockProduct

class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=60)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=18, decimal_places=2, min_value=0)

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = super().create(validated_data)

        for position in positions:
            stock.positions.create(**position)

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)

        stock.positions.all().delete()

        for position in positions:
            stock.positions.update_or_create(**position)

        return stock
