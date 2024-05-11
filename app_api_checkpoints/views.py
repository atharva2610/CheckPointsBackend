from django.contrib.auth import authenticate
from app_checkpoints.models import Account, Project, Task

from .serializers import ProjectSerializer, TaskSerializer, UserSerializer,ChangePasswordSerializer

from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView

from .custom_permissions import IsProjectOwner, IsTaskOwner, UnauthenticatedOnly

from rest_framework_simplejwt.tokens import RefreshToken

class RegistrationApiView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UnauthenticatedOnly]



class UserApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        serializer = UserSerializer(data=request.data, instance=request.user, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginApiView(APIView):
    permission_classes = [UnauthenticatedOnly]
    
    def post(self, request, format=None):
        try:
            user_obj = authenticate(username=request.data.get('username'), password=request.data.get('password'))
            if user_obj is not None:
                token = RefreshToken.for_user(user_obj)
                serializer = UserSerializer(user_obj)
                return Response({'access':str(token.access_token), 'user':serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'messages': [{'message':str(e)}]}, status=status.HTTP_400_BAD_REQUEST)



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ProjectView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return reversed(Project.objects.filter(owner=self.request.user.id))
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context



class ProjectDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectOwner]



class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_pk):
        try:
            project = Project.objects.get(id=project_pk)
            tasks = reversed(Task.objects.filter(project_id=project_pk))
            project_serializer = ProjectSerializer(project)
            tasks_serializer = TaskSerializer(tasks, many=True)
            return Response({'checklist': project_serializer.data, 'tasks': tasks_serializer.data}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response("CheckList not found!", status=status.HTTP_404_NOT_FOUND)

    def post(self, request, project_pk, format=None):
        try:
            serializer = TaskSerializer(data=request.data)
            print('serializer: ', serializer.initial_data)
            serializer.context['user'] = request.user
            serializer.context['project'] = Project.objects.get(id=project_pk)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response("CheckList not found!", status=status.HTTP_404_NOT_FOUND)
        



class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskOwner]