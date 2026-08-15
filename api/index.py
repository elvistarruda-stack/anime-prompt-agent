<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Anime Prompt Inspector (VIDU - Sakuga Edition)</title>
    <link href="https://googleapis.com" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body { background-color: #090d16; color: #f8fafc; padding: 40px 20px; display: flex; justify-content: center; }
        .container { background-color: #111827; border-radius: 16px; padding: 32px; width: 100%; max-width: 700px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5); border: 1px solid #1f2937; }
        h1 { color: #38bdf8; font-size: 26px; font-weight: 700; text-align: center; margin-bottom: 4px; }
        .subtitle { font-size: 14px; color: #94a3b8; text-align: center; margin-bottom: 32px; }
        
        .section-title { font-size: 12px; font-weight: 700; text-transform: uppercase; color: #38bdf8; margin-bottom: 10px; letter-spacing: 0.5px; display: flex; justify-content: space-between;}
        .section-title span { color: #64748b; font-weight: 400; text-transform: none; }
        .group { margin-bottom: 24px; }
        
        /* Grid de Botões/Badges */
        .grid-options { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; margin-bottom: 12px; }
        .option-btn { background-color: #1f2937; border: 1px solid #374151; color: #94a3b8; padding: 10px; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; text-align: center; transition: all 0.2s; }
        .option-btn:hover { border-color: #38bdf8; color: #f8fafc; }
        .option-btn.active { background-color: #38bdf8; border-color: #38bdf8; color: #090d16; }

        textarea { width: 100%; height: 90px; background-color: #090d16; border: 1px solid #374151; border-radius: 8px; color: #f8fafc; padding: 14px; font-size: 14px; resize: none; outline: none; transition: border 0.2s; }
        textarea:focus { border-color: #38bdf8; }
        
        .action-btn { width: 100%; background-color: #38bdf8; color: #090d16; border: none; border-radius: 8px; padding: 16px; font-size: 16px; font-weight: 700; cursor: pointer; transition: background-color 0.2s; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 10px; }
        .action-btn:hover { background-color: #0ea5e9; }
        .action-btn:disabled { background-color: #374151; color: #64748b; cursor: not-allowed; }
        
        /* Caixa de Resultado Avançada */
        .result-box { display: none; margin-top: 28px; background-color: #090d16; border: 1px solid #38bdf8; border-radius: 8px; padding: 20px; position: relative; }
        .result-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
        .result-title { font-size: 12px; color: #38bdf8; font-weight: 700; text-transform: uppercase; }
        .copy-btn { background-color: #1f2937; border: 1px solid #374151; color: #38bdf8; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer; transition: all 0.2s; }
        .copy-btn:hover { background-color: #38bdf8; color: #090d16; border-color: #38bdf8; }
        .result-text { font-size: 14px; color: #f8fafc; line-height: 1.6; white-space: pre-wrap; font-family: 'JetBrains Mono', monospace; background: #111827; padding: 12px; border-radius: 6px; border: 1px solid #1f2937; }
        .suggestion-tag { display: inline-block; margin-top: 10px; font-size: 12px; color: #fbbf24; background-color: rgba(251, 191, 36, 0.1); padding: 4px 8px; border-radius: 4px; font-weight: 600; }
        .error { border-color: #ef4444; color: #fca5a5; }
    </style>
</head>
<body>

<div class="container">
    <h1>Anime Prompt Inspector 🔍</h1>
    <div class="subtitle">Direção Sakuga de Câmera & Física Avançada para Vidu AI</div>
    
    <!-- Modo de Referência -->
    <div class="group">
        <div class="section-title">Ancoragem Visual <span>(Como você enviará os arquivos no Vidu)</span></div>
        <div class="grid-options" id="imageModeGroup">
            <button class="option-btn active" onclick="selectOption('imageMode', '1-img', this)">1 Imagem de Referência</button>
            <button class="option-btn" onclick="selectOption('imageMode', '2-img', this)">2 Imagens (Início/Fim)</button>
        </div>
    </div>

    <!-- Movimento de Câmera Dominante -->
    <div class="group">
        <div class="section-title">Movimento de Câmera Dominante <span>(Selecione apenas 1 para evitar artefatos)</span></div>
        <div class="grid-options" id="cameraGroup">
            <button class="option-btn" onclick="selectOption('camera', 'tracking shot', this)">tracking shot</button>
            <button class="option-btn" onclick="selectOption('camera', 'dolly in', this)">dolly in</button>
            <button class="option-btn" onclick="selectOption('camera', 'dolly out', this)">dolly out</button>
            <button class="option-btn" onclick="selectOption('camera', 'pan left', this)">pan left</button>
            <button class="option-btn" onclick="selectOption('camera', 'pan right', this)">pan right</button>
            <button class="option-btn" onclick="selectOption('camera', 'tilt up', this)">tilt up</button>
            <button class="option-btn" onclick="selectOption('camera', 'tilt down', this)">tilt down</button>
            <button class="option-btn" onclick="selectOption('camera', 'orbit camera', this)">orbit</button>
            <button class="option-btn" onclick="selectOption('camera', 'push in', this)">push in</button>
            <button class="option-btn" onclick="selectOption('camera', 'pull back', this)">pull back</button>
            <button class="option-btn" onclick="selectOption('camera', 'slight handheld camera shake', this)">handheld (leve)</button>
            <button class="option-btn" onclick="selectOption('camera', 'low angle shot', this)">low angle</button>
            <button class="option-btn" onclick="selectOption('camera', 'high angle shot', this)">high angle</button>
            <button class="option-btn" onclick="selectOption('camera', 'over-the-shoulder shot', this)">over-the-shoulder</button>
            <button class="option-btn" onclick="selectOption('camera', 'close-up shot', this)">close-up</button>
            <button class="option-btn" onclick="selectOption('camera', 'wide shot', this)">wide shot</button>
        </div>
    </div>

    <!-- Ritmo da Animação -->
    <div class="group">
        <div class="section-title">Ritmo & Tempo da Animação <span>(Controla a velocidade do motor de física)</span></div>
        <div class="grid-options" id="paceGroup">
            <button class="option-btn active" onclick="selectOption('pace', '4s-fast', this)">4s - Ação Rápida / Impacto</button>
            <button class="option-btn" onclick="selectOption('pace', '8s-slow', this)">8s - Fluidez Contínua / Lenta</button>
        </div>
    </div>

    <!-- Ação Geral e Descrição -->
    <div class="group">
        <div class="section-title">Ação do Personagem & Física <span>(Descreva o que acontece em Português)</span></div>
        <textarea id="ideaInput" placeholder="Ex: Guerreiro de anime golpeando com espada, cabelo balançando violentamente com faíscas elétricas ao redor..."></textarea>
    </div>

    <button id="generateBtn" class="action-btn" onclick="generatePrompt()">Gerar Prompt Otimizado</button>

    <!-- Resultados -->
    <div id="resultContainer" class="result-box">
        <div class="result-header">
            <div class="result-title">Prompt Final Sakuga (Pronto para o Vidu)</div>
            <button class="copy-btn" onclick="copyPrompt()">Copiar</button>
        </div>
        <div id="resultText" class="result-text"></div>
        <div id="suggestionText" class="suggestion-tag"></div>
    </div>
</div>

<script>
    // Estado das escolhas do usuário
    const selections = {
        imageMode: '1-img',
        camera: '',
        pace: '4s-fast'
    };

    function selectOption(category, value, element) {
        // Remove classe ativa dos irmãos
        const siblings = element.parentNode.querySelectorAll('.option-btn');
        siblings.forEach(btn => btn.classList.remove('active'));
        
        // Se clicar no mesmo botão de câmera que já está ativo, ele desmarca (opcional)
        if (category === 'camera' && selections.camera === value) {
            selections.camera = '';
        } else {
            element.classList.add('active');
            selections[category] = value;
        }
    }

    async function generatePrompt() {
        const input = document.getElementById('ideaInput');
        const button = document.getElementById('generateBtn');
        const resultContainer = document.getElementById('resultContainer');
        const resultText = document.getElementById('resultText');
        const suggestionText = document.getElementById('suggestionText');
        
        if (!input.value.trim()) return;

        button.disabled = true;
        button.innerText = 'Orquestrando Coreografia Sakuga...';
        resultContainer.style.display = 'none';

        // Montando o contexto estruturado para enviar à API da Groq
        const fullPayload = {
            idea: input.value,
            imageMode: selections.imageMode,
            camera: selections.camera,
            pace: selections.pace
        };

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(fullPayload)
            });

            const data = await response.json();

            if (response.ok) {
                resultText.innerText = data.prompt;
                
