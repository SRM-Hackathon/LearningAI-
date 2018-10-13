from datetime import timedelta

from django.db import models
from django.utils import timezone

from mixins import TimeStampMixin
from user.models import Team, PlatformUser, TeamMembership


class Course(TimeStampMixin):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)

    instructor = models.ForeignKey(TeamMembership, on_delete=models.PROTECT, related_name="instructing_courses")
    students = models.ManyToManyField(TeamMembership, related_name="courses")
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'team')


class Tag(TimeStampMixin):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'name')


class Assessment(TimeStampMixin):
    # validation : Only subset of course tags should be present

    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    scheduled_at = models.DateTimeField()

    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag)
    created_by = models.ForeignKey(TeamMembership, on_delete=models.PROTECT)


    class Meta:
        unique_together = ('course', 'name')


class Task(TimeStampMixin):

    TODO = "TODO"
    IN_PROGRESS = "INP"
    COMPLETED = "CP"

    STATE_CHOICES = (
        (TODO, "TODO"),
        (IN_PROGRESS, "IN_PROGRESS"),
        (COMPLETED, "COMPLETED")
    )

    name = models.CharField(max_length=100)
    state = models.CharField(max_length=5, choices=STATE_CHOICES, default=TODO)
    description = models.TextField(blank=True, null=True)
    progress = models.PositiveIntegerField(default=0)
    eta = models.DateTimeField(default=timezone.now() + timedelta(hours=1))
    
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    student = models.ForeignKey(TeamMembership, on_delete=models.PROTECT)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def upgrade_state(self):

        if self.state == Task.COMPLETED:
            return None

        elif self.state == Task.TODO:
            self.state = Task.IN_PROGRESS
            state = "In Progress"

        else:
            self.state = Task.COMPLETED
            state = "Completed"

        self.save()
        return state

    class Meta:
        unique_together = ('name', 'assessment', 'student')


class UserEnvironment(TimeStampMixin):

    user = models.OneToOneField(TeamMembership, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, null=True, blank=True, on_delete=models.PROTECT)
    tag = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.PROTECT)


class UserSession(TimeStampMixin):
    BREAK_TERMINATION = "BR"
    NORMAL_TERMINATION = "NOR"

    TERMINATION_TYPE_CHOICES = (
        (BREAK_TERMINATION, "BREAK"),
        (NORMAL_TERMINATION, "NORMAL"),
    )

    is_master = models.BooleanField(default=False)
    termination_type = models.CharField(max_length=5, choices=TERMINATION_TYPE_CHOICES, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)

    user = models.ForeignKey(TeamMembership, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class Doubts(TimeStampMixin):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_clarified = models.BooleanField(default=False)

    user = models.ForeignKey(TeamMembership, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)


class DoubtsClarified(TimeStampMixin):
    clarified_response = models.TextField()
    is_clarified = models.BigAutoField(default=False)

    cleared_by = models.ForeignKey(TeamMembership, on_delete=models.PROTECT)
    doubt = models.ForeignKey(Doubts, on_delete=models.CASCADE)
