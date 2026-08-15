import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# Conecta na API da Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/api/generate', methods=['POST'])
def generate_prompt():
    data = request.json
    user_idea = data.get("idea", "")
    
    if not user_idea:
        return jsonify({"error": "Nenhuma ideia fornecida"}), 400

    # System prompt direto e rígido
    system_prompt = (
        "You are an expert anime director. Translate the user prompt into a short, single-sentence Vidu AI video prompt in English.\n\n"
        "MANDATORY FORMAT:\n"
        "[Technical camera movement and framing: tracking shot, dolly in/out, pan, tilt, orbit, close-up, or wide shot], "
        "[Character physical actions, weight, and sakuga animation physics], "
        "[Safety restrictions: smooth motion, clean linear movement, no motion blur artifacts, quick but controlled, sound effects only, no music.]\n\n"
        "CRITICAL RULES:\n"
        "- Do NOT repeat camera terms.\n"
        "- Do NOT add details, environment objects, dust or explosions unless requested.\n"
        "- Output ONLY the raw prompt. No explanations, no quotes, no conversational text."
    )

    try:
        # Chamando o ID estável conforme consta no seu painel da Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"User Anime Scene: {user_idea}"}
            ],
            model="llama-3.3-70b",
            temperature=0.1,  # Trava o modelo para obedecer friamente
        )
        
        result_prompt = chat_completion.choices[0].message.content.strip()
        
        # Remove aspas se sobrarem
        if result_prompt.startswith('"') and result_prompt.endswith('"'):
            result_prompt = result_prompt[1:-1]
            
        return jsonify({"prompt": result_prompt.lower()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def handler(request):
    return app(request)
