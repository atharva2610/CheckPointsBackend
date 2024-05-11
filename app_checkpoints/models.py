from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from uuid import uuid4

# USER Model
class MyAccountManager(BaseUserManager):

    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Email address required.")
        if not username:
            raise ValueError("Username required.")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,username,password):
        user  = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key = True, default = uuid4, editable = False)
    email = models.EmailField(verbose_name="email", max_length=50, unique=True)
    username = models.CharField(max_length=30, unique=True)
    join_date = models.DateTimeField(verbose_name="join date", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    


# PROJECT Model
class Project(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid4, editable = False)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='owner', editable=False)
    project_name = models.CharField(max_length=50)
    

    def __str__(self):
        return self.project_name
    


# TASK Model
class Task(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid4, editable = False)
    task_owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='task_owner', editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="task", editable=False)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'by: {self.task_owner.username} , {self.description[:15]}'