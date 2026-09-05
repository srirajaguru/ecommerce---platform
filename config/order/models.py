from django.db import models
from django.conf import settings


class OrderInquiry(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    inquiry_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='order_inquiries'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    customer_name = models.CharField(
        max_length=100
    )

    customer_phone = models.CharField(
        max_length=15
    )

    customer_email = models.EmailField()

    notes = models.TextField(
        blank=True
    )

    whatsapp_sent = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.inquiry_id:
            last_inquiry = OrderInquiry.objects.order_by(
                '-id'
            ).first()

            if last_inquiry:
                number = last_inquiry.id + 1
            else:
                number = 1

            self.inquiry_id = f"INQ-{number:05d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.inquiry_id


# class OrderInquiryItem(models.Model):

#     inquiry = models.ForeignKey(
#         OrderInquiry,
#         on_delete=models.CASCADE,
#         related_name='items'
#     )

#     product = models.ForeignKey(
#         Product,
#         on_delete=models.PROTECT
#     )

#     quantity = models.PositiveIntegerField(
#         default=1
#     )

#     price_at_inquiry = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         null=True,
#         blank=True
#     )

#     def __str__(self):
#         return f"{self.product.name} × {self.quantity}"