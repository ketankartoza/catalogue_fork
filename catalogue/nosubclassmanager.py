from django.db import models, connection
from django.db.models import signals

class NoSubclassManager(models.Manager):
  """
  Custom manager that excludes subclasses.
  from http://djangosnippets.org/snippets/950/
  see also: 
  """
  def __init__(self, *args, **kwargs):
    super(NoSubclassManager, self).__init__(*args, **kwargs)
    self.excludes = []

  def _class_prepared(self, sender, **kwargs):
    # add the subclass to our list of excluded models
    if self.model in sender._meta.parents:
      self.excludes.append(sender)

  def contribute_to_class(self, model, name):
    super(NoSubclassManager, self).contribute_to_class(model, name)
    # connect the signal to pick up on subclasses
    signals.class_prepared.connect(self._class_prepared)

  def get_query_set(self):
    qn = connection.ops.quote_name
    return super(NoSubclassManager, self).get_query_set().extra(
        where=['''not exists (select 1 from %s where %s.%s = %s)'''
         % (
        qn(model._meta.db_table),
        qn(model._meta.db_table),
        qn(model._meta.pk.column),
        qn(self.model._meta.pk.column)
        ) for model in self.excludes])
