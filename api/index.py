import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image
import io

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Gemini API Yapılandırması
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Nano Banana (Metin ve Görsel Analiz) için Flash modelini kullanıyoruz
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # HATA DÜZELTME: FormData'dan verileri al (JSON değil)
        user_message = request.form.get('message', '').lower()
        image_file = request.files.get('image')

        system_instruction = "Sen Turna AI'sın. Nano Banana Edition modelisin. Nazik, hızlı ve bir muz kadar tatlısın. Yanıtların Türkçe, kısa ve net olsun."
        prompt_parts = [system_instruction]

        # Görsel varsa, onu Gemini'ye uygun formata dönüştür
        if image_file:
            # Dosyayı hafızada (RAM) aç (diske kaydetmeden)
            img = Image.open(image_file.stream)
            prompt_parts.append(img)
            system_instruction += " Bu fotoğrafı analiz et ve yorumla."
            prompt_parts[0] = system_instruction # Sistem mesajını güncelle

        if user_message:
            prompt_parts.append(f"Soru: {user_message}")

        # Eğer kullanıcı "çiz" derse, görsel oluşturma simülasyonu yapalım 
        # (Gemini API üzerinden görsel oluşturmaImagen gerektirir, şimdilik metinle yanıtlayalım)
        image_keywords = ["çiz", "oluştur", "generate", "create image", "resmini yap"]
        if any(word in user_message for word in image_keywords) and not image_file:
            return jsonify({
                'response': f"Harika bir fikir! 'imagen' API'si açık olsaydı senin için harika bir {user_message.replace('çiz','')} çizerdim. Şimdilik bu özelliği aktif etmedim, sadece metin ve görsel analiz yapıyorum. 🍌"
            })

        # Gemini'den yanıt oluştur
        response = model.generate_content(prompt_parts)
        return jsonify({'response': response.text})

    except Exception as e:
        return jsonify({'response': f'Bir hata oluştu: {str(e)}'}), 500

# Vercel için gerekli
app.debug = False
