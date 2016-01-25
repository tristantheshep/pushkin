# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0003_tag_tag_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='tag_id',
        ),
        migrations.AddField(
            model_name='tag',
            name='text',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
    ]
