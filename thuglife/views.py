import os

from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

from PIL import Image
from ratelimit.decorators import ratelimit

from thuglife.tasks import thug_life_task, text_meme_task
from thugmeme.settings import RATE_LIMIT, RATE_LIMIT_KEY, THUG_MEME_IMAGEQ, TEXT_MEME_IMAGEQ
import os
import redis
from io import StringIO
from uuid import uuid4
from imgurpython import ImgurClient

client_id = '9f7f3d8f201abba'
client_secret = '02a4389e96d3b7f5c5a3614b3f8e6b8da39539ad'

client = ImgurClient(client_id, client_secret)


@ratelimit(key=RATE_LIMIT_KEY, rate=RATE_LIMIT)
def thug_meme(request):
    if request.method == 'POST':
        file = request.FILES['inputfile']

        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = str(fs.url(filename)).replace("%20", " ")
        im = Image.open(uploaded_file_url)
        # os.remove(os.getcwd() + '/' + uploaded_file_url)
        im.save(uploaded_file_url, quality=THUG_MEME_IMAGEQ)
        
        #im.save(output, format=im.format)
        
        #filekey = uuid4();
        
        try:
            #r.set(filekey, output.getvalue())
            
            url = client.upload_from_path(uploaded_file_url)['link']
            t = thug_life_task.delay(url, filename)
            contents = t.get()
            os.remove(os.getcwd() + '/' + uploaded_file_url)

        except Exception as e:
            print(e.with_traceback)
            os.remove(os.getcwd() + '/' + uploaded_file_url)

            try:
                output_path = "thug_" + str(uploaded_file_url.split(".")[0]) + ".png"
                os.remove(os.getcwd() + '/' + output_path)
            except:
                pass

            return JsonResponse({"url": "", "reason": str(e)}, status=500)

        return JsonResponse(data={"url": contents, "reason": ""}, status=200)

@ratelimit(key=RATE_LIMIT_KEY, rate=RATE_LIMIT)
def text_meme(request):
    top_text = request.POST["top"]
    bottom_text = request.POST["bottom"]
    file = request.FILES["inputfile"]

    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    uploaded_file_url = str(fs.url(filename)).replace("%20", " ")
    im = Image.open(uploaded_file_url)
    os.remove(os.getcwd() + '/' + uploaded_file_url)
    im.save(uploaded_file_url, quality=TEXT_MEME_IMAGEQ)

    try:
        t = text_meme_task.delay(top_text, bottom_text, uploaded_file_url)
        contents = t.get()
        os.remove(os.getcwd() + '/' + uploaded_file_url)
        return JsonResponse(data={"url": contents, "reason": ""}, status=200)

    except Exception as e:
        print(e)
        os.remove(os.getcwd() + '/' + uploaded_file_url)
        return JsonResponse(data={"url": "", "reason": str(e)}, status=500)
