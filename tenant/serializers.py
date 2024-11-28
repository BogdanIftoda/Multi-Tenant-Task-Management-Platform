from rest_framework import serializers

from tenant.models import Organization, User


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class UserBaseSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.get_name_display', read_only=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "organization", "role")


class UserWriteSerializer(UserBaseSerializer):
    class Meta(UserBaseSerializer.Meta):
        model = User
        fields = UserBaseSerializer.Meta.fields + ("password",)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserReadSerializer(UserBaseSerializer):
    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + ("id",)
