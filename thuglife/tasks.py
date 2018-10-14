from celery import shared_task
from core import ThugLifeMeme, TextMeme

import redis
from uuid import uuid4

@shared_task(name='thuglife_task', ignore_result=False, bind=True)
def thug_life_task(t, uploaded_file_url,filekey):
    r = redis.from_url(os.environ.get("REDIS_URL"))
    file = r.get(filekey)
    print(file);
    
    obj = ThugLifeMeme()
    contents = obj.meme(uploaded_file_url)
    return contents


@shared_task(name='textmeme_task', ignore_result=False, bind=True)
def text_meme_task(t, top_text, bottom_text, uploaded_file_url):
    obj = TextMeme()
    contents = obj.meme(top_text, bottom_text, uploaded_file_url)
    return contents
