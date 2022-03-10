from django.shortcuts import render
from django.http.response import JsonResponse
from django.utils import timezone

import logging.config
import logging
from gcinside.settings import DEFAULT_LOGGING

from .serializers import PostSerializer
from .models import Post

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logging.config.dictConfig(DEFAULT_LOGGING)
# Create your views here.
class UploadPostView(APIView):
    @swagger_auto_schema(
        request_body=PostSerializer,
        manual_parameters=[openapi.Parameter('header_test', openapi.IN_HEADER, description="a header for  test", type=openapi.TYPE_STRING)]
    )
    @permission_classes(IsAuthenticated, )
    def post(self, request):
        if request.user.is_authenticated:
            serializer = PostSerializer(
                data = {
                    'author' : request.user.id,
                    'title' : request.POST['title'],
                    'content' : request.POST['content'],
                    'image' : request.FILES.get('image', None),
                    'created_at' : timezone.now(),
                }
            )

            if (serializer.is_valid()):
                serializer.save()

                return JsonResponse({'message' : 'Post success'}, status=201)
            return JsonResponse({'message' : 'Bad request'}, status=400)
        else :
            return JsonResponse({'message' : 'auth error'}, status=401)

class UpdatePostView(APIView):
    @swagger_auto_schema(request_body=PostSerializer)
    @permission_classes(IsAuthenticated, )
    def put(self, request, pk):
        if request.user.is_authenticated:
            posting = Post.objects.get(id=pk)

            if posting.author == request.user:

                serializer = PostSerializer(
                    posting,
                    data = {
                        'author' : request.user.id,
                        'title' : request.POST['title'],
                        'content' : request.POST['content'],
                        'image' : request.FILES.get('image', None),
                        'created_at' : timezone.now(),
                    }
                )
    
                if serializer.is_valid():
                    serializer.save()
    
                    return JsonResponse({'message' : 'Update success'}, status=201)
                return JsonResponse({'message' : 'Bad request'}, status=400)
            else :
                return JsonResponse({'message' : 'different user'}, status=401)
        else :
            return JsonResponse({'message' : 'auth error'}, status=401)

class DeletePostView(APIView):
    @swagger_auto_schema(request_body=PostSerializer)
    @permission_classes(IsAuthenticated, )
    def delete(self, request, pk):
        if request.user.is_authenticated:
            posting = Post.objects.get(id=pk)

            if posting.author == request.user:
                posting.delete()

                return JsonResponse({'message' : 'Delete success'}, status=200)
            return JsonResponse({'message' : 'different user'}, status=401)
        else :
            return JsonResponse({'message' : 'auth error'}, status=401)