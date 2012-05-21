from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from taskboard import views

urlpatterns = patterns('',
    url(r'^new/$', views.CreateTask.as_view(),
        name="new_task"),
    url(r'^(?P<slug>[a-z0-9-]+)/$',
        login_required(never_cache(views.ViewTask.as_view())),
        name="view_task"),
    url(r'^(?P<slug>[a-z0-9-]+)/edit/$',
        login_required(never_cache(views.EditTask.as_view())),
        name="edit_task"),
    url(r'^$', (views.ListTasks.as_view()),
        name="list_tasks"),
)
