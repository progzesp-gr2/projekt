from rest_framework import serializers
from ..models import Project, Sprint, Task
from django.contrib.auth import get_user_model

User = get_user_model()


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'role')


class ProjectSerializer(serializers.ModelSerializer):
    owner = MemberSerializer(read_only=True)
    scrum_master = MemberSerializer(read_only=True)
    members = MemberSerializer(many=True, read_only=True)
    scrum_master_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='scrum_master',
        write_only=True,
        required=False,
        allow_null=True,
    )
    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='members',
        write_only=True,
        many=True,
        required=False,
    )

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'key', 'description',
            'owner', 'scrum_master', 'scrum_master_id',
            'members', 'member_ids',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = '__all__'
        read_only_fields = ('id',)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('id', 'reporter', 'created_at', 'updated_at')