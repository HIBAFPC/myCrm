# serializers.py
from rest_framework import serializers
from .models import *

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    user_type = UserTypeSerializer(read_only=True)
    user_type_id = serializers.PrimaryKeyRelatedField(
        queryset=UserType.objects.all(), source='user_type', write_only=True, required=False
    )
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type', 'user_type_id','password']
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    activity_type = ActivityTypeSerializer(read_only=True)
    activity_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ActivityType.objects.all(), source='activity_type', write_only=True
    )
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assigned_to', write_only=True, required=False
    )

    class Meta:
        model = Activity
        fields = [
            'id', 'title', 'assigned_to', 'assigned_to_id',
            'activity_type', 'activity_type_id', 'notes',
            'scheduled_for', 'completed', 'created_at', 'updated_at'
        ]


class LeadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadStatus 
        fields = '__all__'

class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = '__all__'

class LeadSerializer(serializers.ModelSerializer):
    status = LeadStatusSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=LeadStatus.objects.all(), source='status', write_only=True, required=False
    )
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assigned_to', write_only=True, required=False
    )
    contact_infos = ContactInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Lead
        fields = [
            'id', 'name', 'qualification', 'interests', 'status',
            'status_id', 'assigned_to', 'assigned_to_id',
            'notes', 'next_followup', 'created_at', 'updated_at', 'contact_infos'
        ]


class DealStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealStage
        fields = '__all__'

class DealSerializer(serializers.ModelSerializer):
    stage = DealStageSerializer(read_only=True)
    stage_id = serializers.PrimaryKeyRelatedField(
        queryset=DealStage.objects.all(), source='stage', write_only=True, required=False
    )
    customer = LeadSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Lead.objects.all(), source='customer', write_only=True
    )
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assigned_to', write_only=True, required=False
    )

    class Meta:
        model = Deal
        fields = [
            'id', 'title', 'customer', 'customer_id',
            'stage', 'stage_id', 'expected_close_date',
            'assigned_to', 'assigned_to_id', 'created_at', 'updated_at'
        ]


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    
    status = TaskStatusSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=TaskStatus.objects.all(), source='status', write_only=True, required=False
    )
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='created_by', write_only=True, required=False
    )
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assigned_to', write_only=True, required=False
    )

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'created_by', 'created_by_id',
            'assigned_to', 'assigned_to_id', 'activity', 'status',
            'status_id', 'priority', 'due_date', 'depends_on',
            'created_at', 'updated_at'
        ]



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
