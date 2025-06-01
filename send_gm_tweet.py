import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Autenticação com Tweepy (API v1.1 para postar tweet simples)
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def carregar_tweets():
    try:
        with open("tweets.txt", "r", encoding="utf-8") as f:
            # Cada tweet separado por linha vazia
            conteudo = f.read().strip()
        blocos = conteudo.split("\n\n")
        tweets = [bloco.strip().replace('\n', ' ') for bloco in blocos if bloco.strip()]
        return tweets
    except FileNotFoundError:
        print("⚠️ Arquivo tweets.txt não encontrado.")
        return []

def tweet_do_dia():
    import datetime
    tweets = carregar_tweets()
    if not tweets:
        print("⚠️ Nenhum tweet disponível.")
        return None
    dia = datetime.datetime.utcnow().day
    indice = (dia - 1) % len(tweets)
    return tweets[indice]

if __name__ == "__main__":
    texto = tweet_do_dia()
    if texto:
        try:
            api.update_status(texto)
            print(f"✅ Tweet enviado: {texto}")
        except Exception as e:
            print(f"❌ Erro ao enviar tweet: {e}")
    else:
        print("⚠️ Não há tweet para enviar hoje.")
