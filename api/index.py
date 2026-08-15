import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# Inicializa o cliente da Groq usando a sua chave de ambiente
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/api/generate', methods=['POST'])
def generate_prompt():
    data = request.json
    user_idea = data.get("idea", "")
    
    if not user_idea:
        return jsonify({"error": "Nenhuma ideia fornecida"}), 400

    # Instrução ultra-rígida para o modelo Llama 3.3 70B
    system_prompt = (
        "You are an expert anime storyboard director. Translate the user input into a professional Vidu AI video prompt in English.\n\n"
        "STRICT PROMPT FORMAT:\n"
        "You must output exactly one continuous sentence, lowercase, separated by commas following this sequence:\n"
        "1. [camera movement and framing from the options: tracking shot, dolly in, dolly out, pan left, pan right, tilt up, tilt down, orbit camera, push in, pull back, slight handheld camera shake, low angle shot, high angle shot, over-the-shoulder shot, close-up shot, wide shot]\n"
        "2. [character physical action, body weight, and sakuga anime physics, without adding unrequested objects or scene debris]\n"
        "3. [exactly this safety block: 'smooth motion, clean linear movement, no motion blur artifacts, quick but controlled, sound effects only, no music']\n\n"
        "CRITICAL RULES:\n"
        "- Never repeat camera terms or actions.\n"
        "- Do not alucinate. Do not add dust, explosions, or background elements unless explicitly requested by the user.\n"
        "- Output ONLY the raw prompt. No explanations, no quotes, no introductions, no chat filler."
    )

    try:
        # Chamada com o modelo robusto Llama 3.3 70B da sua lista
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"User Anime Scene: {user_idea}"}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1,  # Temperatura quase zero para garantir obediência cega ao formato
        )
        
        result_prompt = chat_completion.choices[0].message.content.strip()
        
        # Remove aspas externas caso o modelo insista em colocar
        if result_prompt.startswith('"') and result_prompt.endswith('"'):
            result_prompt = result_prompt[1:-1]
        if result_prompt.startswith("'") and result_prompt.endswith("'"):
            result_prompt = result_prompt[1:-1]
            
        return jsonify({"prompt": result_prompt.lower()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Handler obrigatório para a arquitetura serverless da Vercel
def handler(request):
    return app(request)
