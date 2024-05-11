from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectView.as_view()),
    path('register/', views.RegistrationApiView.as_view()),
    path('login/', views.LoginApiView.as_view()),
    path('user/', views.UserApiView.as_view()),
    path('change-password/', views.ChangePasswordView.as_view()),

    path('<pk>/', views.ProjectDetailView.as_view()),

    path('<project_pk>/tasks/', views.TaskView.as_view()),
    path('task/<pk>/', views.TaskDetailView.as_view()),

]