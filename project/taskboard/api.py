from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from taskboard.models import Task


class TaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.all()

