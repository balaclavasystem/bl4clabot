import os
import tweepy
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do arquivo .env para dentro do ambiente

# Pega as credenciais do Twitter das variáveis de ambiente
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Configura o cliente Tweepy com suas credenciais
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def enviar_gm_tweet():
    texto = "GM"  # texto fixo do tweet que você quer enviar
    try:
        # Cria o tweet com o texto "GM"
        response = client.create_tweet(text=texto)
        print(f"✅ Tweet enviado: https://twitter.com/user/status/{response.data['id']}")
    except Exception as e:
        print(f"❌ Erro ao enviar tweet: {e}")

# Quando você rodar o arquivo diretamente, vai executar essa função
if __name__ == "__main__":
    enviar_gm_tweet()
