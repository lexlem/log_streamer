from django.conf.urls import url
from .views import JSONStreamer

urlpatterns = [
    url(r'^read_log$', JSONStreamer.as_view(), name='json_streamer')
]
