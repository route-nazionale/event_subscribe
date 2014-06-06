# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoutchiefsubscription',
            name='is_locked',
            field=models.BooleanField(default=False, verbose_name='non si pu\xf2 cancellare'),
            preserve_default=True,
        ),
    ]
