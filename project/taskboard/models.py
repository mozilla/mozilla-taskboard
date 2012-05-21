from datetime import datetime

from django.db import models
from django.db.models import signals as dbsignals
from django.dispatch import receiver
from django.core.urlresolvers import reverse

from elasticutils import S
from elasticutils.models import SearchMixin
from tower import ugettext_lazy as _
from uuslug import uuslug as slugify

from users.models import UserProfile


class Task(SearchMixin, models.Model):
    contact = models.ForeignKey(UserProfile, verbose_name=_(u'Contact'),
                                related_name="contact_for")
    summary = models.CharField(_(u'Summary'), max_length=255)
    slug = models.CharField(_(u'Slug'), max_length=255, default="")
    instructions = models.TextField(_(u'Instructions'), blank=True)
    deadline = models.DateField(_(u'Deadline'), blank=True, null=True,
                                help_text=_(u'yyyy-mm-dd'))
    created = models.DateTimeField(_(u'Created Date'), default=datetime.utcnow,
                                   editable=False)
    assigned = models.DateField(_(u'Assigned'), blank=True, null=True,
                                help_text=_(u'yyyy-mm-dd'))
    accepted_by = models.ForeignKey(UserProfile, blank=True, null=True,
                                    verbose_name=_(u'Accepted by'),
                                    related_name='accepted_tasks')
    disabled = models.BooleanField(_(u'Disabled'), default=False)
    created_by = models.ForeignKey(UserProfile, blank=True, null=True,
                                   verbose_name=_(u'Created by'),
                                   related_name='created_tasks')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.summary, instance=self)
        super(Task, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{0} ({1})'.format(self.summary, self.contact)

    def fields(self):
        attrs = ('id', 'summary', 'instructions', 'deadline',
                 'created', 'disabled')
        return dict((a, getattr(self, a)) for a in attrs)

    @classmethod
    def search(cls, query):
        query = query.lower().strip()
        fields = ('summary__text', 'summary__startswith',
                  'instructions__text')
        q = dict((field, query) for field in fields)
        s = S(cls).query(or_=q).filter(disabled=False)
        return s

    def user_can_edit(self, user):
        # TODO: use django-guardian
        if user.is_anonymous():
            return False
        profile = user.get_profile()
        return (self.contact == profile
                or self.created_by == profile
                or user.is_superuser)

    def get_absolute_url(self):
        return reverse('view_task', args=[self.slug])


@receiver(dbsignals.post_save, sender=Task)
def update_search_index(sender, instance, **kw):
    from elasticutils import tasks as es_tasks
    es_tasks.index_objects.delay(Task, [instance.id])


# This may not be used. Thats ok; it allows us to use Task.delete()
@receiver(dbsignals.post_delete, sender=Task)
def remove_from_search_index(sender, instance, **kw):
    from elasticutils import tasks as es_tasks
    es_tasks.unindex_objects.delay(sender, [instance.id])
