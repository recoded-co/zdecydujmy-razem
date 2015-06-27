__author__ = 'dwa'
from django.conf import settings
from whoosh import index, query
from whoosh.fields import Schema, ID, NGRAMWORDS, NUMERIC, DATETIME, TEXT
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.qparser.dateparse import DateParserPlugin


"""
    author = models.ForeignKey(User, related_name='posts')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='comments')
    plan = models.ForeignKey(Plan, related_name='posts')
    content = models.TextField()
    geometry = models.ForeignKey(Geometry, null=True, blank=True)
    subscriptions = models.ManyToManyField(User, through="PostSubscription", null=True, blank=True)
    date = models.DateField(auto_now=True, blank=True)
"""

from settings.conf import IDX_DIR


SCHEMA = Schema(
    id=ID(stored=True),
    plan_id=NUMERIC(),
    author=TEXT(stored=True),
    content=TEXT(stored=True),
    date=DATETIME(stored=True)
)


def get_or_create_index(force_create=False):
    print 'get_od_create'
    import os
    if not os.path.exists(IDX_DIR):
        os.mkdir(IDX_DIR)
        return index.create_in(IDX_DIR, SCHEMA), True
    else:
        if force_create:
            return index.create_in(IDX_DIR, SCHEMA), True
        else:
            return index.open_dir(IDX_DIR), False


def write_post(writer, post):
    print 'write_post'
    utf_content = post.content
    utf_username = post.author.username
    writer.add_document(id=unicode(post.id), plan_id=post.plan.id, author=utf_username, content=utf_content, date=post.date)


def create_new_index():
    from zr.models import Post
    ix, created = get_or_create_index(force_create=True)#index.create_in(IDX_DIR, SCHEMA)
    entries = Post.objects.all()
    print len(entries)
    writer = ix.writer()
    for e in entries:
        write_post(writer, e)
    writer.commit()


def update_index(post):
    ix, created = get_or_create_index()
    writer = ix.writer()
    write_post(writer, post)
    writer.commit()

"""
    In order to search date, use: "date:2014-05-16" query
"""
def find(uquery, plan_id):
    uquery = uquery[:-1] if uquery.endswith('/') else uquery
    try:
        ix, created = get_or_create_index()
        qp = MultifieldParser(['content', 'author', 'date'], schema=SCHEMA)
        qp.add_plugin(DateParserPlugin())
        allow_q = query.Term('plan_id', plan_id)
        q = qp.parse(''.join(['*', uquery, '*']))
        results = ix.searcher().search(q, filter=allow_q)
        return [int(r['id']) for r in results]
    except Exception, e:
        print e
        # TODO log exception
        return []
