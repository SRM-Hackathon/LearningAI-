# Generated by Django 2.0.2 on 2018-10-12 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('studyobjects', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userenvironment',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.TeamMembership'),
        ),
        migrations.AddField(
            model_name='task',
            name='assessment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studyobjects.Assessment'),
        ),
        migrations.AddField(
            model_name='task',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.TeamMembership'),
        ),
        migrations.AddField(
            model_name='task',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studyobjects.Tag'),
        ),
        migrations.AddField(
            model_name='tag',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studyobjects.Course'),
        ),
        migrations.AddField(
            model_name='session',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studyobjects.Task'),
        ),
        migrations.AddField(
            model_name='session',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.TeamMembership'),
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='instructing_courses', to='user.TeamMembership'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='courses', to='user.TeamMembership'),
        ),
        migrations.AddField(
            model_name='course',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Team'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='studyobjects.Course'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.TeamMembership'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='tags',
            field=models.ManyToManyField(to='studyobjects.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together={('name', 'assessment')},
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together={('course', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('name', 'team')},
        ),
        migrations.AlterUniqueTogether(
            name='assessment',
            unique_together={('course', 'name')},
        ),
    ]