from rest_framework import serializers

from ..models import Project, Sprint, Task


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
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