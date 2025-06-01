import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

# Variáveis do ambiente
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Autenticação v2 (funciona com tweepy.Client)
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Carrega os tweets do arquivo
def carregar_tweets(nome_arquivo):
    tweets = []
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            blocos = f.read().strip().split("\n\n")
            for bloco in blocos:
                texto = bloco.strip()
                if texto:
                    tweets.append(texto)
    except FileNotFoundError:
        print("❌ Arquivo não encontrado.")
    return tweets

# Enviar tweet do dia baseado no dia do mês
def tweet_do_dia(tweets):
    import datetime
    if not tweets:
        print("❌ Nenhum tweet encontrado.")
        return None
    dia = datetime.datetime.utcnow().day
    return tweets[(dia - 1) % len(tweets)]

if __name__ == "__main__":
    tweets = carregar_tweets("tweets.txt")
    texto = tweet_do_dia(tweets)
    if texto:
        try:
            response = client.create_tweet(text=texto)
            print(f"✅ Tweet enviado: https://twitter.com/user/status/{response.data['id']}")
        except Exception as e:
            print(f"❌ Erro ao enviar tweet: {e}")
