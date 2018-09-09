from celery import shared_task
from core import ThugLifeMeme, TextMeme


@shared_task(name='thuglife_task', ignore_result=False, bind=True)
def thug_life_task(t, uploaded_file_url):
    obj = ThugLifeMeme()
    contents = obj.meme(uploaded_file_url)
    return contents


@shared_task(name='textmeme_task', ignore_result=False, bind=True)
def text_meme_task(t, top_text, bottom_text, uploaded_file_url):
    obj = TextMeme()
    contents = obj.meme(top_text, bottom_text, uploaded_file_url)
    return contents
