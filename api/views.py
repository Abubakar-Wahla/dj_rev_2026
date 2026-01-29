from rest_framework.decorators import api_view
from rest_framework.response import Response
from hub.models import Project  # adjust name
from .serializers import ProjectSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@api_view(["GET"])
def get_routes(request):
    routes = [
        {"GET": "/api/"},
        {"GET": "/api/projects/"},
        {"GET": "/api/projects/<id>/"},
    ]
    return Response(routes)

@api_view(["GET", "POST",])
def projects_list(request):
    projects = Project.objects.all()
    
    if request.method == "GET":
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ProjectSerializer(projects,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET","PATCH","PUT","DELETE"])
def project_detail(request, pk):

    project = get_object_or_404(Project, pk=pk)

    if request.method=="GET":
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    if request.method in ["PUT","PATCH"]:
        partial = (request.method=="PATCH")
        serializer=ProjectSerializer(project,data=request.data,partial=partial)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    if request.method =="DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)