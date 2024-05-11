from django.contrib import admin
from .models import Account, Project, Task

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ['username', 'email']



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ['owner', 'project_name']



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ['task_owner', 'description']