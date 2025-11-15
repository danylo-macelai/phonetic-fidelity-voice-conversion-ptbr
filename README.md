<div align="center">
    <h1>PFVC – Phonetic Fidelity Voice Conversion</h1>
</div>
<div align="justify">
    <p>
        Este trabalho apresenta um fluxo de análise fonética que utiliza o dataset LibriSpeech para os falantes source e o Common Voice para os falantes target. Inicialmente, os fonemas dos áudios source são extraídos por meio do reconhecedor fonético Allosaurus. Em seguida, esses mesmos áudios passam por sistemas de Voice Conversion, com destaque para o modelo Seed-VC, para gerar versões convertidas que preservam o conteúdo linguístico do falante source, mas com as características vocais do falante target. Após a conversão, os áudios sintetizados são novamente processados pelo Allosaurus, permitindo uma comparação direta entre as sequências fonéticas originais e as convertidas. Por fim, métricas como a PER (Phoneme Error Rate) são aplicadas para quantificar de forma objetiva o grau de preservação fonética ao longo do processo.
    </p>
    <hr />
    <h2>Instalação e Setup</h2>
    <p>1. Clonar o repositório</p>

```bash
git clone --recurse-submodules https://github.com/danylo-macelai/phonetic-fidelity-voice-conversion-ptbr.git pfvc
```   
   <blockquote>
        <p>💡 <strong>Dica:</strong></p>
        <p>Se você já clonou sem submódulos: (opcional)</p>
        <pre><code>git submodule update --init --recursive</code></pre>
    </blockquote>
   <p>2. Entrar na pasta do projeto</p>

```bash
cd .\pfvc\ 
``` 
   <p>3. Criar o ambiente virtual</p>

```bash 
python -m venv .venv 
``` 
   <p>4. Ativar o ambiente virtual</p>

```bash 
.venv\Scripts\activate      # Windows

source .venv/bin/activate   # macOS / Linux
``` 
   <p>5. Atualizar o pip</p>

```bash
python -m pip install --upgrade pip 
``` 
   <p>6. Instalar o projeto em modo desenvolvimento</p>

```bash 
pip install -e . 
``` 
   <blockquote>
        <p>💡 <strong>Dica:</strong></p>
        <p>Selecionar o ambiente virtual no VSCode (opcional)</p>
        <ol>
            <li>Pressione <strong>Ctrl+Shift+P</strong> (ou Cmd+Shift+P no macOS).</li>
            <li>Digite Python: <strong>Select Interpreter</strong> e pressione <strong>Enter</strong>.</li>
            <li>Escolha o interpretador do ambiente virtual (<strong>.\venv\Scripts\python.exe</strong>).</li>
        </ol>
    </blockquote>
    <h2>Pipeline</h2>
    <ol>
        <li>
            Gerar subset filtrado do dataset:<br>
            <code>python src/main_pipeline.py prepare -ls D://.../mls_portuguese -cv D://.../pt -l dev -s 14400</code>
        </li>
    </ol>
</div>
<h2>Pré-requisitos</h2>
<div id="markdown-links-uteis" align="left">

[![ffmpeg](https://img.shields.io/badge/ffmpeg-(download)-FAEAE4)](https://ffmpeg.org/download.html)
[![CommonVoice](https://img.shields.io/badge/Common%20Voice-(dataset)-FAEAE4)](https://www.openslr.org/94/)
[![LibriSpeech](https://img.shields.io/badge/LibriSpeech-(dataset)-FAEAE4)](https://www.openslr.org/94/)
[![Python](https://img.shields.io/badge/Python-v3.10+-FAEAE4)](https://www.python.org/downloads/)
[![VSCode](https://img.shields.io/badge/VS%20Code-v1.99.3+-FAEAE4)](https://code.visualstudio.com/download)
    <blockquote>
        <p><strong>⚠️ Atenção:</strong></p>
        <p><strong>❝</strong> It also requires the command-line tool <code>ffmpeg</code> to be installed on your system, which is available from most package managers. <strong>❞</strong></p>
    </blockquote>
</div>
