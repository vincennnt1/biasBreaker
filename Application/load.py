import joblib
from preprocessing import clean # needed again for models to work

from newspaper import Article, Config

def loader():
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'

    config = Config()
    config.browser_user_agent = user_agent

    # Loading models
    title_mod = joblib.load("title_model.job")
    text_mod = joblib.load("text_model.job")
    
    return title_mod, text_mod, config

def getArticle(url, config):
    try:
        article = Article(url, config=config)
        article.download()
        article.parse()

        title = article.title
        text = article.text
    except:
        return False, False

    # deleting article to save memory
    del article
    
    return title, text