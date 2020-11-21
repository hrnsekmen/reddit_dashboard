from celery.task import periodic_task, task
from datetime import timedelta
from reddit_dashboard.models import TextChannel, Posts
from api.reddit.manager import reddit_manager
from reddit_dashboard.redis_connection import RedisConsts, REDIS_CONNECTION
from reddit_dashboard.redis_serializers import RedisModelSerializer
from celery.signals import celeryd_init
from discord_bot.bot import client
from reddit_dashboard.settings import DISCORD_BOT_TOKEN
from reddit_dashboard.celery_loader import app
import asyncio


# celery -A reddit_dashboard beat -l info
# celery -A reddit_dashboard worker --pool=solo -l info // for windows


#@periodic_task(run_every=timedelta(minutes=15))
def get_hot_posts():
    following_subreddits = []
    for rel_data in TextChannel.following_subreddits.through.objects.all():
        if rel_data.subreddit not in following_subreddits:
            following_subreddits.append(rel_data.subreddit)

    for following_subreddit in following_subreddits:
        subreddit = reddit_manager.get_subreddit(display_name=following_subreddit.name)

        for submission in subreddit.hot():
            try:
                Posts.create(submission, subreddit=following_subreddit)
            except Exception as ex:
                print(ex)


@periodic_task(name='reddit_dashboard.tasks.test_task', run_every=timedelta(seconds=5))
def test_task(*args, **kwargs):
    print("TASK ÇALIŞIYOR!")


@periodic_task(name="discord_server_pushes", run_every=timedelta(seconds=5))
def discord_server_pushes(*args, **kwargs):
    payload = REDIS_CONNECTION.lpop(RedisConsts.SERVER_PUSH)
    if payload:
        RedisModelSerializer.serialize(payload)







