from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from hub.models import Project
from .serializers import ProjectSerializer
from .permissions import IsOwnerOrReadOnly

class ProjectListCreateAPIView(generics.ListCreateAPIView):

    queryset = Project.objects.all().order_by("-created")
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    search_fields = [
        "title",
        "description",
        "owner__username",
        "tags__name",
    ]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ["owner", "tags"]

    ordering_fields = ["created", "title"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProjectDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self,pk):
        obj=get_object_or_404(Project,pk=pk)
        self.check_object_permissions(self.request,obj)
        return obj
    
    def get(self,request,pk):
        projects=self.get_object(pk)
        serializer=ProjectSerializer(projects)
        return Response(serializer.data)
    
    def patch(self,request,pk):
        projects=self.get_object(pk)
        serializer=ProjectSerializer(projects,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors,status=400)
    
    def put(self,request,pk):
        projects=self.get_object(pk)
        serializer=ProjectSerializer(projects,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors,status=400)
    
    def delete(self,request,pk):
        projects=self.get_object(pk)
        projects.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class MyProjectsAPIView(generics.ListAPIView):

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user).order_by("-created")

