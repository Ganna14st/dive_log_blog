from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.get_all_posts, name='get_all_posts'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('post/<int:post_id>/', views.show_post, name='show_post'),
    path('contact/', views.contact, name='contact'),
    path('new_post/', views.add_new_post, name='new_post'),
    path('edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('log_book/', views.log_book, name='log_book'),
    path('log_book/<int:log_id>/', views.show_log, name='show_log'),
    path('new_log/', views.add_log, name='add_log'),
    path('edit_log/<int:log_id>/', views.edit_log, name='edit_log'),
    path('delete_log/<int:log_id>/', views.delete_log, name='delete_log'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
