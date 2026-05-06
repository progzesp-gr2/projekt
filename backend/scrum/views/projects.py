from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet
from rest_framework import generics, permissions

from ..models import Project, ProjectMembership, Sprint, Task
from ..serializers import (
    ProjectMembershipSerializer,
    ProjectSerializer,
    SprintSerializer,
    TaskSerializer,
    UserSerializer,
)

User = get_user_model()


def accessible_projects_queryset(user) -> QuerySet[Project]:
    return Project.objects.filter(Q(owner=user) | Q(memberships__user=user)).distinct()


def visible_tasks_queryset(user):
    return Task.objects.filter(project__in=accessible_projects_queryset(user)).distinct()


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return (
            accessible_projects_queryset(self.request.user)
            .select_related('owner')
            .prefetch_related('memberships')
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return (
            accessible_projects_queryset(self.request.user)
            .select_related('owner')
            .prefetch_related('memberships')
        )


class ProjectMembershipListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectMembershipSerializer

    def get_project(self) -> Project:
        return generics.get_object_or_404(accessible_projects_queryset(self.request.user), pk=self.kwargs['project_pk'])

    def get_queryset(self):
        return ProjectMembership.objects.filter(project=self.get_project()).select_related('user')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project'] = self.get_project()
        return context

    def perform_create(self, serializer):
        serializer.save(project=self.get_project())


class ProjectMembershipDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectMembershipSerializer

    def get_queryset(self):
        return ProjectMembership.objects.filter(
            project__in=accessible_projects_queryset(self.request.user),
            project_id=self.kwargs['project_pk'],
        ).select_related('user', 'project')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project'] = self.get_object().project
        return context


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.order_by('username')


class SprintListCreateView(generics.ListCreateAPIView):
    serializer_class = SprintSerializer

    def get_queryset(self):
        qs = Sprint.objects.filter(project__in=accessible_projects_queryset(self.request.user))
        params = self.request.query_params
        if project := params.get('project'):
            qs = qs.filter(project_id=project)
        if status := params.get('status'):
            qs = qs.filter(status=status)
        return qs


class SprintDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SprintSerializer

    def get_queryset(self):
        return Sprint.objects.filter(project__in=accessible_projects_queryset(self.request.user))


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        qs = visible_tasks_queryset(self.request.user)
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
    serializer_class = TaskSerializer

    def get_queryset(self):
        return visible_tasks_queryset(self.request.user)
