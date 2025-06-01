import os
import tweepy
import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Autenticação tweepy com OAuth1UserHandler para v1.1 (requerido para criar tweets)
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def carregar_tweets_do_arquivo(nome_arquivo="tweets.txt"):
    tweets = []
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
            blocos = conteudo.split("\n\n")  # separa por linhas vazias
            for bloco in blocos:
                texto = bloco.strip()
                if texto:
                    tweets.append(texto)
    except FileNotFoundError:
        print(f"⚠️ Arquivo {nome_arquivo} não encontrado.")
    return tweets

def tweet_do_dia(tweets):
    if not tweets:
        return None
    dia = datetime.datetime.utcnow().day
    indice = (dia - 1) % len(tweets)
    return tweets[indice]

def enviar_tweet(texto):
    if not texto:
        print("⚠️ Nenhum texto para enviar.")
        return
    try:
        api.update_status(texto)
        print(f"✅ Tweet enviado:\n{texto}")
    except Exception as e:
        print(f"❌ Erro ao enviar tweet: {e}")

if __name__ == "__main__":
    tweets = carregar_tweets_do_arquivo()
    texto_do_dia = tweet_do_dia(tweets)
    enviar_tweet(texto_do_dia)
