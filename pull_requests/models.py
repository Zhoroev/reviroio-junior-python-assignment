from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRequest(models.Model):
    link_github = models.URLField(max_length=128)


class UserRequestResult(models.Model):
    name = models.CharField(max_length=200,)
    reviewer = models.CharField(max_length=200,)
    assignee = models.CharField(max_length=200,)
    link = models.URLField(max_length=128)
    user_req_link = models.ForeignKey(UserRequest,
                                      on_delete=models.CASCADE,
                                      related_name='result', )



