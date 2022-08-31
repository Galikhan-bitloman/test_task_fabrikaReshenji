# Generated by Django 4.1 on 2022-08-30 11:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mailings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailings_id', models.UUIDField(default=uuid.UUID('be53fa39-0004-48e2-a560-01ef083b7e40'), verbose_name="Mailing's id")),
                ('start_date', models.DateTimeField(auto_now=True, verbose_name='Starting date to mail')),
                ('start_time', models.TimeField(auto_now=True, verbose_name='Starting time to mail')),
                ('end_date', models.DateTimeField(auto_now=True, verbose_name='End of date to mail')),
                ('end_time', models.TimeField(auto_now=True, verbose_name='End of time to mail')),
            ],
        ),
    ]