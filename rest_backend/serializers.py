from rest_framework import serializers
from .models import AppUser, Invoice, Item, Provider
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = AppUser
        fields = ("id", "username", "email", "user_type", "password")
        # extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # password = validated_data.pop("password")
        user = AppUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            user_type=validated_data["user_type"],
        )
        return user


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["name", "quantity", "price"]


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = ["id", "user", "name", "address", "phone_number"]
        read_only_fields = ["user"]


class InvoiceSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    provider = serializers.CharField()

    class Meta:
        model = Invoice
        fields = ["id", "user", "provider", "state", "items"]
        read_only_fields = ["user"]

    def validate_provider(self, value):
        try:
            return Provider.objects.get(name=value)
        except Provider.DoesNotExist:
            raise ValidationError("Provider with this name does not exist.")

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        provider = validated_data.pop("provider")
        invoice = Invoice.objects.create(provider=provider, **validated_data)

        for item_data in items_data:
            Item.objects.create(invoice=invoice, **item_data)
        return invoice

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["provider"] = instance.provider.name

        total_cost = sum(item.quantity * item.price for item in instance.items.all())
        representation["total_cost"] = total_cost
        return representation
