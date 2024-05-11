from rest_framework import serializers
from app_checkpoints.models import Account, Project, Task
from rest_framework.validators import ValidationError

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['id', 'username', 'email','password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        user = Account(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def validate(self, attrs):
        if "password" in attrs:
            if attrs["password"] != attrs["password2"]:
                raise ValidationError("The two passwords didn’t match.")
        return super().validate(attrs)
    


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        return super().create(validated_data)

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
    #     project_obj = Project.objects.get(id = self.context.get('project_'))
    #     request = self.context.get('user')
        validated_data['task_owner'] = self.context.get('user')
        validated_data['project'] = self.context.get('project')
        return super().create(validated_data)