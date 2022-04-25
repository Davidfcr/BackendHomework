from django.db import models
from user.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


class Film(models.Model):
    title = models.CharField(_('title'), blank=False, max_length=128)
    director = models.CharField(_('director'), blank=False, max_length=128)
    rating = models.IntegerField(_('rating'), default=1, validators=[
        MaxValueValidator(10),
        MinValueValidator(1)
    ])
    description = models.TextField(_('description'), blank=False)
    is_private = models.BooleanField(_('private item'), default=False)
    added_by = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
