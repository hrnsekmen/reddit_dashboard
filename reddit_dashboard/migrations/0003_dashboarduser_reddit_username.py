# Generated by Django 3.1.2 on 2020-10-17 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reddit_dashboard', '0002_auto_20201017_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboarduser',
            name='reddit_username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
