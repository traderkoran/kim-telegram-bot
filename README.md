# Efsanevi Yatırım Eğitim Botu

## 🎯 Proje Açıklaması

Bu Telegram botu, PROMETHEUS AI'nın 7 katmanlı analiz modeli ve Piyasa Sihirbazlarının psikolojik prensiplerine dayalı kapsamlı bir yatırım eğitimi platformudur.

## 📚 Özellikler

### Eğitim Modülleri
- **Modül 1:** Temel Kavramlar (Piyasa Psikolojisi, Risk Yönetimi)
- **Modül 2:** Teknik Analiz (Mum Formasyonları, Grafik Formasyonları)
- **Modül 3:** İleri Teknikler (Fibonacci, Harmonik Formasyonlar)
- **Modül 4:** Ticaret Psikolojisi (Zihniyet, Duygu Yönetimi)
- **Modül 5:** Risk Yönetimi (Pozisyon Büyüklüğü, Stop-Loss)

### Etkileşimli Özellikler
- ✅ İlerleme takibi
- 🧠 Quiz sistemi
- 🏆 Puanlama sistemi
- 📊 Analiz araçları (yakında)
- 🎓 Sertifika sistemi

## 🚀 Kurulum

### Gereksinimler
- Python 3.7+
- Telegram Bot Token
- python-telegram-bot kütüphanesi

### Adım Adım Kurulum

1. **Bot Token Oluşturma**
   - @BotFather ile konuşun
   - `/newbot` komutunu kullanın
   - Token'ı kopyalayın

2. **Proje Dosyalarını İndirme**
   ```bash
   git clone https://github.com/yourusername/efsanevi-trading-bot.git
   cd efsanevi-trading-bot
   ```

3. **Bağımlılıkları Yükleme**
   ```bash
   pip install -r requirements.txt
   ```

4. **Çevre Değişkenlerini Ayarlama**
   ```bash
   export BOT_TOKEN="your_bot_token_here"
   export DEVELOPER_ID="your_telegram_user_id"
   ```

5. **Botu Çalıştırma**
   ```bash
   python trading_education_bot.py
   ```

## 🌐 Ücretsiz Hosting

### Render.com (Önerilen)
1. Render.com'da hesap oluşturun
2. GitHub reposunu bağlayın
3. Environment variables ayarlayın:
   - `BOT_TOKEN`: BotFather'dan aldığınız token
   - `DEVELOPER_ID`: Telegram kullanıcı ID'niz

### Alternatif Platformlar
- **Heroku**: Ücretsiz dyno ile hosting
- **PythonAnywhere**: Python projeleri için ideal
- **Replit**: Tarayıcı tabanlı geliştirme
- **Vercel**: Serverless functions

## 💻 Kullanım

### Komutlar
- `/start` - Botu başlat
- `/help` - Yardım bilgisi
- `/progress` - İlerleme durumu
- `/quiz` - Quiz başlat

### Etkileşimler
- 📚 Modül seçimi
- 📖 Ders okuma
- 🧠 Quiz çözme
- 📊 İlerleme takibi

## 📊 Teknik Detaylar

### Kütüphaneler
- `python-telegram-bot`: Telegram API entegrasyonu
- `requests`: HTTP istekleri

### Veri Yapısı
- Kullanıcı ilerlemesi (RAM'de saklanır)
- Modül ve ders içerikleri
- Quiz soruları ve cevapları

### Güvenlik
- Token gizleme (environment variables)
- Kullanıcı doğrulama
- Hata yönetimi

## 🔧 Geliştirme

### Yeni Modül Ekleme
```python
"module_6": {
    "title": "Yeni Modül Başlığı",
    "description": "Modül açıklaması",
    "lessons": [
        {"id": "lesson_6_1", "title": "Ders 1", "content": "İçerik"}
    ]
}
```

### Quiz Sorusu Ekleme
```python
{
    "question": "Soru metni",
    "options": ["Seçenek 1", "Seçenek 2", "Seçenek 3"],
    "correct": 0,
    "explanation": "Açıklama"
}
```

## 📱 Bot Özellikleri

### Kullanıcı Deneyimi
- 🎯 Sezgisel menü sistemi
- 📱 Mobil uyumlu
- 🎨 Emoji desteği
- ⚡ Hızlı yanıt

### Eğitim Kalitesi
- 📚 Yapılandırılmış içerik
- 🧠 Etkileşimli öğrenme
- 📊 İlerleme takibi
- 🏆 Motivasyon sistemi

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun
3. Değişikliklerinizi commit edin
4. Pull request gönderin

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.

## 📞 İletişim

- **Telegram:** @developer_username
- **Email:** developer@email.com
- **GitHub:** github.com/yourusername

---

**Efsanevi Yatırım Eğitim Botu** - Geleceğin yatırım uzmanlarını yetiştiriyor! 🚀