from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .models import User, Lead, Activity, Deal, Task
from .serializers import *
from .permissions import HasCustomPermission

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permissions = ["view_user"]

    def get_permissions(self):
        if self.request.method == "POST":
            self.required_permissions = ["add_user"]
        return [permission() for permission in self.permission_classes]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, HasCustomPermission]

    def get_permissions(self):
        if self.request.method == "GET":
            self.required_permissions = ["view_user"]
        elif self.request.method in ["PUT", "PATCH"]:
            self.required_permissions = ["change_user"]
        elif self.request.method == "DELETE":
            self.required_permissions = ["delete_user"]
        return [permission() for permission in self.permission_classes]



class LeadListCreateView(generics.ListCreateAPIView):
    queryset = Lead.objects.all().select_related('status', 'assigned_to')
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permissions = ["view_lead"]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'assigned_to']
    search_fields = ['name', 'interests', 'notes']
    ordering_fields = ['created_at', 'name']
    ordering = ['created_at']

    def get_permissions(self):
        if self.request.method == "POST":
            self.required_permissions = ["add_lead"]
        return [permission() for permission in self.permission_classes]
    def perform_create(self, serializer):
         serializer.save(created_by=self.request.user)

class LeadDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all().select_related('status', 'assigned_to')
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated, HasCustomPermission]

    def get_permissions(self):
        if self.request.method == "GET":
            self.required_permissions = ["view_lead"]
        elif self.request.method in ["PUT", "PATCH"]:
            self.required_permissions = ["change_lead"]
        elif self.request.method == "DELETE":
            self.required_permissions = ["delete_lead"]
        return [permission() for permission in self.permission_classes]



class ActivityListCreateView(generics.ListCreateAPIView):
    queryset = Activity.objects.all().select_related('activity_type', 'assigned_to')
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permissions = ["view_activity"]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['activity_type', 'assigned_to']
    search_fields = ['description', 'notes']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_permissions(self):
        if self.request.method == "POST":
            self.required_permissions = ["add_activity"]
        return [permission() for permission in self.permission_classes]
    
    def perform_create(self, serializer):
         serializer.save(created_by=self.request.user)


class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all().select_related('activity_type', 'assigned_to')
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated, HasCustomPermission]

    def get_permissions(self):
        if self.request.method == "GET":
            self.required_permissions = ["view_activity"]
        elif self.request.method in ["PUT", "PATCH"]:
            self.required_permissions = ["change_activity"]
        elif self.request.method == "DELETE":
            self.required_permissions = ["delete_activity"]
        return [permission() for permission in self.permission_classes]



class DealListCreateView(generics.ListCreateAPIView):
    queryset = Deal.objects.all().select_related('customer', 'stage', 'assigned_to')
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permissions = ["view_deal"]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['stage', 'customer', 'assigned_to']
    search_fields = ['title', 'customer__name']
    ordering_fields = ['expected_close_date', 'created_at']
    ordering = ['expected_close_date']

    def get_permissions(self):
        if self.request.method == "POST":
            self.required_permissions = ["add_deal"]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
         serializer.save(created_by=self.request.user)
         
         
class DealDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deal.objects.all().select_related('customer', 'stage', 'assigned_to')
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticated, HasCustomPermission]

    def get_permissions(self):
        if self.request.method == "GET":
            self.required_permissions = ["view_deal"]
        elif self.request.method in ["PUT", "PATCH"]:
            self.required_permissions = ["change_deal"]
        elif self.request.method == "DELETE":
            self.required_permissions = ["delete_deal"]
        return [permission() for permission in self.permission_classes]



class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all().select_related('status', 'assigned_to', 'created_by')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permissions = ["view_task"]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'assigned_to', 'created_by']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at']
    ordering = ['due_date']

    def get_permissions(self):
        if self.request.method == "POST":
            self.required_permissions = ["add_task"]
        return [permission() for permission in self.permission_classes]
    def perform_create(self, serializer):
         serializer.save(created_by=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all().select_related('status', 'assigned_to', 'created_by')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, HasCustomPermission]

    def get_permissions(self):
        if self.request.method == "GET":
            self.required_permissions = ["view_task"]
        elif self.request.method in ["PUT", "PATCH"]:
            self.required_permissions = ["change_task"]
        elif self.request.method == "DELETE":
            self.required_permissions = ["delete_task"]
        return [permission() for permission in self.permission_classes]

    

# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         user = authenticate(username=username, password=password)
#         if user is None:
#             return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

#         refresh = RefreshToken.for_user(user)
#         return Response({
#             "user": UserSerializer(user).data,
#             "refresh": str(refresh),
#             "access": str(refresh.access_token)
#         })
class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
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
        
class LeadStatusListCreateView(generics.ListCreateAPIView):
    queryset = LeadStatus.objects.all()
    serializer_class = LeadStatusSerializer
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permissions = {
        'GET': ['view_leadstatus'],
        'POST': ['add_leadstatus']
    }

class LeadStatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LeadStatus.objects.all()
    serializer_class = LeadStatusSerializer
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permissions = {
        'GET': ['view_leadstatus'],
        'PUT': ['change_leadstatus'],
        'PATCH': ['change_leadstatus'],
        'DELETE': ['delete_leadstatus']
    }
    
class DealStageListCreateView(generics.ListCreateAPIView):
    queryset = DealStage.objects.all()
    serializer_class = DealStageSerializer
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permissions = {
        'GET': ['view_dealstage'],
        'POST': ['add_dealstage']
    }

class DealStageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DealStage.objects.all()
    serializer_class = DealStageSerializer
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permissions = {
        'GET': ['view_dealstage'],
        'PUT': ['change_dealstage'],
        'PATCH': ['change_dealstage'],
        'DELETE': ['delete_dealstage']
    }
class TaskStatusListCreateView(generics.ListCreateAPIView):
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSerializer
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permissions = {
        'GET': ['view_taskstatus'],
        'POST': ['add_taskstatus']
    }

class TaskStatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSerializer
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permissions = {
        'GET': ['view_taskstatus'],
        'PUT': ['change_taskstatus'],
        'PATCH': ['change_taskstatus'],
        'DELETE': ['delete_taskstatus']
    }
from .permissions import IsLeadOwnerOrAdmin
class ContactInfoListCreateView(generics.ListCreateAPIView):
   
    serializer_class = ContactInfoSerializer
    permission_classes = [IsAuthenticated, IsLeadOwnerOrAdmin]
    
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['lead', 'contact_type', 'is_primary']
    search_fields = ['value', 'label']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return ContactInfo.objects.select_related('lead').all()
        
        return ContactInfo.objects.filter(lead__assigned_to=user)

    def perform_create(self, serializer):
       
        lead = serializer.validated_data.get('lead')
        user = self.request.user

        if not (user.is_superuser or lead.assigned_to == user or lead.created_by==user):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("This lead is neither created by you nor assigned to you")

        serializer.save()
    
class ContactInfoDetailView(generics.RetrieveUpdateDestroyAPIView):
   
    queryset = ContactInfo.objects.all().select_related('lead')
    serializer_class = ContactInfoSerializer
    permission_classes = [IsAuthenticated, IsLeadOwnerOrAdmin]

    def get_permissions(self):

        return [permission() for permission in self.permission_classes]
