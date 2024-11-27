from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, SubCategory, Content, Comment
from .serializers import CategorySerializer, SubCategorySerializer, ContentSerializer, CommentSerializer

category_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Category name'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='Category description', nullable=True),
    },
    required=['name'],  
)

category_update_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Updated category name'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='Updated category description', nullable=True),
    },
    required=['name'],  
)

subcategory_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'sub': openapi.Schema(type=openapi.TYPE_STRING, description='SubCategory name'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='SubCategory description', nullable=True),
        'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
    },
    required=['sub', 'category'],  
)

subcategory_update_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'sub': openapi.Schema(type=openapi.TYPE_STRING, description='Updated SubCategory name'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='Updated SubCategory description', nullable=True),
        'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated Category ID'),
    },
    required=['sub', 'category'],  
)
content_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='Content title'),
        'image': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_BINARY, description='Content image'),
        'content': openapi.Schema(type=openapi.TYPE_STRING, description='Content body'),
        'author': openapi.Schema(type=openapi.TYPE_STRING, description='Author name', nullable=True),
        'active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is content active?'),
        'subcategory': openapi.Schema(type=openapi.TYPE_INTEGER, description='SubCategory ID'),
        'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID', nullable=True),
    },
    required=['title', 'content', 'subcategory'],
)

content_update_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='Updated Content title'),
        'image': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_BINARY, description='Updated Content image'),
        'content': openapi.Schema(type=openapi.TYPE_STRING, description='Updated Content body'),
        'author': openapi.Schema(type=openapi.TYPE_STRING, description='Updated Author name', nullable=True),
        'active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is content active?'),
        'subcategory': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated SubCategory ID'),
        'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated Category ID', nullable=True),
    },
    required=['title', 'content', 'subcategory'],
)



@swagger_auto_schema(
    method='post',
    request_body=category_request_body,
    responses={201: CategorySerializer, 400: "Invalid input"}
)
@swagger_auto_schema(
    method='get',
    responses={200: CategorySerializer(many=True)}
)
@api_view(['GET', 'POST'])
def category_view(request):
    
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    responses={200: CategorySerializer, 404: "Category not found"}
)
@swagger_auto_schema(
    method='put',
    request_body=category_update_body,
    responses={200: CategorySerializer, 400: "Invalid input", 404: "Category not found"}
)
@swagger_auto_schema(
    method='delete',
    responses={204: "Deleted successfully", 404: "Category not found"}
)
@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response({'message': 'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method='post',
    request_body=subcategory_request_body,
    responses={201: SubCategorySerializer, 400: "Invalid input"}
)
@swagger_auto_schema(
    method='get',
    responses={200: SubCategorySerializer(many=True)}
)
@api_view(['GET', 'POST'])
def subcategory_view(request):
    
    if request.method == 'GET':
        subcategories = SubCategory.objects.all()
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    responses={200: SubCategorySerializer, 404: "SubCategory not found"}
)
@swagger_auto_schema(
    method='put',
    request_body=subcategory_update_body,
    responses={200: SubCategorySerializer, 400: "Invalid input", 404: "SubCategory not found"}
)
@swagger_auto_schema(
    method='delete',
    responses={204: "Deleted successfully", 404: "SubCategory not found"}
)
@api_view(['GET', 'PUT', 'DELETE'])
def subcategory_detail(request, pk):
    try:
        subcategory = SubCategory.objects.get(pk=pk)
    except SubCategory.DoesNotExist:
        return Response({'error': 'SubCategory not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubCategorySerializer(subcategory)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = SubCategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        subcategory.delete()
        return Response({'message': 'SubCategory deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(
    method='get',
    responses={200: ContentSerializer, 404: "Content not found"}
)
@swagger_auto_schema(
    method='put',
    request_body=content_update_body,
    responses={200: ContentSerializer, 400: "Invalid input", 404: "Content not found"}
)
@swagger_auto_schema(
    method='delete',
    responses={204: "Deleted successfully", 404: "Content not found"}
)
@api_view(['GET', 'PUT', 'DELETE'])
def content_detail(request, pk):
    try:
        content = Content.objects.get(pk=pk)
    except Content.DoesNotExist:
        return Response({'error': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ContentSerializer(content)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ContentSerializer(content, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        content.delete()
        return Response({'message': 'Content deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method='post',
    request_body=ContentSerializer,
    responses={201: ContentSerializer, 400: "Invalid input"}
)
@api_view(['POST'])
def content_create_by_subcategory(request):
    serializer = ContentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    responses={200: CommentSerializer(many=True), 404: "Content not found"}
)
@swagger_auto_schema(
    method='post',
    request_body=CommentSerializer,
    responses={201: CommentSerializer, 400: "Invalid input"}
)
@api_view(['GET', 'POST'])
def add_comment(request, content_id):
    try:
        content = Content.objects.get(id=content_id)
    except Content.DoesNotExist:
        return Response({'detail': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        comments = content.comments.all()  
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = request.data.copy()
        data['content'] = content.id  
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@swagger_auto_schema(
    method='get',
    responses={200: CommentSerializer, 404: "Comment not found"}
)
@swagger_auto_schema(
    method='put',
    request_body=CommentSerializer,
    responses={200: CommentSerializer, 400: "Invalid input", 404: "Comment not found"}
)
@swagger_auto_schema(
    method='delete',
    responses={204: "Comment deleted successfully", 404: "Comment not found"}
)
@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, id):
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        content_id = request.data.get('content_id')  
        if content_id:
            try:
                content = Content.objects.get(id=content_id)
                comment.content = content  
            except Content.DoesNotExist:
                return Response({'error': 'Content not found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    elif request.method == 'DELETE':
        comment.delete()
        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)