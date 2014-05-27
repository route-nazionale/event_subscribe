# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'base', b'0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'EventPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'person', models.ForeignKey(to=b'base.Person', to_field='id')),
                (b'event_happening', models.ForeignKey(to=b'base.EventHappening', to_field='id')),
                (b'role', models.CharField(default=b'ANIMATOR', max_length=16, choices=[(b'ANIMATOR', b'animatore'), (b'RELATOR', b'relatore'), (b'MODERATOR', b'moderatore'), (b'REFERRED', b'referente')])),
                (b'contacts', models.CharField(help_text=b'codifica dei contatti di una persona. Ad es: cell:328111111, mail:a@a.com', max_length=512, verbose_name=b'contatti', blank=True)),
            ],
            options={
                'db_table': b'camp_eventhappeningpeople',
                'verbose_name': b'riferimento evento',
                'verbose_name_plural': b'riferimenti evento',
            },
            bases=(models.Model,),
        ),
    ]
