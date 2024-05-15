from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'reviews'
urlpatterns = [
    path("", views.homepage, name='homepage'),
    path('search', views.search, name='search'),
    path('search/<int:gender_id>', views.search_gender, name='search_gender'),
    path('profile/<int:profile_id>', views.profile, name='profile'),
    path('follow/<int:reviewer_id>', views.follow, name='follow'),
    path('unfollow/<int:reviewer_id>', views.unfollow, name='unfollow'),
    path('login_register', views.login_register, name='login_register'),
    path('loginview', views.loginview, name='loginview'),
    path('registerview', views.registerview, name='registerview'),
    path('logoutview', views.logoutview, name='logoutview'),
    path('review/<int:review_id>', views.review, name='review'),
    path('createreview', views.createreview, name='createreview'),
    path('review/<int:review_id>/deletereview', views.deletereview, name='deletereview'),
    path('deletecomment/<int:comment_id>', views.deletecomment, name='deletecomment'),
    path('editar_perfil', views.editar_perfil, name='editar_perfil'),
    path('termsofservice', views.termsofservice, name='termsofservice'),
    path('aboutus', views.aboutus, name="aboutus"),
    path('contact', views.contact, name="contact"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
