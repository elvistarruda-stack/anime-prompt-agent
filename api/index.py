from flask import Flask, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# Puxa a chave que salvamos com segurança na Vercel
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/api/generate", methods=["POST"])
def generate_prompt():
    data = request.json
    user_idea = data.get("idea", "")
    
    if not user_idea:
        return jsonify({"error": "Nenhuma ideia enviada"}), 400
        
    try:
        system_instruction = (
            "Você é o Anime Prompt Inspector. Sua tarefa é transformar uma ideia simples de anime "
            "em um prompt altamente detalhado, profissional e otimizado para geradores de imagens (como Midjourney ou Stable Diffusion). "
            "Retorne APENAS o prompt final otimizado em inglês, sem introduções ou explicações adicionais."
        )
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-specdec",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Transforme essa ideia em um prompt de arte de anime incrível: {user_idea}"}
            ]
        )
        
        generated_text = completion.choices.message.content
        return jsonify({"prompt": generated_text})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
