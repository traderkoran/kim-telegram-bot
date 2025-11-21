#!/usr/bin/env python3
"""
Efsanevi Yatırım Eğitim Botu
"""

import logging
import os
import asyncio
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot konfigürasyonu
BOT_TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
DEVELOPER_ID = os.environ.get('DEVELOPER_ID', 'YOUR_DEVELOPER_ID')

# --- RENDER KEEP-ALIVE WEB SUNUCUSU ---
app = Flask('')

@app.route('/')
def home():
    return "Bot aktif! Efsanevi Yatırım Botu çalışıyor."

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ---------------------------------------

# Eğitim İçerikleri
EDUCATION_MODULES = {
    "module_1": {
        "title": "🎯 Temel Kavramlar",
        "description": "Yatırımın temel prensipleri ve piyasa yapısı",
        "lessons": [
            {"id": "lesson_1_1", "title": "Piyasa Psikolojisi", "content": "Piyasa katılımcılarının davranışları ve duygusal etkiler."},
            {"id": "lesson_1_2", "title": "Risk Yönetimi Temelleri", "content": "Risk toleransı ve sermaye koruma stratejileri."},
            {"id": "lesson_1_3", "title": "Piyasa Yapısı Analizi", "content": "Trendler, destek/direnç ve piyasa aşamaları."}
        ]
    },
    "module_2": {
        "title": "📊 Teknik Analiz",
        "description": "Fiyat hareketleri ve grafik formasyonları",
        "lessons": [
            {"id": "lesson_2_1", "title": "Mum Çubuğu Formasyonları", "content": "Tekli, ikili ve üçlü mum formasyonları."},
            {"id": "lesson_2_2", "title": "Grafik Formasyonları", "content": "Omuz Baş Omuz, Üçgen, Bayrak formasyonları."},
            {"id": "lesson_2_3", "title": "Göstergeler ve Osilatörler", "content": "RSI, MACD, Stokastik ve ADX kullanımı."}
        ]
    },
    "module_3": {
        "title": "⚡ İleri Teknikler",
        "description": "Harmonik formasyonlar ve Elliott Dalga Teorisi",
        "lessons": [
            {"id": "lesson_3_1", "title": "Fibonacci Uygulamaları", "content": "Geri çekilme ve uzantı seviyeleri."},
            {"id": "lesson_3_2", "title": "Harmonik Formasyonlar", "content": "Gartley, Kelebek, Yarasa formasyonları."},
            {"id": "lesson_3_3", "title": "Elliott Dalga Analizi", "content": "İtici ve düzeltici dalga yapıları."}
        ]
    },
    "module_4": {
        "title": "🧠 Ticaret Psikolojisi", 
        "description": "Zihinsel disiplin ve duygu yönetimi",
        "lessons": [
            {"id": "lesson_4_1", "title": "Kazanma Zihniyeti", "content": "Disiplin, sabır ve objektiflik."},
            {"id": "lesson_4_2", "title": "Risk Psikolojisi", "content": "Korku ve açgözlülükle başa çıkma."},
            {"id": "lesson_4_3", "title": "Bağımsız Düşünme", "content": "Gurulara ve kitle psikolojisine karşı koyma."}
        ]
    },
    "module_5": {
        "title": "🛡️ Risk Yönetimi",
        "description": "Sermaye koruma ve pozisyon yönetimi",
        "lessons": [
            {"id": "lesson_5_1", "title": "Pozisyon Büyüklüğü", "content": "Risk oranları ve sermaye yüzdesi."},
            {"id": "lesson_5_2", "title": "Zarar Durdurma", "content": "Stop-loss stratejileri ve uygulaması."},
            {"id": "lesson_5_3", "title": "Portföy Çeşitlendirmesi", "content": "Korelasyon ve risk dağıtımı."}
        ]
    }
}

user_progress = {}

def get_user_progress(user_id):
    if str(user_id) not in user_progress:
        user_progress[str(user_id)] = {
            'current_module': None,
            'completed_lessons': [],
            'quiz_scores': {},
            'total_score': 0
        }
    return user_progress[str(user_id)]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_user_progress(user.id)
    welcome_message = f"🎓 **Hoşgeldiniz {user.first_name}!**\n\n📚 **Efsanevi Yatırım Eğitim Botu**\n\nBaşlamak için menüyü kullanın!"
    keyboard = [
        [InlineKeyboardButton("📚 Eğitim Modülleri", callback_data='modules')],
        [InlineKeyboardButton("🧠 Quiz Sistemi", callback_data='quiz')],
        [InlineKeyboardButton("📊 Analiz Araçları", callback_data='tools')],
        [InlineKeyboardButton("ℹ️ Bilgi", callback_data='info')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_message, parse_mode='Markdown', reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "📖 **Yardım Menüsü**\n\n/start - Botu başlat\n/progress - İlerleme durumu"
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def modules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = []
    for module_id, module_data in EDUCATION_MODULES.items():
        keyboard.append([InlineKeyboardButton(module_data['title'], callback_data=f'module_{module_id}')])
    keyboard.append([InlineKeyboardButton("🔙 Ana Menü", callback_data='main_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("📚 **Eğitim Modülleri**", parse_mode='Markdown', reply_markup=reply_markup)

async def module_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    module_id = query.data.replace('module_', '')
    module_data = EDUCATION_MODULES.get(module_id)
    if not module_data: return
    user = update.effective_user
    progress = get_user_progress(user.id)
    keyboard = []
    for lesson in module_data['lessons']:
        completed = "✅" if lesson['id'] in progress['completed_lessons'] else "📖"
        keyboard.append([InlineKeyboardButton(f"{completed} {lesson['title']}", callback_data=f'lesson_{lesson["id"]}')])
    keyboard.append([InlineKeyboardButton("🔙 Modüller", callback_data='modules')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"📚 **{module_data['title']}**\n\n{module_data['description']}", parse_mode='Markdown', reply_markup=reply_markup)

async def lesson_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lesson_id = query.data.replace('lesson_', '')
    lesson_data = None
    for module_data in EDUCATION_MODULES.values():
        for lesson in module_data['lessons']:
            if lesson['id'] == lesson_id:
                lesson_data = lesson
                break
        if lesson_data: break
    if not lesson_data: return
    user = update.effective_user
    progress = get_user_progress(user.id)
    if lesson_id not in progress['completed_lessons']:
        progress['completed_lessons'].append(lesson_id)
        progress['total_score'] += 10
    keyboard = [[InlineKeyboardButton("📝 Quiz Çöz", callback_data=f'quiz_{lesson_id}')], [InlineKeyboardButton("🔙 Modüllere Dön", callback_data='modules')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"📖 **{lesson_data['title']}**\n\n{lesson_data['content']}", parse_mode='Markdown', reply_markup=reply_markup)

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    quiz_questions = [{"question": "Yatırımda en önemli kural?", "options": ["Şans", "Kayıpları kesmek", "Kaldıraç"], "correct": 1}]
    question = quiz_questions[0]
    keyboard = []
    for i, option in enumerate(question["options"]):
        keyboard.append([InlineKeyboardButton(option, callback_data=f'answer_{i}_{question["correct"]}')])
    keyboard.append([InlineKeyboardButton("🔙 Ana Menü", callback_data='main_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"🧠 **Quiz**\n\n{question['question']}", parse_mode='Markdown', reply_markup=reply_markup)

async def quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        data = query.data.split('_')
        user_answer, correct_answer = int(data[1]), int(data[2])
        user = update.effective_user
        progress = get_user_progress(user.id)
        if user_answer == correct_answer:
            progress['total_score'] += 20
            message = "✅ **Doğru!** +20 Puan"
        else:
            message = "❌ **Yanlış.**"
        keyboard = [[InlineKeyboardButton("🔙 Ana Menü", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)
    except:
        await query.edit_message_text("Hata oluştu.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data='main_menu')]]))

async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    progress = get_user_progress(user.id)
    msg = f"📊 **Puanın:** {progress['total_score']}"
    keyboard = [[InlineKeyboardButton("🔙 Ana Menü", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query: await update.callback_query.edit_message_text(msg, parse_mode='Markdown', reply_markup=reply_markup)
    else: await update.message.reply_text(msg, parse_mode='Markdown', reply_markup=reply_markup)

async def tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📊 **Analiz Araçları** yakında!", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Ana Menü", callback_data='main_menu')]]))

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("ℹ️ **Bot Hakkında**\nEğitim Botu v1.0", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Ana Menü", callback_data='main_menu')]]))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    if data == 'modules': await modules(update, context)
    elif data == 'quiz': await quiz(update, context)
    elif data == 'tools': await tools(update, context)
    elif data == 'info': await info(update, context)
    elif data == 'main_menu': await start(update, context)
    elif data.startswith('module_'): await module_detail(update, context)
    elif data.startswith('lesson_'): await lesson_detail(update, context)
    elif data.startswith('answer_'): await quiz_answer(update, context)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning('Error: %s', context.error)

async def main():
    """Start the bot."""
    keep_alive()
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("progress", progress))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, help_command))
    application.add_error_handler(error_handler)
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    logger.info("Bot started successfully!")
    
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
