import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/api/generate', methods=['POST'])
def generate_prompt():
    data = request.json
    user_idea = data.get("idea", "")
    
    if not user_idea:
        return jsonify({"error": "Nenhuma ideia fornecida"}), 400

    # System prompt cirúrgico focado em separar Câmera de Personagem com termos técnicos Sakuga
    system_prompt = (
        "You are an elite Sakuga Anime Director and expert prompt engineer for Vidu AI video generation.\n"
        "Your task is to convert the user's scene description into a highly precise, technical prompt in English.\n\n"
        "STRICT PROMPT ARCHITECTURE (Output must follow this exact sequence in a single continuous technical prompt):\n"
        "1. CAMERA MOVEMENT & ANGLE: Start immediately with professional cinematography terms. Use exclusively: tracking shot, dolly in/out, pan left/right, tilt up/down, orbit, push in, pull back, handheld, low angle, high angle, over-the-shoulder, close-up, wide shot.\n"
        "2. CHARACTER ACTION & PHYSICS: Clearly separate character movement from camera movement. Describe physical actions, weight, and targeted physics (e.g., hair flowing, cloth simulation, heavy footsteps) without adding unrequested elements.\n"
        "3. RITMO & SAKUGA STYLE: Focus on dynamic flow, high-speed execution, or fluid motion (e.g., sakuga animation, high-speed execution, fluid animation weight).\n"
        "4. LIGHTING & ATMOSPHERE: Extract from user input or lock professional studio lighting (e.g., dramatic backlighting, high contrast, cinematic atmosphere).\n"
        "5. VISUAL EFFECTS: Impact frames, crisp linework, zero motion blur distortion.\n"
        "6. CHARACTER CONSISTENCY & RESTRICTIONS: Always end the prompt exactly with this technical safety block: 'smooth motion, clean linear movement, no motion blur artifacts, quick but controlled, sound effects only, no music.'\n\n"
        "CRITICAL CONSTRAINT:\n"
        "Output ONLY the final raw prompt in English. No introductions, no explanations, no chat, no quotes, no conversational filler. Just the direct prompt ready to copy."
    )

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"User Anime Scene Idea: {user_idea}"}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.15, # Temperatura baixa para travar alucinações e focar nas regras
        )
        
        result_prompt = chat_completion.choices[0].message.content.strip()
        return jsonify({"prompt": result_prompt})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def handler(request):
    return app(request)
