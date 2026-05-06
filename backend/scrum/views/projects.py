from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q, QuerySet
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError

from ..models import Project, ProjectMembership, Sprint, Task
from ..serializers import (
    ProjectMembershipSerializer,
    ProjectSerializer,
    SprintSerializer,
    TaskSerializer,
    UserSerializer,
)

User = get_user_model()

ROLE_PRODUCT_OWNER = ProjectMembership.ProjectRole.PRODUCT_OWNER
SPRINT_MANAGEMENT_ROLES = {
    ROLE_PRODUCT_OWNER,
    ProjectMembership.ProjectRole.SCRUM_MASTER,
}
TASK_MANAGEMENT_ROLES = {
    ROLE_PRODUCT_OWNER,
    ProjectMembership.ProjectRole.SCRUM_MASTER,
}


def accessible_projects_queryset(user) -> QuerySet[Project]:
    return Project.objects.filter(Q(owner=user) | Q(memberships__user=user)).distinct()


def get_project_role(project: Project, user) -> str | None:
    if project.owner_id == user.id:
        return ROLE_PRODUCT_OWNER
    return (
        project.memberships.filter(user_id=user.id)
        .values_list('role', flat=True)
        .first()
    )


def ensure_role(project: Project, user, allowed_roles: set[str], message: str):
    if get_project_role(project, user) not in allowed_roles:
        raise PermissionDenied(message)


def visible_tasks_queryset(user):
    return Task.objects.filter(
        Q(project__owner=user)
        | Q(
            project__memberships__user=user,
            project__memberships__role=ProjectMembership.ProjectRole.SCRUM_MASTER,
        )
        | Q(
            project__memberships__user=user,
            project__memberships__role=ProjectMembership.ProjectRole.PROGRAMMER,
            assignee=user,
        )
    ).distinct()


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

    def perform_update(self, serializer):
        project: Project = serializer.instance
        if project.owner_id != self.request.user.id:
            raise PermissionDenied('Only project owner can modify project details.')

        new_owner_id = self.request.data.get('owner')
        if new_owner_id is not None:
            try:
                new_owner_id = int(new_owner_id)
            except (TypeError, ValueError):
                raise ValidationError({'owner': 'Owner must be a valid user id.'})

            new_owner = User.objects.filter(pk=new_owner_id).first()
            if new_owner is None:
                raise ValidationError({'owner': 'Owner must be a valid user id.'})
        else:
            new_owner = None

        if new_owner is not None and new_owner.id != project.owner_id:
            if not ProjectMembership.objects.filter(project=project, user=new_owner).exists():
                raise ValidationError({'owner': 'New owner must be an existing project member.'})

            previous_owner_id = project.owner_id
            with transaction.atomic():
                ProjectMembership.objects.filter(project=project, user=new_owner).delete()
                serializer.save(owner=new_owner)

                if previous_owner_id and previous_owner_id != new_owner.id:
                    ProjectMembership.objects.update_or_create(
                        project=project,
                        user_id=previous_owner_id,
                        defaults={'role': ProjectMembership.ProjectRole.PROGRAMMER},
                    )
            return

        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner_id != self.request.user.id:
            raise PermissionDenied('Only project owner can delete project.')
        instance.delete()


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
        project = self.get_project()
        if project.owner_id != self.request.user.id:
            raise PermissionDenied('Only project owner can add members.')
        serializer.save(project=project)


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

    def perform_update(self, serializer):
        membership = self.get_object()
        if membership.project.owner_id != self.request.user.id:
            raise PermissionDenied('Only project owner can change member role.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.project.owner_id != self.request.user.id:
            raise PermissionDenied('Only project owner can remove members.')
        instance.delete()


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

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        ensure_role(project, self.request.user, SPRINT_MANAGEMENT_ROLES, 'You do not have permissions to create sprints in this project.')
        serializer.save()


class SprintDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SprintSerializer

    def get_queryset(self):
        return Sprint.objects.filter(project__in=accessible_projects_queryset(self.request.user))

    def perform_update(self, serializer):
        sprint = self.get_object()
        ensure_role(sprint.project, self.request.user, SPRINT_MANAGEMENT_ROLES, 'You do not have permissions to modify this sprint.')
        serializer.save()

    def perform_destroy(self, instance):
        ensure_role(instance.project, self.request.user, SPRINT_MANAGEMENT_ROLES, 'You do not have permissions to delete this sprint.')
        instance.delete()


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
        project = serializer.validated_data['project']
        ensure_role(project, self.request.user, TASK_MANAGEMENT_ROLES, 'You do not have permissions to create tasks in this project.')
        serializer.save(reporter=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return visible_tasks_queryset(self.request.user)

    def perform_update(self, serializer):
        task = self.get_object()
        ensure_role(task.project, self.request.user, TASK_MANAGEMENT_ROLES, 'You do not have permissions to modify this task.')
        serializer.save()

    def perform_destroy(self, instance):
        ensure_role(instance.project, self.request.user, TASK_MANAGEMENT_ROLES, 'You do not have permissions to delete this task.')
        instance.delete()
