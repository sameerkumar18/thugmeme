from django.shortcuts import render
from thuglife.views import thug_meme, text_meme


def index(request):
    return


def test_thug_meme(request):
    if request.method == "POST":
        contents = [i for i in (thug_meme(request))]
        print(contents)
        return render(request, "image.html", {"contents": str(contents).split("'")[1].split("'")[0]})

    return render(request, template_name="index.html")


def test_text_meme(request):
    if request.method == "POST":
        contents = text_meme(request)
        return render(request, "image.html", {"contents": contents})

    return render(request, template_name="index.html")
