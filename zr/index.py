__author__ = 'dwa'
from whoosh import index
from whoosh.fields import Schema, ID, NGRAMWORDS
from whoosh.qparser import QueryParser, MultifieldParser



"""
    author = models.ForeignKey(User, related_name='posts')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='comments')
    plan = models.ForeignKey(Plan, related_name='posts')
    content = models.TextField()
    geometry = models.ForeignKey(Geometry, null=True, blank=True)
    subscriptions = models.ManyToManyField(User, through="PostSubscription", null=True, blank=True)
    date = models.DateField(auto_now=True, blank=True)
"""

IDX_DIR = 'zr_index'

SCHEMA = Schema(
    id=ID(stored=True),
    author=NGRAMWORDS(stored=True),
    content=NGRAMWORDS(stored=True)
)


def get_or_create_index(force_create=False):
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
    utf_content = post.content
    utf_username = post.author.get_username()
    writer.add_document(id=unicode(post.id), author=utf_username, content=utf_content)


def create_new_index():
    from zr.models import Post
    ix, created = get_or_create_index(force_create=True)#index.create_in(IDX_DIR, SCHEMA)
    entries = Post.objects.all()
    writer = ix.writer()
    for e in entries:
        write_post(writer, e)
    writer.commit()


def update_index(post):
    ix, created = get_or_create_index()
    writer = ix.writer()
    write_post(writer, post)
    writer.commit()


def find(query):
    query = query[:-1] if query.endswith('/') else query
    try:
        ix, created = get_or_create_index()
        qp = MultifieldParser(['content', 'author'], schema=SCHEMA)
        q = qp.parse(query)
        results = ix.searcher().search(q)
        return [int(r['id']) for r in results]
    except Exception, e:
        print e
        # TODO log exception
        return []