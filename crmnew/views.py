from django.shortcuts import render
from rest_framework.permissions import AllowAny
# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics,status
from .models import User, Lead, Activity, Deal, Task
from .serializers import *
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from .permissions import AuthDocPermission

class UserListView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserCreateView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    required_permissions =[]
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.permissions import DjangoModelPermissions

class LeadListView(APIView):
    permission_classes = [IsAuthenticated, AuthDocPermission]
    required_permissions = ["crm.view_lead"]

    def get(self, request):
        leads = Lead.objects.select_related('status', 'assigned_to')
        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data)

    def post(self, request):
        self.required_permissions = ["crm.add_lead"]
        serializer = LeadSerializer(data=request.data)
        if serializer.is_valid():
            lead = serializer.save()
            return Response(LeadSerializer(lead).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeadDetailView(APIView):
    permission_classes = [IsAuthenticated, AuthDocPermission]

    def get(self, request, pk):
        self.required_permissions = ["crm.view_lead"]
        lead = get_object_or_404(Lead, pk=pk)
        return Response(LeadSerializer(lead).data)

    def put(self, request, pk):
        self.required_permissions = ["crm.change_lead"]
        lead = get_object_or_404(Lead, pk=pk)
        serializer = LeadSerializer(lead, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.required_permissions = ["crm.delete_lead"]
        lead = get_object_or_404(Lead, pk=pk)
        lead.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ActivityListView(APIView):
    permission_classes = [IsAuthenticated, AuthDocPermission]
    required_permissions = ["crm.view_activity"]

    def get(self, request):
        activities = Activity.objects.select_related('activity_type', 'assigned_to')
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    def post(self, request):
        self.required_permissions = ["crm.add_activity"]
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            activity = serializer.save()
            return Response(ActivitySerializer(activity).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivityDetailView(APIView):
    permission_classes = [IsAuthenticated, AuthDocPermission]

    def get(self, request, pk):
        self.required_permissions = ["crm.view_activity"]
        activity = get_object_or_404(Activity, pk=pk)
        return Response(ActivitySerializer(activity).data)

    def put(self, request, pk):
        self.required_permissions = ["crm.change_activity"]
        activity = get_object_or_404(Activity, pk=pk)
        serializer = ActivitySerializer(activity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.required_permissions = ["crm.delete_activity"]
        activity = get_object_or_404(Activity, pk=pk)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class DealListView(APIView):
    permission_classes = [IsAuthenticated, AuthDocPermission]
    required_permissions = ["crm.view_deal"]

    def get(self, request):
        deals = Deal.objects.select_related('customer', 'stage', 'assigned_to')
        serializer = DealSerializer(deals, many=True)
        return Response(serializer.data)

    def post(self, request):
        self.required_permissions = ["crm.add_deal"]
        serializer = DealSerializer(data=request.data)
        if serializer.is_valid():
            deal = serializer.save()
            return Response(DealSerializer(deal).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DealDetailView(APIView):
    permission_classes = [IsAuthenticated, AuthDocPermission]

    def get(self, request, pk):
        self.required_permissions = ["crm.view_deal"]
        deal = get_object_or_404(Deal, pk=pk)
        return Response(DealSerializer(deal).data)

    def put(self, request, pk):
        self.required_permissions = ["crm.change_deal"]
        deal = get_object_or_404(Deal, pk=pk)
        serializer = DealSerializer(deal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.required_permissions = ["crm.delete_deal"]
        deal = get_object_or_404(Deal, pk=pk)
        deal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class TaskListView(APIView):
    permission_classes = [IsAuthenticated, AuthDocPermission]
    required_permissions = ["crm.view_task"]

    def get(self, request):
        tasks = Task.objects.select_related('status', 'assigned_to', 'created_by')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        self.required_permissions = ["crm.add_task"]
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated, AuthDocPermission]

    def get(self, request, pk):
        self.required_permissions = ["crm.view_task"]
        task = get_object_or_404(Task, pk=pk)
        return Response(TaskSerializer(task).data)

    def put(self, request, pk):
        self.required_permissions = ["crm.change_task"]
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.required_permissions = ["crm.delete_task"]
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"detail": "Invalid credentials"}, status=400)

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": access_token,
        }, status=status.HTTP_201_CREATED)
