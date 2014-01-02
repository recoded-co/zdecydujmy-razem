__author__ = 'dwa'
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, DATETIME

from zr.models import Post


"""
    author = models.ForeignKey(User, related_name='posts')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='comments')
    plan = models.ForeignKey(Plan, related_name='posts')
    content = models.TextField()
    geometry = models.ForeignKey(Geometry, null=True, blank=True)
    subscriptions = models.ManyToManyField(User, through="PostSubscription", null=True, blank=True)
    date = models.DateField(auto_now=True, blank=True)
"""


class Index():

    IDX_DIR = 'zr_index'

    SCHEMA = Schema(id=ID, author=TEXT, content=TEXT)

    def get_queryset(self, date):
        return Post.objects.filter(date__gt=date)

    def get_or_create_folder(self):
        import os
        if not os.path.exists(self.IDX_DIR):
            os.mkdir(self.IDX_DIR)
            return index.create_in(self.IDX_DIR, self.SCHEMA), True
        else:
            return index.open_dir(self.IDX_DIR), False

    def write_post(self, writer, post):
        utf_content = post.content
        print utf_content
        utf_username = post.author.get_username()
        print utf_username
        writer.add_document(id=post.id, author=utf_username, content=utf_content)

    def create_new_index(self):
        from datetime import date, datetime
        from zdecydujmyrazem import base

        ix = index.create_in(self.IDX_DIR, self.SCHEMA), True
        entries = self.get_queryset(base.INDEX_LAST_UPDATE)# TODO !
        writer = ix.writer()
        for e in entries:
            self.write_post(writer, e)
        writer.commit()
        base.INDEX_LAST_UPDATE = date.today()

    def update_index(self):
        from datetime import date, datetime
        from zdecydujmyrazem import base

        ix, created = self.get_or_create_folder()
        entries = self.get_queryset(base.INDEX_LAST_UPDATE)# TODO !
        writer = ix.writer()
        for e in entries:
            self.write_post(writer, e)
        writer.commit()
        base.INDEX_LAST_UPDATE = date.today()


