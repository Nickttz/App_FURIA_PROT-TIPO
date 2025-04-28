from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

# from twitter_api import fetch_tweets_from_twitter 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar os arquivos estáticos
app.mount("/data", StaticFiles(directory="data"), name="data")

# Palavras-chave
furia_keywords = ["furia", "#furia", "@furia"]
games_keywords = {
    "CS:GO": ["csgo", "cs:go", "counter-strike"],
    "Valorant": ["valorant", "vava"],
    "League of Legends": ["lol", "league of legends"],
    "Rainbow Six Siege": ["rainbow six", "r6"],
    "Free Fire": ["free fire"],
    "Apex Legends": ["apex legends"],
    "Rocket League": ["rocket league", "rl"],
    "PUBG": ["pubg"],
    "Dota 2": ["dota 2"],
    "Fortnite": ["fortnite"],
    "Xadrez": ["xadrez", "chess"],
    "Poker": ["poker"],
}

class GameAnalysis(BaseModel):
    label: str
    percent: float

class AnalyzeRequest(BaseModel):
    username: str

class AnalyzeResponse(BaseModel):
    furia_percent: float
    games: list[GameAnalysis]
    profile_photo: str  

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_user(data: AnalyzeRequest):
    username = data.username.lstrip('@')
    file_path = f"{username}_tweets.feather"

    try:
        if not os.path.exists(file_path):
            # FUTURA INTEGRAÇÃO COM API DO TWITTER:
            # tweets = fetch_tweets_from_twitter(username)
            # if not tweets:
            #     raise HTTPException(status_code=404, detail="Nenhum tweet encontrado na API do Twitter.")
            # df = pd.DataFrame(tweets)
            # df.to_feather(file_path)
            raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
        else:
            df = pd.read_feather(file_path)
    except Exception as e:
        print(f"[ERRO] Falha ao carregar os dados: {e}")
        raise HTTPException(status_code=500, detail="Erro ao carregar os dados.")

    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhum tweet encontrado.")

    total_tweets = len(df)
    furia_tweets = 0
    only_furia = 0
    game_counts = {game: 0 for game in games_keywords.keys()}

    for content in df['content'].str.lower():
        mentions_furia = any(keyword in content for keyword in furia_keywords)
        mentioned_game = None

        for game, keywords in games_keywords.items():
            if any(keyword in content for keyword in keywords):
                mentioned_game = game
                game_counts[game] += 1
                break

        if mentions_furia:
            furia_tweets += 1
            if not mentioned_game:
                only_furia += 1

    furia_percent = ((furia_tweets + only_furia) / total_tweets) * 100

    games_list = []
    for game, count in game_counts.items():
        if count > 0:
            games_list.append({
                "label": game,
                "percent": round((count / total_tweets) * 100, 2)
            })

    if only_furia > 0:
        games_list.append({
            "label": "Só FURIA",
            "percent": round((only_furia / total_tweets) * 100, 2)
        })

    # Incluir o caminho da foto do perfil na resposta
    return AnalyzeResponse(
        furia_percent=round(furia_percent, 2),
        games=games_list,
        profile_photo="data/user_photo.png"  # A URL da foto do perfil
    )

# DADOS DE TESTE PARA SIMULAR ANÁLISE 
data = [
    {"date": "2023-04-01", "content": "Comecei a jogar com a FURIA no CS:GO! Tô amando! #FURIA #CSGO", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-02", "content": "Valorant tem sido minha terapia diária. ❤️ #Valorant", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-03", "content": "A FURIA tá jogando demais! #FURIA #CBLOL", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-03", "content": "FURIA destruindo no League of Legends! Vamos meninas! #FURIA #LoL", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-04", "content": "Assistindo a LOUD antes de dormir. Relax total. #GOLOUD", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-05", "content": "Não curti muito o jogo da FURIA ontem... dava pra ganhar! #FURIA #CBLOL", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-06", "content": "Almoço pronto, podcast de CS:GO rolando. 💻🍝 #almoco #CSGO", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-06", "content": "A RED Canids hoje foi impecável! Que time! #REDCanids #CBLOL", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-07", "content": "Bom dia! Já com café na mão e pensando na próxima partida. ☕️🎮", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-08", "content": "O FalleN é um monstro. Que jogada! #FalleN #CSGO", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-09", "content": "Hoje é dia de torcer pra FURIA na semi! Bora! 🔥 #FURIA #GoFURIA", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-10", "content": "Acho que a FURIA precisa repensar o draft... algo não encaixa. #FURIA", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-11", "content": "Amo colocar a live do Gaules enquanto estudo. 💻📚 #Gaules #CSGO", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-12", "content": "Ganhei uma ranked no CS:GO! Que sensação boa! 🥳 #gameplay", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-13", "content": "FURIA é o orgulho do Brasil nos esports! 💚 #FURIA", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-14", "content": "Contando os dias pro CBLOL final! Ansiosa demais! #CBLOL", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-15", "content": "LOUD na final! Tô torcendo muito por elas! 💥 #GOLOUD #CBLOL", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-16", "content": "Sem tempo até pra respirar esses dias... vida adulta né? 😅 #correria", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-17", "content": "FURIA merecia mais nesse jogo. Foi bem, mas o adversário foi melhor. #FURIA #CSGO", "username": "ana_gamer", "at_username": "@ana_gamer"},
    {"date": "2023-04-18", "content": "LOUD x RED foi insano! Jogo digno de final! #CBLOL #GOLOUD #REDCanids", "username": "ana_gamer", "at_username": "@ana_gamer"}
]

df = pd.DataFrame(data)
df["profile_photo"] = "data/user_photo.png"  # A URL da foto do perfil
df.to_feather("ana_gamer_tweets.feather")
