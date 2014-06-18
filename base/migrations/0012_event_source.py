# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'base', b'0011_auto_20140606_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name=b'event',
            name=b'source',
            field=models.TextField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
