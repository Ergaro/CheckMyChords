"""CMC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from CheckMyChords.views import (
    HelloWorldView,
    AddPieceView,
    CheckPieceView,
    PiecesView,
    GenerateMidiView,
)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello_world$', HelloWorldView.as_view()),
    
    url(r'^new_piece$', AddPieceView.as_view(), name="add_new_piece"),
    url(r'^check_piece/(?P<piece_id>(\d)+)$', CheckPieceView.as_view(),
        name = 'check_piece' ),
    url(r'^$', PiecesView.as_view(), name = 'pieces'),
    url(r'^generate_midi/(?P<piece_id>(\d)+)$', GenerateMidiView.as_view(),
        name = "generate_midi"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
