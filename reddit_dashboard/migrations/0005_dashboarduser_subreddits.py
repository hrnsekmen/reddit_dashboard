# Generated by Django 3.1.2 on 2020-10-18 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reddit_dashboard', '0004_discordserver_subreddit'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboarduser',
            name='subreddits',
            field=models.ManyToManyField(to='reddit_dashboard.Subreddit'),
        ),
    ]