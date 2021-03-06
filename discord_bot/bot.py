import discord
from discord.ext import tasks
import redis
import json
from asgiref.sync import sync_to_async
from reddit_dashboard.redis_connection import REDIS_CONNECTION, RedisConsts
from reddit_dashboard.redis_serializers import RedisModelSerializer


REDIS_KEY = RedisConsts.DISCORD_PUSH
client = discord.Client()


class PushPayload:
    def __init__(self, pid, post_id, text_channel_id, server_id, url, text, title):
        self.id = pid
        self.post_id = post_id
        self.text_channel_id = text_channel_id
        self.server_id = server_id
        self.url = url
        self.text = text
        self.title = title

    @classmethod
    def serialize(cls, payload):
        return cls(
            pid=payload["id"],
            post_id=payload["post_id"],
            text_channel_id=payload["text_channel_id"],
            server_id=payload["server_id"],
            url=payload["url"],
            text=payload["text"],
            title=payload["title"],
        )


@tasks.loop(seconds=1)
async def redis_listener():
    await client.wait_until_ready()
    value = REDIS_CONNECTION.lpop(REDIS_KEY)
    if value:
        data = json.loads(value)
        data = PushPayload.serialize(data)
        url = 'https://reddit.com' + data.url
        text = discord.Embed(
            title=data.title,
            url=url,
            description=data.text[:100])
        subreddit = "r/" + data.url.split("/")[2]
        text.set_author(url="https://reddit.com/" + subreddit, name=subreddit)
        guild = client.get_guild(int(data.server_id))
        if guild:
            channel = guild.get_channel(int(data.text_channel_id))
            if channel:
                try:
                    await client.get_guild(int(data.server_id)).get_channel(int(data.text_channel_id)).send(embed=text)
                except:
                    print(f"Submission sent error : {data.id}")


@client.event
async def on_ready():
    print("Bot connected")
    redis_listener.start()


@client.event
async def on_guild_join(guild):
    """
    Get guild id, name and text channels
    """
    # Not saving models in async functions bc of mysql gone away error
    # django.db.utils.OperationalError: (2006, 'MySQL server has gone away')

    model = RedisModelSerializer(guild.id, guild.name)
    for channel in guild.channels:
        if str(channel.type) == 'text':
            model.add_channel(channel.name, channel.id)

    model.push()

