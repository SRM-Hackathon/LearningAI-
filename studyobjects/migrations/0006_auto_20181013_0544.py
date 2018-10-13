# Generated by Django 2.0.2 on 2018-10-13 05:44

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('studyobjects', '0005_auto_20181013_0518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doubtsclarified',
            name='doubt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clarifications', to='studyobjects.Doubts'),
        ),
        migrations.AlterField(
            model_name='task',
            name='eta',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 13, 6, 44, 58, 191721, tzinfo=utc)),
        ),
    ]
