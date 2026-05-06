from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Project, ProjectMembership, Sprint, Task
from .auth import UserSerializer

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    current_user_role = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    owner_details = UserSerializer(source='owner', read_only=True)

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'key',
            'description',
            'owner',
            'owner_details',
            'created_at',
            'updated_at',
            'current_user_role',
            'is_owner',
        )
        read_only_fields = (
            'id',
            'owner',
            'owner_details',
            'created_at',
            'updated_at',
            'current_user_role',
            'is_owner',
        )

    def get_current_user_role(self, obj: Project):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user is None or not user.is_authenticated:
            return None
        if obj.owner_id == user.id:
            return ProjectMembership.ProjectRole.PRODUCT_OWNER
        return obj.memberships.filter(user_id=user.id).values_list('role', flat=True).first()

    def get_is_owner(self, obj: Project):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        return bool(user and user.is_authenticated and obj.owner_id == user.id)


class ProjectMembershipSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ProjectMembership
        fields = (
            'id',
            'project',
            'user',
            'user_details',
            'role',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'project', 'created_at', 'updated_at')


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
