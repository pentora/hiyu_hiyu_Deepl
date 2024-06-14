import os
import discord
from discord.ext import commands
import requests

# Discordのボットトークンを環境変数から取得
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# DeepL APIキーも同様に環境変数から取得する場合の例
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')

# intentsを設定
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

# コマンドプレフィックスを設定
bot = commands.Bot(command_prefix='!', intents=intents)

# ボットが起動したときに呼ばれるイベント
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# 国旗の絵文字に対応するターゲット言語を定義
flag_to_language = {
    '🇯🇵': 'JA',  # 日本語
    '🇺🇸': 'EN',  # 英語
    '🇫🇷': 'FR',  # フランス語
    '🇩🇪': 'DE',  # ドイツ語
    '🇪🇸': 'ES',  # スペイン語
    '🇮🇹': 'IT',  # イタリア語
    # 必要に応じて他の国旗と言語のペアを追加してください
}

# リアクションが追加されたときに呼ばれるイベント
@bot.event
async def on_reaction_add(reaction, user):
    # ボット自身のリアクションは無視する
    if user.bot:
        return

    # リアクションが国旗の絵文字であるかチェック
    if reaction.emoji in flag_to_language:
        # 元のメッセージを取得
        original_message = reaction.message.content

        # 翻訳先の言語を決定
        target_lang = flag_to_language[reaction.emoji]

        # DeepL APIのエンドポイント
        url = "https://api-free.deepl.com/v2/translate"
        params = {
            'auth_key': DEEPL_API_KEY,
            'text': original_message,
            'target_lang': target_lang
        }
        response = requests.post(url, data=params)
        result = response.json()
        translated_text = result["translations"][0]["text"]

        # 翻訳結果を元のメッセージにリプライ
        await reaction.message.reply(translated_text)

# ボットを実行
bot.run(DISCORD_TOKEN)
