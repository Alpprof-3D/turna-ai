import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Gemini API Yapılandırması
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        # Turna AI Kişiliği
        prompt = f"Senin adın Turna AI. 2018 model, nazik ve hızlı bir yapay zekasın. Yanıtın kısa ve öz olsun. Soru: {user_message}"
        
        response = model.generate_content(prompt)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': 'Bir hata oluştu: ' + str(e)}), 500