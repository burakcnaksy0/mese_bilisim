from rest_framework import serializers
from .models import *


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    page_number = serializers.IntegerField()
    published_date = serializers.DateField()
    stock_number = serializers.IntegerField()

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.page_number = validated_data.get("page_number", instance.page_number)
        instance.published_date = validated_data.get("published_date", instance.published_date)
        instance.stock_number = validated_data.get("stock_number", instance.stock_number)
        instance.save()
        return instance
