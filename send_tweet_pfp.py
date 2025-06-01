import os
import tweepy

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def carregar_blocos_tweets(nome_arquivo):
    with open(nome_arquivo, "r", encoding="utf-8") as f:
        conteudo = f.read().strip()
    blocos = conteudo.split("\n\n")  # separa por linha em branco
    tweets = []
    for bloco in blocos:
        linhas = bloco.strip().split("\n")
        if len(linhas) >= 3:
            nome = linhas[0].strip()
            descricao = linhas[1].strip()
            imagem = linhas[2].strip()
            texto = f"{nome}\n{descricao}"
            tweets.append((texto, imagem))
    return tweets

def tweet_do_dia(texto, imagem_path):
    try:
        media = api.media_upload(imagem_path)
        api.update_status(status=texto, media_ids=[media.media_id_string])
        print(f"✅ Tweet enviado:\n{texto}\ncom imagem {imagem_path}")
    except Exception as e:
        print(f"❌ Erro ao enviar tweet: {e}")

if __name__ == "__main__":
    tweets = carregar_blocos_tweets("tweets_pfp.txt")
    
    import datetime
    dia = datetime.datetime.utcnow().day
    indice = (dia - 1) % len(tweets)
    texto, imagem = tweets[indice]
    
    caminho_imagem = os.path.join("images", imagem)  # Ajuste o caminho conforme sua pasta de imagens
    
    tweet_do_dia(texto, caminho_imagem)
