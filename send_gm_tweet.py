import os
import tweepy
from dotenv import load_dotenv
import datetime

load_dotenv()

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def carregar_tweets_do_arquivo(nome_arquivo="tweets.txt"):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
        blocos = conteudo.split("\n\n")
        tweets = [bloco.strip() for bloco in blocos if bloco.strip()]
        return tweets
    except Exception as e:
        print(f"Erro ao carregar tweets: {e}")
        return []

def tweet_do_dia(tweets):
    if not tweets:
        print("Nenhum tweet encontrado.")
        return None
    dia = datetime.datetime.utcnow().day
    indice = (dia - 1) % len(tweets)
    return tweets[indice]

if __name__ == "__main__":
    tweets = carregar_tweets_do_arquivo()
    texto = tweet_do_dia(tweets)
    if texto:
        try:
            response = client.create_tweet(text=texto)
            print(f"✅ Tweet enviado: https://twitter.com/user/status/{response.data['id']}")
        except Exception as e:
            print(f"❌ Erro ao enviar tweet: {e}")
    else:
        print("⚠️ Nenhum texto para enviar hoje.")
