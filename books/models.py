from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import uuid

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cover = models.ImageField(upload_to='covers/', height_field=None, width_field=None, max_length=None, blank=True)

    class Meta:
        permissions = [
            ('special_status', 'Can read all books'),
            ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])


class Review(models.Model):

    book = models.ForeignKey(Book, 
        related_name='reviews', 
        on_delete=models.CASCADE)
    
    review = models.CharField(max_length=255)

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return self.review

    def get_absolute_url(self):
        return reverse("Reviews_detail", args=[str(self.id)])



 