# 🎮 Know You Fan - Perfil de Fã de eSports com FastAPI

Este é um protótipo de API construído com **FastAPI** para análise de perfis de fãs com foco em **esports** e interações sociais com organizações como a **FURIA**.

Ele simula o comportamento de um serviço de back-end que analisa tweets de um usuário e identifica:
- O quanto ele interage com a FURIA
- Quais jogos ele mais menciona
- Um score de afinidade por conteúdo

---

## 🚀 Funcionalidades

✅ Análise semântica de tweets salvos localmente  
✅ Classificação dos tweets por tipo de jogo (ex: CS:GO, Valorant)  
✅ Cálculo de engajamento com a FURIA  
✅ Retorno de imagem de perfil do fã  
✅ CORS habilitado para fácil integração com front-end  
✅ Estrutura pronta para integrar com a API do Twitter

---

## 📦 Estrutura

App_FURIA_PROT-TIPO/  
├── main.py               # Código principal da FastAPI  
├── data/                 # Pasta de imagens e arquivos do usuário  
│   └── user_photo.png    # Foto do perfil do usuário para retorno da API  
├── ana_gamer_tweets.feather  # Arquivo com os tweets simulados para análise  
├── requirements.txt      # Arquivo que lista as dependências do projeto  

## ▶️ Como Executar Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/Nickttz/App_FURIA_PROT-TIPO.git
cd App_FURIA_PROT-TIPO
```

### 2. Crie um ambiente virtual e instale as dependências

python -m venv venv  
source venv/bin/activate  # Linux/MacOS  
venv\Scripts\activate     # Windows  
pip install -r requirements.txt  

### 3. Rode o servidor 

```bash
uvicorn main:app --reload
```

## 📤 Endpoint Principal

Envia o nome de usuário (ex: ana_gamer) para análise.

### Corpo da Requisição:

```json
{
  "username": "ana_gamer"
}
```

### Resposta:

```json
{
  "furia_percent": 55,
  "games": [
    {"label": "CS:GO", "percent": 30},
    {"label": "League of Legends", "percent": 35},
    {"label": "Valorant", "percent": 5},
    {"label": "Só FURIA", "percent": 15}
  ],
  "profile_photo": "data/user_photo.png"
}
```

## 🧪 Dados de Teste

O repositório inclui um conjunto de dados (ana_gamer_tweets.feather) com 19 tweets simulados de uma fã, utilizados pela API para gerar o perfil.  
Todos os dados são fictícios gerados pelo ChatGPT, incluindo a própria foto de perfil

## 🎥 Demonstração em GIF

![Main - Pessoal — Microsoft_ Edge 2025-04-28 18-19-03](https://github.com/user-attachments/assets/8f3fa2e6-02e8-4c28-9e1c-48d015216726)

## 🧠 Futuras Melhorias
- Integração com a API real do Twitter e outras redes sociais (via OAuth)
- Dashboard visual
- Reconhecimento de imagem de perfil com IA
- Armazenamento em banco de dados (Firebase ou MongoDB)
- Recomendações de conteúdo baseado na análise de perfil do usuário feito por uma IA

## 📄 Licença
Este projeto é um protótipo educacional, criado para fins de demonstração de análise de fãs com base em interações digitais.
