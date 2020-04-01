from datetime import datetime, timedelta
import unittest

from tests.base import BaseTestCase
from application.models import db, User, Post, Category


class UserModelCase(BaseTestCase):
    '''test for models.py'''
    def test_password_hashing(self):
        u = User(name='susan', email="sdasd@gmail.com")
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    # def test_avatar(self):
    #     u = User(name='john', email='john@example.com')
    #     self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
    #                                      'd4c74594d841139328695756648b6bd6'
    #                                      '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(name='john', email='john@example.com')
        u2 = User(name='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().name, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().name, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(name='john', email='john@example.com')
        u2 = User(name='susan', email='susan@example.com')
        u3 = User(name='mary', email='mary@example.com')
        u4 = User(name='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="post from john", author=u1, title="fake title",
                  pub_date=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2, title="fake title", 
                  pub_date=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=u3, title="fake title",
                  pub_date=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4, title="fake title",
                  pub_date=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


class PostModelCase(BaseTestCase):
    def test_post(self):
        u1 = User(name='john', email='john@example.com')
        u2 = User(name='susan', email='susan@example.com')
        u3 = User(name='mary', email='mary@example.com')
        u4 = User(name='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        category1 = Category(label="tech")
        category2 = Category(label="music")
        category3 = Category(label="game")
        category4 = Category(label="sport")
        category5 = Category(label="art")
        db.session.add_all([category1, category2, category3, category4, category5])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="post from john", author=u1, title="fake title", 
                  pub_date=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2, title="fake title",
                  pub_date=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=u3, title="fake title", 
                  pub_date=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4, title="fake title",
                  pub_date=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        self.assertFalse(p1.is_category_of(category1))
        self.assertEqual(p1.categories.all(), [])

        p1.add_category(category1)
        p1.add_category(category2)
        p2.add_category(category1)
        p2.add_category(category5)
        p3.add_category(category1)
        p4.add_category(category3)
        db.session.commit()

        self.assertEqual(p1.categories.all(), [category1, category2])
        self.assertCountEqual(category1.posts.all(), [p2, p1, p3])

        p1.delete_category(category1)
        p1.delete_category(category3)
        p1.delete_category(category2)
        db.session.commit()

        self.assertEqual(p1.categories.all(), [])




if __name__ == '__main__':
    unittest.main(verbosity=2)