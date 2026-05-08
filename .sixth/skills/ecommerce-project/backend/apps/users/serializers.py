from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
	name = serializers.CharField(source="username", read_only=True)

	class Meta:
		model = User
		fields = ("id", "name", "email", "role", "is_verified")


class RegisterSerializer(serializers.ModelSerializer):
	name = serializers.CharField(write_only=True)
	password = serializers.CharField(write_only=True, min_length=6)

	class Meta:
		model = User
		fields = ("name", "email", "password", "role")

	# create new user
	def create(self, validated_data):
		name = validated_data.pop("name")
		password = validated_data.pop("password")
		role = validated_data.get("role", User.Roles.CUSTOMER)

		user = User(
			username=name,
			email=validated_data["email"],
			role=role,
			is_verified=True,
		)
		# hash password before saving
		user.set_password(password)
		user.save()
		return user


class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(write_only=True)

	# check login credentials
	def validate(self, attrs):
		email = attrs.get("email")
		password = attrs.get("password")

		user = authenticate(email=email, password=password)
		if not user:
			raise serializers.ValidationError("Invalid email or password.")

		attrs["user"] = user
		return attrs
