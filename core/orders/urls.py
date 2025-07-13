from django.urls import path
# from django.conf.
from django.conf import settings
from django.conf.urls.static import static
from orders.views import ContactView, SolutionView3
urlpatterns=[
    path('contacts/',ContactView.as_view(),name='contact-lists'),
    # path('identify/', SolutionView.as_view(), name='solutions'),
    path('identify/',SolutionView3.as_view(), name='solution')    # the main solution
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 