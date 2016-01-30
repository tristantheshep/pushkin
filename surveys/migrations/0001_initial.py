# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('answer_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('question_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=101)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(related_name='surveys', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='SurveyResponse',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('survey', models.ForeignKey(related_name='responses', to='surveys.Survey')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('tag_text', models.CharField(max_length=20)),
                ('survey', models.ForeignKey(related_name='tag_options', to='surveys.Survey')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(related_name='questions', to='surveys.Survey'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answers', to='surveys.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='response',
            field=models.ForeignKey(related_name='answers', to='surveys.SurveyResponse'),
        ),
        migrations.AddField(
            model_name='answer',
            name='tags',
            field=models.ManyToManyField(to='surveys.Tag'),
        ),
    ]
