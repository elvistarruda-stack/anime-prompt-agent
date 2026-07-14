from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

@app.route("/api/generate", methods=["POST"])
def generate_prompt():
    if not client:
        return jsonify({"error": "Chave GROQ_API_KEY nao configurada na Vercel."}), 500

    try:
        data = request.get_json(silent=True) or {}
        user_idea = data.get("idea", "").strip()
        
        if not user_idea:
            return jsonify({"error": "Por favor, digite uma ideia antes!"}), 400
            
        system_instruction = (
            "You are the Anime Prompt Inspector. Your job is to expand the user's basic anime idea "
            "into a highly detailed, professional prompt optimized for AI image generators like Midjourney or Stable Diffusion. "
            "Output ONLY the final detailed prompt in English. Do not include any introduction, conversational filler, or side comments."
        )
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Expand this concept into a stunning anime art prompt: {user_idea}"}
            ]
        )
        
        generated_text = completion.choices.message.content
        return jsonify({"prompt": generated_text}), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro na API da Groq: {str(e)}"}), 500

