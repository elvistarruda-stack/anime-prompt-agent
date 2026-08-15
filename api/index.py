import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Conecta diretamente na API oficial da OpenAI (ChatGPT)
# Certifique-se de colocar sua chave na Vercel com o nome OPENAI_API_KEY
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/api/generate', methods=['POST'])
def generate_prompt():
    data = request.json
    user_idea = data.get("idea", "")
    
    if not user_idea:
        return jsonify({"error": "Nenhuma ideia fornecida"}), 400

    # Instrução cirúrgica e sem brechas que força a estrutura Sakuga que você desenhou
    system_prompt = (
        "You are an elite Sakuga Anime Director and professional prompt engineer for Vidu AI.\n"
        "Your sole task is to transform the user's raw scene description into a clean, technical video prompt in English.\n\n"
        "STRICT STRUCTURE REQUIREMENT:\n"
        "The output must be exactly one single continuous line of lowercase text, separated only by commas, following this exact sequence:\n"
        "1. [CAMERA MOVEMENT & FRAMING]: Use technical terms requested or implied (e.g., tracking shot, dolly in/out, pan, tilt, orbit, push in, pull back, handheld, low/high angle, over-the-shoulder, close-up, wide shot).\n"
        "2. [CHARACTER ACTIONS & PHYSICS]: Describe clear physical movement and weight (e.g., character walking forward, hair simulation flowing, clothes waving).\n"
        "3. [SAKUGA STYLE & PACE]: Dynamic fluid animation weight and speed.\n"
        "4. [LIGHTING & ATMOSPHERE]: Cinematic lighting according to the scene.\n"
        "5. [SAFETY TRAWLS]: End the line exactly with these words: 'smooth motion, clean linear movement, no motion blur artifacts, quick but controlled, sound effects only, no music'\n\n"
        "CRITICAL FORBIDDEN ACTIONS:\n"
        "- NEVER use brackets [] or category titles in the final output.\n"
        "- NEVER repeat camera terms or actions.\n"
        "- NEVER hallucinate debris, explosions, dust, or background items unless explicitly requested by the user.\n"
        "- Output ONLY the direct English prompt. No chat, no intros, no quotes, no explanations."
    )

    try:
        # Chamada oficial da API do ChatGPT
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"User Idea: {user_idea}"}
            ],
            model="gpt-4o-mini",
            temperature=0.1  # Temperatura baixa para travar qualquer comportamento criativo
        )
        
        result_prompt = response.choices[0].message.content.strip()
        
        # Limpeza bruta redundante para garantir que nenhum colchete passe para a tela
        result_prompt = result_prompt.replace("[", "").replace("]", "")
        if result_prompt.startswith('"') and result_prompt.endswith('"'):
            result_prompt = result_prompt[1:-1]
            
        return jsonify({"prompt": result_prompt.lower()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def handler(request):
    return app(request)
