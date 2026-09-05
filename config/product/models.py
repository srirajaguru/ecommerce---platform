from django.db import models


class Product(models.Model):

    name = models.CharField(
        max_length=200
    )

    product_code = models.CharField(
        max_length=50,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    size = models.CharField(
        max_length=100,
        blank=True
    )

    load_capacity = models.CharField(
        max_length=100,
        blank=True
    )

    material = models.CharField(
        max_length=100,
        default="SFRC"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    is_available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.name} - {self.product_code}"