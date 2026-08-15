import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# Inicializa o cliente da Groq com a chave de ambiente
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/api/generate', methods=['POST'])
def generate_prompt():
    data = request.json
    user_idea = data.get("idea", "")
    image_mode = data.get("imageMode", "1-img")
    camera_selected = data.get("camera", "")
    pace = data.get("pace", "4s-fast")
    
    if not user_idea:
        return jsonify({"error": "Nenhuma ideia fornecida"}), 400

    # Ajusta o comportamento com base nas escolhas dos botões do usuário
    anchoring_instruction = ""
    if image_mode == "2-img":
        anchoring_instruction = (
            "- ATENÇÃO: O usuário vai usar DUAS imagens de referência (Início e Fim). "
            "Portanto, NUNCA descreva transições de enquadramento ou o movimento da câmera no texto "
            "(evite termos como 'from close-up to full body' ou 'camera pulling back'). "
            "Deixe que as imagens guiem o enquadramento. Foque 100% da força do prompt em termos de impacto "
            "físico e intensidade das ações dentro da cena fixada (ex: 'taking heavy footsteps forward', 'blowing violently')."
        )
    else:
        anchoring_instruction = (
            "- O usuário vai usar APENAS UMA imagem de referência. "
            "Você pode incluir comandos contínuos de câmera se o usuário não tiver selecionado um botão específico."
        )

    pace_instruction = ""
    if pace == "4s-fast":
        pace_instruction = "- Ritmo: Foco em animação estilo Sakuga de ação rápida. Use termos como 'burst of speed', 'sharp impact effects', 'fast and energetic motion'."
    else:
        pace_instruction = "- Ritmo: Foco em fluidez contínua e cadenciada. Use termos como 'smooth elegant motion', 'continuous flow', 'graceful physics simulation'."

    # O "System Prompt" ultra-especializado para o Vidu
    system_prompt = (
        "Você é um Diretor de Storyboard e Animação especialista em prompts para a IA de vídeo Vidu, "
        "focado no estilo anime profissional (referências como MAPPA, Jujutsu Kaisen, Chainsaw Man). "
        "Seu objetivo é transformar a ideia simples e as configurações do usuário em um prompt técnico em inglês curto e limpo.\n\n"
        "Diretrizes obrigatórias que você DEVE seguir:\n"
        "1. Estrutura do Prompt: Uma única frase contendo exatamente: [ação do personagem] + [efeitos físicos e partículas] + [controle de artefatos] + [som ambientado, sem música].\n"
        "2. Câmera: Se o usuário selecionou uma câmera específica, incorpore-a de forma natural. Nunca acumule mais de um movimento complexo.\n"
        f"{anchoring_instruction}\n"
        f"{pace_instruction}\n"
        "3. Prevenção de Distorção: Sempre encerre o corpo do prompt com travas de consistência: 'smooth motion, clean linear movement, no motion blur artifacts, quick but controlled'.\n"
        "4. Áudio: Finalize obrigatoriamente restringindo músicas, focando em efeitos (ex: '[efeito de som], no background music' ou 'sound effects only, no music').\n\n"
        "Formato da Saída:\n"
        "Retorne APENAS o prompt final em inglês, sem aspas externas, sem explicações adicionais, sem introduções e sem parágrafos."
    )

    # Constrói a mensagem final misturando os botões apertados com o texto livre
    user_content = f"Ideia livre: {user_idea} | Câmera travada pelo botão: {camera_selected} | Modo de Ritmo: {pace}"

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.4,
        )
        
        result_prompt = chat_completion.choices[0].message.content.strip()
        return jsonify({"prompt": result_prompt})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Necessário para a Vercel serverless
def handler(request):
    return app(request)
