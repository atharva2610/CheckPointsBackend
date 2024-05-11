from rest_framework.permissions import BasePermission, SAFE_METHODS
from app_checkpoints.models import Project, Task
from django.contrib.auth.models import AnonymousUser

class IsProjectOwner(BasePermission):
    def has_permission(self, request, view):
        project_id = None
        if 'pk' in view.kwargs:
            project_id = view.kwargs.get('pk')
        elif 'project_pk' in view.kwargs:
            project_id = view.kwargs.get('project_pk')

        project = Project.objects.get(id=project_id)
        return project.owner == request.user
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    

class IsTaskOwner(BasePermission):
    def has_permission(self, request, view):
        task = Task.objects.get(id=view.kwargs.get('pk'))
        return task.task_owner == request.user
    
    def has_object_permission(self, request, view, obj):
        return obj.task_owner == request.user
    
    
class UnauthenticatedOnly(BaseException):
    def has_permission(self, request, view):
        return request.user == AnonymousUser()
    
    def has_object_permission(self, request, view, obj):
        return True