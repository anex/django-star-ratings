from random import randint
from django.contrib.auth import get_user_model
from django.test import TestCase
from model_mommy import mommy
from star_ratings.models import AggregateRating, Rating
from .models import Foo, Bar


class RatingStr(TestCase):
    def test_result_contains_user_id_and_aggregate_rating_name(self):
        user = mommy.make(get_user_model())
        foo = mommy.make(Foo)

        aggregate = AggregateRating.objects.rate(foo, 1, user, '0.0.0.0')
        rating = aggregate.ratings.get(user=user)

        self.assertEqual('{} rating {} for {}'.format(user, rating.score, aggregate.content_object, aggregate.content_object), str(rating))


class RatingHasRated(TestCase):
    def setUp(self):
        self.foo = mommy.make(Foo)
        self.bar = mommy.make(Bar)
        self.user_a = mommy.make(get_user_model())
        self.user_b = mommy.make(get_user_model())

    def test_user_has_rated_the_model___results_is_true(self):
        AggregateRating.objects.rate(self.foo, randint(1, 5), self.user_a, '0.0.0.0')

        self.assertTrue(Rating.objects.has_rated(self.foo, self.user_a))

    def test_different_user_has_rated_the_model___results_is_false(self):
        AggregateRating.objects.rate(self.foo, randint(1, 5), self.user_a, '0.0.0.0')

        self.assertFalse(Rating.objects.has_rated(self.foo, self.user_b))

    def test_user_has_rated_a_different_model___results_is_false(self):
        AggregateRating.objects.rate(self.foo, randint(1, 5), self.user_a, '0.0.0.0')

        self.assertFalse(Rating.objects.has_rated(self.bar, self.user_a))

    def test_user_has_rated_a_different_model_instance___results_is_false(self):
        foo2 = mommy.make(Foo)

        AggregateRating.objects.rate(self.foo, randint(1, 5), self.user_a, '0.0.0.0')

        self.assertFalse(Rating.objects.has_rated(foo2, self.user_a))
