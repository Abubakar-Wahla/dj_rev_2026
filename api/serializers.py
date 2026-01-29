from rest_framework import serializers
from hub.models import Project,Tag 
from django.contrib.auth.models import User 

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields=["id","name"]

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username"]

    

class ProjectSerializer(serializers.ModelSerializer):

    owner=OwnerSerializer(read_only=True)
    tags=TagsSerializer(many=True,read_only=True)

    tag_ids=serializers.PrimaryKeyRelatedField(
        source="tags",
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        required=False,

    )
    class Meta:
        model = Project
        fields =["id", "title", "description", "created", "owner", "tags", "tag_ids"]
        read_only_fields = ["id", "created", "owner", "tags"]

