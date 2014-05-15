#-*- coding: utf-8 -*-

from django.contrib.auth.models import User
from base.models import ScoutChief, Unit

class ScoutChiefAuthBackend(object):
    """
    Authentication backend for a ScoutChief
    """

    def authenticate(self, code=None, birth_date=None, unit_name=None):

        # QUESTION: birth_date needs to be pythonized in a datetime object?
        # I think so. Login does not know about kind of credentials it receives
        # TODO Ric

        try:
            unit = Unit.objects.get(name=unit_name)
            scout_chief = ScoutChief.object.get(
                code=code, birth_date=birth_date, unit=unit
            )
        except ScoutChief.DoesNotExist as e:
            return None
        except Unit.DoesNotExist as e:
            return None
        else:
            return scout_chief.user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
