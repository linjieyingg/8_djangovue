# Generated by Django 5.0.4 on 2024-04-12 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0003_reminder_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reminder',
            options={'ordering': ['date']},
        ),
        migrations.RenameField(
            model_name='reminder',
            old_name='include',
            new_name='homework',
        ),
        migrations.RemoveField(
            model_name='reminder',
            name='time',
        ),
        migrations.AddField(
            model_name='tag',
            name='homework',
            field=models.BooleanField(default=False),
        ),
    ]
