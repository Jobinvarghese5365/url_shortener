from django.db import models
import string
import random
from django.urls import reverse

class Url(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=15, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.original_url

    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.short_code = self.generate_short_code()
        return super().save(*args, **kwargs)
    
    def generate_short_code(self):
        characters = string.ascii_letters + string.digits
        short_code = ''.join(random.choice(characters) for _ in range(6))
        return short_code