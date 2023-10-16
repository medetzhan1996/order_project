from rest_framework import serializers

from accounts.models import CustomUser
from .utils import is_valid_phone_number, calculate_age


class BaseCustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'phone', 'password', 'date_of_birth', 'profile_photo']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
        }

    def validate_date_of_birth(self, value):
        """
        Проверка даты рождения на соответствие возрастному ограничению.
        """
        if calculate_age(value) < 18:
            raise serializers.ValidationError('Users under 18 are not allowed to register.')
        return value

    def set_user_password(self, user, validated_data):
        password = validated_data.pop('password', None)
        if password:
            user.set_password(password)
            user.save()


class CustomUserSerializer(BaseCustomUserSerializer):
    age = serializers.SerializerMethodField()

    class Meta(BaseCustomUserSerializer.Meta):
        model = CustomUser  # Добавьте атрибут model с указанием модели
        fields = ['id', 'phone', 'password', 'date_of_birth', 'age', 'profile_photo']

    def get_age(self, obj):
        return calculate_age(obj.date_of_birth)


class CustomUserCreateSerializer(BaseCustomUserSerializer):

    def validate_phone(self, phone):
        """
        Проверка корректности номера телефона.
        """
        if not is_valid_phone_number(phone):
            raise serializers.ValidationError(
                'Invalid phone number format. Expected format: +7 XXX XXX XX XX'
            )
        return phone

    def create(self, validated_data):
        user = super().create(validated_data)
        self.set_user_password(user, validated_data)
        return user


class CustomUserUpdateSerializer(BaseCustomUserSerializer):
    class Meta(BaseCustomUserSerializer.Meta):
        read_only_fields = ['phone']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8, 'required': False},
        }

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        self.set_user_password(user, validated_data)
        return user

