from django.db import models
import uuid
# Create your models here.
class Room(models.Model):
  id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=200)
  description = models.TextField(null=True, blank=True)
  #  alllows null & blank description
  # paticipants = 
  updated = models.DateTimeField(auto_now=True) 
  created = models.DateTimeField(auto_now_add=True) 
  # topic host
  def __str__(self):
    return self.name
