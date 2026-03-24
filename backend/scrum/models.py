from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    """
    Represents a main workspace or product being developed.
    A project contains multiple epics, sprints, and tasks.
    """
    name = models.CharField(
        max_length=255,
        help_text="The name of the project"
    )
    key = models.CharField(
        max_length=10,
        unique=True,
        help_text="A short, unique identifier for the project"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the project goals and scope"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_projects',
        help_text="The user who created or manages the project"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return f"{self.key} - {self.name}"


class Sprint(models.Model):
    """
    Represents a iteration (usually 1-4 weeks) during which a specific set of
    tasks is completed.
    """
    class SprintStatus(models.TextChoices):
        PLANNED = 'PLANNED', _('Planned')
        ACTIVE = 'ACTIVE', _('Active')
        COMPLETED = 'COMPLETED', _('Completed')

    name = models.CharField(
        max_length=100,
        help_text="Name of the sprint"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='sprints',
        help_text="The project this sprint belongs to"
    )
    goal = models.TextField(
        blank=True,
        help_text="The main objective to be achieved during this sprint"
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        help_text="The date when the sprint officially starts"
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="The date when the sprint is scheduled to end"
    )
    status = models.CharField(
        max_length=20,
        choices=SprintStatus.choices,
        default=SprintStatus.PLANNED,
        help_text="Current lifecycle state of the sprint"
    )

    class Meta:
        ordering = ['start_date', 'name']
        verbose_name = "Sprint"
        verbose_name_plural = "Sprints"

    def __str__(self):
        return f"{self.name} ({self.project.key})"


class Epic(models.Model):
    """
    Represents a large amount of work that can be broken down into a number of
    smaller tasks (stories).
    """
    class EpicStatus(models.TextChoices):
        TODO = 'TODO', _('To do')
        IN_PROGRESS = 'IN_PROGRESS', _('In progress')
        DONE = 'DONE', _('Done')

    name = models.CharField(
        max_length=255,
        help_text="A brief name summarizing the epic"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed explanation of the epic requirements and business value"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='epics',
        help_text="The project this epic belongs to"
    )
    status = models.CharField(
        max_length=20,
        choices=EpicStatus.choices,
        default=EpicStatus.TODO,
        help_text="Current progress status of the epic"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Epic"
        verbose_name_plural = "Epics"

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Represents a single unit of work in the Scrum.
    It can be a user story, a bug, or a general task.
    """
    class TaskType(models.TextChoices):
        STORY = 'STORY', _('User Story')
        TASK = 'TASK', _('Task')
        BUG = 'BUG', _('Bug')

    class TaskStatus(models.TextChoices):
        BACKLOG = 'BACKLOG', _('Backlog')
        TODO = 'TODO', _('To do')
        IN_PROGRESS = 'IN_PROGRESS', _('In progress')
        IN_REVIEW = 'IN_REVIEW', _('In review')
        DONE = 'DONE', _('Done')

    class TaskPriority(models.TextChoices):
        LOW = 'LOW', _('Low')
        MEDIUM = 'MEDIUM', _('Medium')
        HIGH = 'HIGH', _('High')
        CRITICAL = 'CRITICAL', _('Critical')

    title = models.CharField(
        max_length=255,
        help_text="A concise summary of the task"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description, acceptance criteria or steps to reproduce (for bugs)."
    )
    task_type = models.CharField(
        max_length=10,
        choices=TaskType.choices,
        default=TaskType.STORY,
        help_text="The nature of the work item"
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.BACKLOG,
        help_text="Current position in workflow"
    )
    priority = models.CharField(
        max_length=10,
        choices=TaskPriority.choices,
        default=TaskPriority.MEDIUM,
        help_text="Importance and urgency of the task"
    )
    story_points = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="An estimate of the effort required to implement this task"
    )

    # Relations
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        help_text="The project to which this task belongs"
    )
    epic = models.ForeignKey(
        Epic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks',
        help_text="Optional grouping into a larger group of related work (epic)"
    )
    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks',
        help_text="The sprint during which this task is planned to be executed"
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        help_text="The user responsible for completing the task"
    )
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reported_tasks',
        help_text="The user who created or reported this task"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return f"[{self.project.key}-{self.pk}] {self.title}"


class Comment(models.Model):
    """
    Represents a discussion point or an update note attached to a specific task.
    """
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The task this comment belongs to"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='task_comments',
        help_text="The user who wrote the comment"
    )
    content = models.TextField(
        help_text="The body of the comment"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the comment was posted"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the comment was last edited"
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"
