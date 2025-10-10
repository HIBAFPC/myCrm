from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import User, Lead, Activity, Deal, Task
from .serializers import *

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LeadListCreateView(generics.ListCreateAPIView):
    queryset = Lead.objects.all().select_related('status', 'assigned_to')
    serializer_class = LeadSerializer

class LeadDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all().select_related('status', 'assigned_to')
    serializer_class = LeadSerializer



class ActivityListCreateView(generics.ListCreateAPIView):
    queryset = Activity.objects.all().select_related('activity_type', 'assigned_to')
    serializer_class = ActivitySerializer

class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all().select_related('activity_type', 'assigned_to')
    serializer_class = ActivitySerializer



class DealListCreateView(generics.ListCreateAPIView):
    queryset = Deal.objects.all().select_related('customer', 'stage', 'assigned_to')
    serializer_class = DealSerializer

class DealDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deal.objects.all().select_related('customer', 'stage', 'assigned_to')
    serializer_class = DealSerializer



class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all().select_related('status', 'assigned_to', 'created_by')
    serializer_class = TaskSerializer

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all().select_related('status', 'assigned_to', 'created_by')
    serializer_class = TaskSerializer
