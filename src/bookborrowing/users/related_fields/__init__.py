from collections import OrderedDict

from rest_framework_json_api.relations import ResourceRelatedField


class ResourceRelatedRoleField(ResourceRelatedField):

    def to_representation(self, value):
        return OrderedDict([
            ('id', str(value.pk)),
            ('name', value.name),
        ])
