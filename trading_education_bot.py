#!/usr/bin/env python3
"""
Efsanevi Yatırım Eğitim Botu
Legendary Investment Education Bot

Bu bot, PROMETHEUS AI ve Piyasa Sihirbazları konseptlerine dayalı
kapsamlı bir yatırım eğitimi platformudur.
"""

import logging
import os
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# --- RENDER İÇİN GEREKLİ EKLEMELER ---
from flask import Flask
from threading import Thread
# -------------------------------------

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
DEVELOPER_ID = os.environ.get('DEVELOPER_ID', 'YOUR_DEVELOPER_ID')

# --- RENDER KEEP-ALIVE WEB SUNUCUSU ---
# Bu bölüm Render'ın botu kapatmaması için sahte bir web sunucusu çalıştırır.
app = Flask('')

@app.route('/')
def home():
    return "Bot aktif! Efsanevi Yatırım Botu çalışıyor."

def run():
    # Render'ın atadığı PORT'u kullan, yoksa 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ---------------------------------------

# Education content structure
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

# User progress tracking
user_progress = {}

def get_user_progress(user_id):
    """Get user progress from memory or initialize"""
    if str(user_id) not in user_progress:
        user_progress[str(user_id)] = {
            'current_module': None,
            'completed_lessons': [],
            'quiz_scores': {},
            'total_score': 0
        }
    return user_progress[str(user_id)]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    get_user_progress(user.id) # Initialize user
    
    welcome_message = f"""
🎓 **Hoşgeldiniz {user.first_name}!**

📚 **Efsanevi Yatırım Eğitim Botu**

Bu bot, PROMETHEUS AI'nın 7 katmanlı analiz modeli ve Piyasa Sihirbazlarının psikolojik prensiplerine dayalı kapsamlı bir yatırım eğitimi platformudur.

**🎯 Özellikler:**
• Yapılandırılmış eğitim modülleri
• Etkileşimli quizler ve testler  
• İlerleme takibi ve sertifikalar
• Uygulamalı analiz araçları

**Başlamak için aşağıdaki menüyü kullanın!**
    """
    
    keyboard = [
        [InlineKeyboardButton("📚 Eğitim Modülleri", callback_data='modules')],
        [InlineKeyboardButton("🧠 Quiz Sistemi", callback_data='quiz')],
        [InlineKeyboardButton("📊 Analiz Araçları", callback_data='tools')],
        [InlineKeyboardButton("ℹ️ Bilgi", callback_data='info')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, parse_mode='Markdown', reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """
📖 **Yardım Menüsü**

**Komutlar:**
• /start - Botu başlat
• /help - Yardım bilgisi
• /progress - İlerleme durumu
• /quiz - Quiz başlat

**Özellikler:**
• 5 eğitim modülü
• 15+ interaktif ders
• Quiz sistemi
• İlerleme takibi

**İletişim:** @developer_username
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def modules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display education modules"""
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    for module_id, module_data in EDUCATION_MODULES.items():
        keyboard.append([InlineKeyboardButton(
            f"{module_data['title']}", 
            callback_data=f'module_{module_id}'
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Ana Menü", callback_data='main_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """
📚 **Eğitim Modülleri**

Aşağıdaki modülleri tamamlayarak yatırım uzmanlığınızı geliştirebilirsiniz:
    """
    
    await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)

async def module_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display module details and lessons"""
    query = update.callback_query
    await query.answer()
    
    module_id = query.data.replace('module_', '')
    module_data = EDUCATION_MODULES.get(module_id)
    
    if not module_data:
        return
    
    user = update.effective_user
    progress = get_user_progress(user.id)
    
    keyboard = []
    for lesson in module_data['lessons']:
        completed = "✅" if lesson['id'] in progress['completed_lessons'] else "📖"
        keyboard.append([InlineKeyboardButton(
            f"{completed} {lesson['title']}", 
            callback_data=f'lesson_{lesson["id"]}'
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Modüller", callback_data='modules')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = f"""
📚 **{module_data['title']}**

{module_data['description']}

**Dersler:**
    """
    
    await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)

async def lesson_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display lesson content"""
    query = update.callback_query
    await query.answer()
    
    lesson_id = query.data.replace('lesson_', '')
    
    # Find lesson data
    lesson_data = None
    for module_data in EDUCATION_MODULES.values():
        for lesson in module_data['lessons']:
            if lesson['id'] == lesson_id:
                lesson_data = lesson
                break
        if lesson_data:
            break
    
    if not lesson_data:
        return
    
    user = update.effective_user
    progress = get_user_progress(user.id)
    
    # Mark lesson as completed
    if lesson_id not in progress['completed_lessons']:
        progress['completed_lessons'].append(lesson_id)
        progress['total_score'] += 10
    
    keyboard = [
        [InlineKeyboardButton("📝 Quiz Çöz", callback_data=f'quiz_{lesson_id}')],
        [InlineKeyboardButton("🔙 Derslere Dön", callback_data=f'module_{lesson_id.split("_")[0]}_{lesson_id.split("_")[1]}')] # Go back to specific module
    ]
    # Basit hata önleme: Modül ID'sini dersten çıkarmak zor olabilir, güvenli dönüş:
    keyboard = [
        [InlineKeyboardButton("📝 Quiz Çöz", callback_data=f'quiz_{lesson_id}')],
        [InlineKeyboardButton("🔙 Modüllere Dön", callback_data='modules')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = f"""
📖 **{lesson_data['title']}**

{lesson_data['content']}

**Tebrikler!** 🎉
Bu dersi tamamladınız ve 10 puan kazandınız!
    """
    
    await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start quiz for a lesson"""
    query = update.callback_query
    await query.answer()
    
    # Sample quiz questions
    quiz_questions = [
        {
            "question": "Yatırımda en önemli üç kural nedir?",
            "options": ["Analiz, zamanlama, şans", "Kayıpları kes, kes, kes", "Kaldıraç, sabır, disiplin"],
            "correct": 1,
            "explanation": "Piyasa Sihirbazları'na göre en önemli kural kayıpları kısa tutmaktır."
        },
        {
            "question": "RSI göstergesi 70 seviyesinin üzerinde olduğunda ne anlama gelir?",
            "options": ["Aşırı satım", "Aşırı alım", "Nötr piyasa"],
            "correct": 1,
            "explanation": "RSI 70 üzeri aşırı alım bölgesi olarak kabul edilir."
        },
        {
            "question": "Omuz Baş Omuz formasyonu hangi tür bir sinyaldir?",
            "options": ["Devam formasyonu", "Dönüş formasyonu", "Konsolidasyon"],
            "correct": 1,
            "explanation": "OBO formasyonu %93 başarı oranıyla güçlü bir dönüş sinyalidir."
        }
    ]
    
    # Rastgele bir soru seçebiliriz ama şimdilik ilki
    import random
    question = random.choice(quiz_questions)
    
    keyboard = []
    for i, option in enumerate(question["options"]):
        keyboard.append([InlineKeyboardButton(option, callback_data=f'answer_{i}_{question["correct"]}')])
    
    keyboard.append([InlineKeyboardButton("🔙 Ana Menü", callback_data='main_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = f"""
🧠 **Quiz Zamanı!**

{question['question']}

Doğru cevabı seçin:
    """
    
    await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)

async def quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quiz answer"""
    query = update.callback_query
    await query.answer()
    
    try:
        data = query.data.split('_')
        user_answer = int(data[1])
        correct_answer = int(data[2])
        
        user = update.effective_user
        progress = get_user_progress(user.id)
        
        if user_answer == correct_answer:
            progress['total_score'] += 20
            message = "✅ **Doğru Cevap!** 🎉\n\nTebrikler! 20 puan kazandınız!"
        else:
            message = "❌ **Yanlış Cevap**\n\nBir sonraki soruda daha şanslı olacaksınız!"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Yeni Soru", callback_data='quiz')],
            [InlineKeyboardButton("🔙 Ana Menü", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Quiz error: {e}")
        await query.edit_message_text("Bir hata oluştu, lütfen tekrar deneyin.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Ana Menü", callback_data='main_menu')]]))

async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user progress"""
    user = update.effective_user
    progress = get_user_progress(user.id)
    
    completed_lessons = len(progress['completed_lessons'])
    total_lessons = sum(len(module['lessons']) for module in EDUCATION_MODULES.values())
    
    # Sıfıra bölünme hatasını önle
    if total_lessons > 0:
        completion_rate = (completed_lessons / total_lessons) * 100
    else:
        completion_rate = 0
    
    message = f"""
📊 **İlerleme Durumunuz**

✅ **Tamamlanan Dersler:** {completed_lessons}/{total_lessons}
📈 **Tamamlanma Oranı:** %{completion_rate:.1f}
🏆 **Toplam Puan:** {progress['total_score']}

**Sertifika Durumu:**
{"🎓 Sertifika Kazanıldı!" if completion_rate >= 80 else f"Sertifika için %{80-completion_rate:.0f} daha tamamlamalısınız"}
    """
    
    keyboard = [[InlineKeyboardButton("🔙 Ana Menü", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)
    else:
        await update.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)

async def tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display analysis tools"""
    query = update.callback_query
    await query.answer()
    
    message = """
📊 **Analiz Araçları**

**Geliştirilmekte olan özellikler:**

🔍 **Piyasa Scannerı**
- Gerçek zamanlı formasyon tespiti
- RSI ve MACD sinyalleri
- Hacim analizi

📈 **Risk Hesaplayıcı**
- Pozisyon büyüklüğü hesaplama
- Stop-loss seviyeleri
- Risk/ödül oranları

🎯 **Sinyal Üretici**
- Çoklu zaman dilimi analizi
- Harmonik formasyon tespiti
- Ticaret planı oluşturucu

**Yakında aktif olacak!**
    """
    
    keyboard = [[InlineKeyboardButton("🔙 Ana Menü", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display bot information"""
    query = update.callback_query
    await query.answer()
    
    message = """
ℹ️ **Bot Hakkında**

**🎯 Amaç:**
PROMETHEUS AI ve Piyasa Sihirbazları konseptlerine dayalı,
kapsamlı yatırım eğitimi platformu.

**📚 İçerik:**
• 5 Eğitim Modülü
• 15+ İnteraktif Ders
• Quiz Sistemi
• İlerleme Takibi

**🔧 Teknik Özellikler:**
- Python Telegram Bot API
- Gerçek zamanlı etkileşim
- Kullanıcı ilerleme takibi
- Ücretsiz hosting

**📞 İletişim:** @developer_username
    """
    
    keyboard = [[InlineKeyboardButton("🔙 Ana Menü", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all callback queries"""
    query = update.callback_query
    data = query.data
    
    if data == 'modules':
        await modules(update, context)
    elif data == 'quiz':
        await quiz(update, context)
    elif data == 'tools':
        await tools(update, context)
    elif data == 'info':
        await info(update, context)
    elif data == 'main_menu':
        await start(update, context)
    elif data.startswith('module_'):
        await module_detail(update, context)
    elif data.startswith('lesson_'):
        await lesson_detail(update, context)
    elif data.startswith('answer_'):
        await quiz_answer(update, context)
    else:
        await query.answer("Bu özellik yakında aktif olacak!")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


    async def main():
        """Start the bot."""
    
    # --- BU KISIM ÇOK ÖNEMLİ: RENDER'IN BOTU KAPATMAMASI İÇİN ---
        keep_alive()
    # ------------------------------------------------------------
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("progress", progress))

    # on callback queries
    application.add_handler(CallbackQueryHandler(button_handler))

    # on non command i.e message
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, help_command))

    # log all errors
    application.add_error_handler(error_handler)

    # Start the Bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    logger.info("Bot started successfully!")
    
    # Run the bot until you press Ctrl-C
    await application.updater.idle()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
