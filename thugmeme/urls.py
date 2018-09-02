from django.urls import path,include

from thuglife.views import thug_meme, text_meme
from website.views import test_thug_meme, test_text_meme


urlpatterns = [
    path('test/', include('website.urls')),
    path('api/', include('thuglife.urls')),

]
