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
    '🇸🇦': 'ar-SA',   # アラビア語
    '🇧🇬': 'bg',      # ブルガリア語
    '🇨🇳': 'zh',      # 中国語
    '🇨🇿': 'cs',      # チェコ語
    '🇩🇰': 'da',      # デンマーク語
    '🇳🇱': 'nl',      # オランダ語
    '🇬🇧': 'en',      # 英語
    '🇪🇪': 'et',      # エストニア語
    '🇫🇮': 'fi',      # フィンランド語
    '🇫🇷': 'fr',      # フランス語
    '🇩🇪': 'de',      # ドイツ語
    '🇬🇷': 'el',      # ギリシャ語
    '🇭🇺': 'hu',      # ハンガリー語
    '🇮🇩': 'id',      # インドネシア語
    '🇮🇹': 'it',      # イタリア語
    '🇯🇵': 'ja-JP',   # 日本語
    '🇰🇷': 'ko',      # 韓国語
    '🇱🇻': 'lv',      # ラトビア語
    '🇱🇹': 'lt',      # リトアニア語
    '🇳🇴': 'no',      # ノルウェー語
    '🇵🇱': 'pl',      # ポーランド語
    '🇵🇹': 'pt',      # ポルトガル語
    '🇷🇴': 'ro',      # ルーマニア語
    '🇷🇺': 'ru-RU',   # ロシア語
    '🇸🇰': 'sk',      # スロバキア語
    '🇸🇮': 'sl',      # スロベニア語
    '🇪🇸': 'es',      # スペイン語
    '🇸🇪': 'sv',      # スウェーデン語
    '🇹🇷': 'tr',      # トルコ語
    '🇺🇦': 'uk',      # ウクライナ語
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
