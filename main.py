from config import TOKEN

import discord
from discord import app_commands

from datetime import datetime
import asyncio

intents = discord.Intents.default()
intents.message_content = True # メッセージを読むことを可能にするには、これが必要
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# bot名の確認
async def daily_task():
    await client.wait_until_ready()
    while not client.is_closed():
        print(f"このbotは{client.user.name}です")
        now = datetime.now()
        next_run = now.replace(day=now.day + 1, hour=0, minute=0, second=0, microsecond=0)
        sleep_time = (next_run - now).total_seconds()
        await asyncio.sleep(sleep_time)

# 単純なメッセージの例
@tree.command(name="hello", description="Hello, world!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"こんにちは、{interaction.user.mention}さん！", ephemeral=True) # ephemeral=Trueで他のユーザーには見えないメッセージを送信

# 引数で何か受け取る例
@tree.command(name="args", description="argsコマンドの説明をここに追加する")
@app_commands.default_permissions(administrator=True) # 管理者権限を必要とするようにする
@app_commands.describe(strings='文字列', integers='整数', select_str='選択文字列', select_bool='選択真偽値')
@app_commands.choices(
    select_str=[
        discord.app_commands.Choice(name="ピースフル",value="peaceful"),
        discord.app_commands.Choice(name="イージー",value="easy"),
        discord.app_commands.Choice(name="ノーマル",value="normal"),
        discord.app_commands.Choice(name="ハード",value="hard")
    ],
    select_bool=[
        discord.app_commands.Choice(name="はい",value=1),
        discord.app_commands.Choice(name="いいえ",value=0)
    ]
)
async def args(interaction: discord.Interaction, strings: str, integers: int, select_str: str, select_bool: int): # 真偽値はint型で受け取り、後で変換する
    embed = discord.Embed(
        title="embedのタイトル",
        color=0x00ff00,
        description=f"文字列：{strings}\n" + f"整数を×3すると：{integers * 3}\n" + f"選択文字列：{select_str}\n" + "選択真偽値がTrueの場合、このメッセージは他のユーザーには見えません。"
        )
    await interaction.response.send_message(embed=embed, ephemeral=bool(select_bool))

# 成功のembedの例
def success():
    embed = discord.Embed(
        title="成功",
        color=0x00ff00, # 緑
        description="成功しました。"
        )
    return embed

# エラーのembedの例
def error():
    embed = discord.Embed(
        title="エラー",
        color=0xff0000, # 赤
        description="エラーが発生しました。"
        )
    return embed

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Template Bot"))
    await tree.sync()
    print("login complete")
    client.loop.create_task(daily_task())

client.run(TOKEN)