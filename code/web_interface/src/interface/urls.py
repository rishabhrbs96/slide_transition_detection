from django.conf.urls import url,include
from .views import slides_file,interface_home,interface_time,interface_compare,interface_convert,interface_download,interface_again,seconds_file,mail_to
urlpatterns = [
	url(r'^data.txt', seconds_file),
	url(r'^ans.csv', slides_file),
	url(r'^download/', interface_download),
	url(r'^mail/', mail_to),
    url(r'^home/', interface_home),
    url(r'^time/', interface_time),
    url(r'^compare/', interface_compare),
    url(r'^convert/', interface_convert),
    url(r'^again/', interface_again),
]