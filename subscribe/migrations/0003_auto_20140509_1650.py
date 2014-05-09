# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'subscribe', b'0002_scoutchiefeventsubscribe_scout_chief'),
    ]

    operations = [
        migrations.AlterField(
            model_name=b'scoutchiefeventsubscribe',
            name=b'scout_chief',
            field=models.ForeignKey(to=b'base.ScoutGroup', to_field='id'),
        ),
    ]
