from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "phone",
            "image",
            "country",
        )
