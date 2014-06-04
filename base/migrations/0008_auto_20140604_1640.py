# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20140527_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventhappening',
            name='seats_n_chiefs',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventhappening',
            name='seats_n_boys',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='event',
            name=b'seats_n_boys',
        ),
        migrations.RemoveField(
            model_name='event',
            name=b'seats_n_chiefs',
        ),
    ]
