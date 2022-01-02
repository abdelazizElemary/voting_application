# Generated by Django 4.0 on 2022-01-02 17:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='voter',
        ),
        migrations.AddField(
            model_name='poll',
            name='voter',
            field=models.ManyToManyField(blank=True, null=True, related_name='polls', to=settings.AUTH_USER_MODEL),
        ),
    ]