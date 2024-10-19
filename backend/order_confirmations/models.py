from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from main.models import Order


class OrderConfirmation(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    confirmed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="confirmations"
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )  # Add price field

    def __str__(self):
        return f"Confirmation for Order {self.order.id} (Completed: {self.completed})"

    def time_to_complete(self):
        if self.confirmed_at and self.completed_at:
            return self.completed_at - self.confirmed_at
        return None
