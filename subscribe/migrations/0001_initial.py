# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'base', b'0002_eventperson'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'ScoutChiefSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'scout_chief', models.ForeignKey(to=b'base.ScoutChief', to_field='id')),
                (b'event_happening', models.ForeignKey(to=b'base.EventHappening', to_field='id')),
                (b'subscribed_on', models.DateTimeField(auto_now_add=True)),
                (b'unsubscribed_on', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': b'subscriptions',
                'verbose_name': b'iscrizione evento',
                'verbose_name_plural': b'iscrizioni eventi',
            },
            bases=(models.Model,),
        ),
    ]
