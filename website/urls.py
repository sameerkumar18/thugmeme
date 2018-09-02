from django.urls import path,include

from website.views import test_thug_meme, test_text_meme


urlpatterns = [

    path('thug_meme/', test_thug_meme),
    path('text_meme/', test_text_meme),
]