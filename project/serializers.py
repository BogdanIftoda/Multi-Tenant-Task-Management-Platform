from rest_framework import serializers

from project.models import Project, Task, Label
from tenant.models import User
from tenant.serializers import UserReadSerializer


class BaseProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("title", "description", "end_date", "start_date", "priority", "status", "organization")


class ProjectWriteSerializer(BaseProjectSerializer):
    workers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )

    def validate_workers(self, value):
        """
            Ensure that all users assigned to the project belong to the same organization
            as the current authenticated user.
       """
        user = self.context['request'].user
        organization = user.organization
        # Check if all users in the 'assigned_to' field belong to the same organization
        for worker in value:
            if worker.organization != organization:
                raise serializers.ValidationError(
                    f"User {worker.username} does not belong to your organization."
                )
        return value

    class Meta(BaseProjectSerializer.Meta):
        fields = BaseProjectSerializer.Meta.fields + ("workers",)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['creator_id'] = user.id
        return super().create(validated_data)


class ProjectReadSerializer(BaseProjectSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    workers = UserReadSerializer(many=True, read_only=True)
    status = serializers.ReadOnlyField(source='get_status_display')
    priority = serializers.ReadOnlyField(source='get_priority_display')

    class Meta(BaseProjectSerializer.Meta):
        fields = BaseProjectSerializer.Meta.fields + ("creator", "workers")


class BaseTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("title", "description", "priority", "status", "start_date", "end_date", "project", "labels")


class TaskReadSerializer(BaseTaskSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    assigned_to = UserReadSerializer(many=True, read_only=True)
    status = serializers.ReadOnlyField(source='get_status_display')
    priority = serializers.ReadOnlyField(source='get_priority_display')

    class Meta(BaseTaskSerializer.Meta):
        fields = BaseTaskSerializer.Meta.fields + ("creator", "assigned_to")


class TaskWriteSerializer(BaseTaskSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), allow_null=True, allow_empty=True
    )

    class Meta(BaseTaskSerializer.Meta):
        fields = BaseTaskSerializer.Meta.fields + ("assigned_to",)

    @staticmethod
    def contains(project_workers, assigned_to):
        return all(elem in project_workers for elem in assigned_to)

    def validate(self, data):
        user = self.context['request'].user
        organization = user.organization
        assigned_to = data.get('assigned_to', [])

        for assigned_user in assigned_to:
            if assigned_user.organization != organization:
                raise serializers.ValidationError(
                    f"User {assigned_user.username} does not belong to your organization."
                )

        # handle update
        if self.instance:
            if not self.contains(self.instance.project.workers.all(), assigned_to):
                raise serializers.ValidationError(
                    "Not all members works on the project"
                )
        else:
            project = data.get('project')
            if not self.contains(project.workers.all(), assigned_to):
                raise serializers.ValidationError(
                    "Not all members works on the project"
                )

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['creator_id'] = user.id
        return super().create(validated_data)


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'
