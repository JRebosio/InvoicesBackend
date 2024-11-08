from django.db import models

from django.contrib.auth.models import AbstractUser


class AppUser(AbstractUser):
    class UserType(models.TextChoices):
        PLACER = "PLACER"
        APPROVER = "APPROVER"

    user_type = models.CharField(max_length=10, choices=UserType.choices)


class Provider(models.Model):

    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)


class Invoice(models.Model):
    class State(models.TextChoices):
        APPROVED = "APPROVED"
        REJECTED = "REJECTED"
        PENDING = "PENDING"

    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=15, choices=State.choices, default=State.PENDING
    )


class Item(models.Model):
    invoice = models.ForeignKey(
        to=Invoice, on_delete=models.CASCADE, related_name="items"
    )

    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
