# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20140604_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoutchief',
            name='is_spalla',
            field=models.BooleanField(default=False, help_text="questo capo verr\xe0 iscritto dalla 'pattuglia eventi' con criteri supersonici", verbose_name='\xe8 un capo spalla'),
            preserve_default=True,
        ),
    ]
