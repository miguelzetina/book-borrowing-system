from rest_framework_json_api import serializers

from bookborrowing.users.models import User
from bookborrowing.users.related_fields import ResourceRelatedRoleField


class UserSerializer(serializers.ModelSerializer):

    role = ResourceRelatedRoleField(queryset=User.objects)

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'last_name',
            'second_last_name',
            'role'
        )