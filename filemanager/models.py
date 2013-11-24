__author__ = 'marcinra'

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from zr.models import Post


class PostFileUpload(models.Model):
    name = models.CharField(max_length=250)
    file = models.FileField(upload_to = 'file_uploads')
    post = models.ForeignKey(Post, related_name="filep")

    def __unicode__(self):
        return self.name

    def to_dict(self):
        ret = { 'name':self.name, 'file':self.file.name, 'post':self.post.id }
        return ret

    def remove_file(self):
        import os
        os.remove(self.file.path)

def deleteMapFile(sender, instance, **kwargs):
    instance.remove_file()

post_delete.connect(deleteMapFile, sender=PostFileUpload)