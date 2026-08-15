import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# Inicializa o cliente conectado na API da Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/api/generate', methods=['POST'])
def generate_prompt():
    data = request.json
    user_idea = data.get("idea", "")
    
    if not user_idea:
        return jsonify({"error": "Nenhuma ideia fornecida"}), 400

    # Instrução cirúrgica para o modelo gigante de 120B
    system_prompt = (
        "You are an expert anime director. Translate the user prompt into a short, single-sentence Vidu AI video prompt in English.\n\n"
        "MANDATORY FORMAT:\n"
        "Your response must be a single continuous sentence of technical terms in lowercase, separated ONLY by commas. "
        "Do NOT write titles, do NOT use brackets [], do NOT use bullet points, do NOT give explanations.\n\n"
        "REQUIRED TEMPLATE STRUCTURE:\n"
        "[technical camera movements and framing], [character physical actions and sakuga animation physics], [safety restrictions]\n\n"
        "CRITICAL RULES:\n"
        "- Never repeat camera terms or actions.\n"
        "- Do not alucinate. Do not add dust, explosions, or background elements unless requested by the user.\n"
        "- The prompt MUST end exactly with this safety block: 'smooth motion, clean linear movement, no motion blur artifacts, quick but controlled, sound effects only, no music'"
    )

    try:
        # Acionando o modelo de 120B da sua lista da Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"User Anime Scene Idea: {user_idea}"}
            ],
            model="gpt-oss-120b",
            temperature=0.1,  # Travado no mínimo para ele seguir o padrão cegamente
        )
        
        result_prompt = chat_completion.choices[0].message.content.strip()
        
        # Limpeza bruta de segurança para remover qualquer colchete ou aspa teimosa
        result_prompt = result_prompt.replace("[", "").replace("]", "")
        if result_prompt.startswith('"') and result_prompt.endswith('"'):
            result_prompt = result_prompt[1:-1]
        if result_prompt.startswith("'") and result_prompt.endswith("'"):
            result_prompt = result_prompt[1:-1]
            
        return jsonify({"prompt": result_prompt.lower()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def handler(request):
    return app(request)
