from functools import cached_property

from django.db import models
from django.forms import model_to_dict

from core.models import TimeStampedModel
from accounts.models import User


class Post(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()

    @cached_property
    def to_dict(self):
        result = model_to_dict(self)
        result['user'] = self.user.to_dict
        result['created_at'] = self.created_at
        return result
