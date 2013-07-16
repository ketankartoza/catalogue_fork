import datetime

from django.conf import settings
from django.contrib.contenttypes import models as ct_models
from django.contrib.auth.models import Group, Permission, User
from django import VERSION as DJANGO_VERSION


if DJANGO_VERSION[:2] >= (1, 4):
    from django.utils import timezone

import factory


class ContentTypeF(factory.django.DjangoModelFactory):
    FACTORY_FOR = ct_models.ContentType

    name = factory.Sequence(lambda n: "content type %s" % n)


class PermissionF(factory.django.DjangoModelFactory):
    FACTORY_FOR = Permission

    name = factory.Sequence(lambda n: "permission%s" % n)
    content_type = factory.SubFactory(ContentTypeF)
    codename = factory.Sequence(lambda n: "factory_%s" % n)


class GroupF(factory.django.DjangoModelFactory):
    FACTORY_FOR = Group

    @classmethod
    def _setup_next_sequence(cls):
        try:
            return cls._associated_class.objects.values_list(
                'id', flat=True).order_by('-id')[0] + 1
        except IndexError:
            return 0

    name = factory.Sequence(lambda n: "group%s" % n)


class UserF(factory.django.DjangoModelFactory):
    FACTORY_FOR = User

    @classmethod
    def _setup_next_sequence(cls):
        try:
            return cls._associated_class.objects.values_list(
                'id', flat=True).order_by('-id')[0] + 1
        except IndexError:
            return 0

    username = factory.Sequence(lambda n: "username%s" % n)
    first_name = factory.Sequence(lambda n: "first_name%s" % n)
    last_name = factory.Sequence(lambda n: "last_name%s" % n)
    email = factory.Sequence(lambda n: "email%s@example.com" % n)
    password = 'sha1$caffc$30d78063d8f2a5725f60bae2aca64e48804272c3'
    is_staff = False
    is_active = True
    is_superuser = False
    if DJANGO_VERSION[:2] >= (1, 4) and settings.USE_TZ:
        last_login = timezone.datetime(2000, 1, 1).replace(tzinfo=timezone.utc)
        date_joined = timezone.datetime(1999, 1, 1).replace(
            tzinfo=timezone.utc)
    else:
        last_login = datetime.datetime(2000, 1, 1)
        date_joined = datetime.datetime(1999, 1, 1)
