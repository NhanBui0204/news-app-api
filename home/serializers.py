from rest_framework import serializers
from .models import Category, SubCategory, Content, Comment, User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__' 

class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  
    class Meta:
        model = SubCategory
        fields = ['sub', 'description', 'category']


class ContentSerializer(serializers.ModelSerializer):
    subcategory_id = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all(),
        source='subcategory',
        write_only=True
    )
    
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category', 
        write_only=True
    )

    image_url = serializers.URLField(required=False, allow_null=True)
    image_file = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Content
        fields = [
            'id',
            'title',
            'image_url',  
            'image_file',
            'content',
            'author',
            'created_date',
            'updated_date',
            'active',
            'subcategory_id',
            'category_id',
        ]

    def validate(self, data):
        image_url = data.get('image_url')
        image_file = data.get('image_file')

        if image_url and image_file:
            raise serializers.ValidationError("Chỉ được cung cấp một trong hai: image_url hoặc image_file.")
        
        if not image_url and not image_file:
            raise serializers.ValidationError("Cần phải cung cấp ít nhất một trong hai: image_url hoặc image_file.")

        return data
    
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['id', 'title', 'author', 'created_date']
    
    def validate(self, data):
        if self.instance is None and not data.get('content'):
            raise serializers.ValidationError("Cần chọn một content hợp lệ cho comment.")
        return data

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

