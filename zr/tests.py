from django.test import TestCase
from django.contrib.auth.models import User
from zr.models import Configuration, Geometry, Plan, Subjects, Post, PostSubscription


class TestPostClass(TestCase):

    def setUp(self):
        g = Geometry(
            name="Test",
            poly="POLYGON ((-29.5312499958896630 77.0295586711385596, -67.4999999906039108 74.6251009596365122, -60.4687499915822144 58.5166517940893414, 26.7187499962811614 58.5166517940893414, -29.5312499958896630 77.0295586711385596))")
        g.save()

        self.plan = Plan(
            name="testplan",
            area="POLYGON ((-29.5312499958896630 77.0295586711385596, -67.4999999906039108 74.6251009596365122, -60.4687499915822144 58.5166517940893414, 26.7187499962811614 58.5166517940893414, -29.5312499958896630 77.0295586711385596))",
            zoom_level=5)
        self.plan.save()

        s = Subjects(geometry=g, plan=self.plan, label="Test")
        s.save()

        self.configuration = Configuration(
            plan = self.plan,
            side = 'L',
            max = 40,
            min = 10,
            default = 30)
        self.configuration.save()

        self.user = User.objects.create_user('test', 'lalala')
        self.user.save()

    def test_get_root(self):
        root = Post(author=self.user, plan=self.plan, content='post1')
        root.save()
        p1 = Post(author=self.user, plan=self.plan, content='post1', parent=root)
        p1.save()
        p2 = Post(author=self.user, plan=self.plan, content='post1', parent=root)
        p2.save()
        p11 = Post(author=self.user, plan=self.plan, content='post1', parent=p1)
        p11.save()
        p111 = Post(author=self.user, plan=self.plan, content='post1', parent=p11)
        p111.save()

        self.assertEqual(root, root.get_root(), msg="self is root")
        self.assertEqual(root, p1.get_root(), msg="self.parent is root")
        self.assertEqual(root, p2.get_root(), msg="similar to p1")
        self.assertEqual(root, p11.get_root(), msg="second level")
        self.assertEqual(root, p111.get_root(), msg="third level")

    def test_notification_signal(self):
        from notification.models import NoticeQueueBatch

        root = Post(author=self.user, plan=self.plan, content='post1')
        root.save()
        p1 = Post(author=self.user, plan=self.plan, content='post1', parent=root)
        p1.save()
        queue_length = len(NoticeQueueBatch.objects.all())
        self.assertEqual(0, queue_length, msg="no post subscription, should be 0 after new post")

        subscription = PostSubscription(post=root, user=self.user, active=True)
        subscription.save()

        p2 = Post(author=self.user, plan=self.plan, content='post1', parent=root)
        p2.save()

        queue_length = len(NoticeQueueBatch.objects.all())
        self.assertEqual(1, queue_length, msg="1 direct child")

        p11 = Post(author=self.user, plan=self.plan, content='post1', parent=p1)
        p11.save()
        queue_length = len(NoticeQueueBatch.objects.all())
        self.assertEqual(2, queue_length, msg="2 direct comments")

        p111 = Post(author=self.user, plan=self.plan, content='post1', parent=p11)
        p111.save()
        queue_length = len(NoticeQueueBatch.objects.all())
        self.assertEqual(3, queue_length, msg="2 direct + 1 subpost")

        pX = Post(author=self.user, plan=self.plan, content='post1')
        pX.save()
        queue_length = len(NoticeQueueBatch.objects.all())
        self.assertEqual(3, queue_length, msg="still 3 notification, new not subscribed thread")
