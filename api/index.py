import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='../templates')

# API Yapılandırması
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Nano Banana (Görsel Nesli) ve Flash (Metin Nesli) için modeller
text_model = genai.GenerativeModel('gemini-2.5-flash')
# Not: API üzerinden görsel oluşturma yeteneği Imagen (imagen-3.0) modeliyle sağlanır
image_model = genai.GenerativeModel('imagen-3.0-generate-001') # Veya kullandığın bölgedeki en güncel sürüm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').lower()
        
        # Eğer kullanıcı "çiz" veya "oluştur" gibi bir komut verirse Nano Banana devreye girsin
        image_keywords = ["çiz", "oluştur", "generate", "create image", "resmini yap"]
        
        if any(word in user_message for word in image_keywords):
            # Görsel Oluşturma Mantığı
            response = image_model.generate_content(f"Create a high quality image of: {user_message}")
            # Gemini API doğrudan görsel URL'si veya base64 döner (API versiyonuna göre değişir)
            # Şimdilik simüle edilmiş bir başarılı dönüş yapalım veya API dokümanına göre URL'yi alalım
            return jsonify({
                'type': 'image',
                'response': 'İşte senin için oluşturduğum görsel:',
                'image_url': response.images[0].url if hasattr(response, 'images') else None
            })
        
        # Normal Metin Sohbeti
        prompt = f"Sen Turna AI'sın. Nano Banana gücüne sahipsin. Yanıtın: {user_message}"
        response = text_model.generate_content(prompt)
        return jsonify({'type': 'text', 'response': response.text})

    except Exception as e:
        return jsonify({'response': 'Hata: ' + str(e)}), 500
