from rest_framework import serializers
from .models import Project, Membership
from .models import User, Task

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email',]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters")
        return value

    def create(self, validated_data):
        print("---------------", validated_data)
        return User.objects.create_user(**validated_data)



class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description']

from rest_framework import serializers
from .models import Membership, User

class AddMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role = serializers.ChoiceField(choices=['ADMIN', 'MEMBER'])

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        return value

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'assigned_to', 'status', 'due_date']

    def validate(self, data):
        project = data.get('project')
        user = data.get('assigned_to')

        # 🔥 check if assigned user is part of project
        if user:
            if not Membership.objects.filter(user=user, project=project).exists():
                raise serializers.ValidationError("User is not a member of this project")

        return data
