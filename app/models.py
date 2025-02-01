from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the category (e.g., Electronics, Clothing, Accessories)."
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional detailed description of the category."
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]


class LostAndFoundItem(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]

    item = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='lost_and_found_images/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item} ({self.get_status_display()})"

    def get_absolute_url(self):
        return reverse('lost-item-view', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-date']
        verbose_name = "Lost and Found Item"
        verbose_name_plural = "Lost and Found Items"



