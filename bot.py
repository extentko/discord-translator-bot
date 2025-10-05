import discord
from deep_translator import GoogleTranslator
from langdetect import detect
import os

# 🔹 Токен береться з Environment Variable на Render
TOKEN = os.environ.get("TOKEN")

# 🔹 Вкажи ID каналу перекладу
TRANSLATOR_CHANNEL_ID = 1424469331407929564  # заміни на свій канал

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# 🔹 Мапа мов для перекладу
LANGUAGES = ["da", "uk", "en"]

def translate_message(text, src_lang):
    translations = {}
    for lang in LANGUAGES:
        if lang != src_lang:
            translated = GoogleTranslator(source=src_lang, target=lang).translate(text)
            translations[lang] = translated
    return translations

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    # Не реагуємо на власні повідомлення
    if message.author == client.user:
        return

    # Переклад тільки в певному каналі
    if message.channel.id != TRANSLATOR_CHANNEL_ID:
        return

    try:
        detected_lang = detect(message.content)
    except:
        return  # Якщо не вдалося визначити мову

    if detected_lang not in LANGUAGES:
        return  # Якщо мова не підтримується

    translations = translate_message(message.content, detected_lang)

    # Відправляємо переклади
    for lang, text in translations.items():
        flag = {
            "da": "🇩🇰",
            "uk": "🇺🇦",
            "en": "🇬🇧"
        }.get(lang, "")
        await message.channel.send(f"{flag} ➜ {text}")
print(f"TOKEN: {TOKEN}")
client.run(TOKEN)
