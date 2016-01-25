# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_auto_20160125_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='tag_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
