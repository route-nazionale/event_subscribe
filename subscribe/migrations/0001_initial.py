# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'base', b'__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'ScoutChiefEventSubscribe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'event', models.ForeignKey(to=b'base.Event', to_field='id')),
                (b'subscribed_on', models.DateTimeField(auto_now_add=True)),
                (b'unsubscribed_on', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': b'iscrizione evento',
                'verbose_name_plural': b'iscrizioni eventi',
            },
            bases=(models.Model,),
        ),
    ]
