from django.urls import path

from user import views

urlpatterns = [
    path("<str:username>", views.UserView.as_view()),
    path("<str:username>/avatar",views.user_avatar)
]
