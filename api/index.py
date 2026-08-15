import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# Inicializa o cliente da Groq pegando a chave das variáveis de ambiente
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/api/generate', methods=['POST'])
def generate_prompt():
    data = request.json
    user_idea = data.get("idea", "")
    
    if not user_idea:
        return jsonify({"error": "Nenhuma ideia fornecida"}), 400

    # O "System Prompt" com as regras rígidas do Vidu AI que você definiu
    system_prompt = (
        "Você é um Diretor de Storyboard e Animação especialista em prompts para a IA de vídeo Vidu, "
        "focado no estilo anime (referências como MAPPA, Jujutsu Kaisen, Chainsaw Man). Seu objetivo é "
        "transformar a ideia simples do usuário em um prompt de vídeo curto, direto e ultra-otimizado em inglês.\n\n"
        "Diretrizes rígidas que você DEVE seguir:\n"
        "1. Estrutura do Prompt: Uma única frase curta contendo exatamente: [ação do personagem] + [comando técnico de câmera] + [física/efeitos] + [som ambientado, sem música].\n"
        "2. Comandos de Câmera: Use apenas UM comando dominante por vez para evitar artefatos (ex: dolly in/out, truck left/right, pan, tilt, orbit, crane, handheld, steadycam, rack focus, zoom).\n"
        "3. Física Controlada: Destaque no máximo 1 ou 2 elementos físicos (ex: hair flowing, cloth simulation, dust particles, smoke rising). Nunca misture muitos elementos para não distorcer.\n"
        "4. Prevenção de Distorção: Sempre inclua termos de controle para movimentos rápidos como: smooth motion, clean linear movement, no motion blur artifacts, quick but controlled.\n"
        "5. Áudio: Finalize obrigatoriamente com restrição de música, focando em efeitos (ex: [efeito de som], no background music ou sound effects only, no music).\n\n"
        "Formato da Saída:\n"
        "Retorne APENAS o prompt final em inglês dentro de aspas duplas, sem explicações adicionais, sem introduções e sem parágrafos."
    )

    try:
        # Faz a chamada para o modelo Llama da Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Ideia do usuário: {user_idea}"}
            ],
            model="llama3-8b-8192", # Ou o modelo que você já estava usando
            temperature=0.5,
        )
        
        result_prompt = chat_completion.choices[0].message.content.strip()
        return jsonify({"prompt": result_prompt})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Necessário para a Vercel serverless funcionar
def handler(request):
    return app(request)
