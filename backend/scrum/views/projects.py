from rest_framework import generics

from ..models import Project, Sprint, Task
from ..serializers import ProjectSerializer, SprintSerializer, TaskSerializer


class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class SprintListCreateView(generics.ListCreateAPIView):
    serializer_class = SprintSerializer

    def get_queryset(self):
        qs = Sprint.objects.all()
        params = self.request.query_params
        if project := params.get('project'):
            qs = qs.filter(project_id=project)
        if status := params.get('status'):
            qs = qs.filter(status=status)
        return qs


class SprintDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        qs = Task.objects.all()
        params = self.request.query_params
        if project := params.get('project'):
            qs = qs.filter(project_id=project)
        if sprint := params.get('sprint'):
            qs = qs.filter(sprint_id=sprint)
        if status := params.get('status'):
            qs = qs.filter(status=status)
        if assignee := params.get('assignee'):
            qs = qs.filter(assignee_id=assignee)
        return qs

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
