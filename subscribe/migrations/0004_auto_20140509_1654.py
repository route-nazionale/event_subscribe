# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'subscribe', b'0003_auto_20140509_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name=b'scoutchiefeventsubscribe',
            name=b'scout_chief',
            field=models.ForeignKey(to=b'base.ScoutChief', to_field='id'),
        ),
    ]
