from rest_framework import serializers
from core.utils.exception_utils import AppExceptionHelper, AppValidateException
from modules.client.models import Client

class ClientGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "CPF",
            "email",
            "company_id",
            "phone",
            "tier",
            "created_at",
            "updated_at"
        ]
        
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        
    def validate(self, attrs):
        return super().validate(attrs) 
    
    
class ClientUpdateSerializer(serializers.ModelSerializer, AppExceptionHelper):
    CLIENT_TIER = [('basic', 'Basic'), ('premium', 'Premium')]
    name = serializers.CharField(max_length=200, required=False)
    CPF = serializers.CharField(max_length=250)
    email = serializers.EmailField(max_length=250)
    company_id = serializers.IntegerField()
    phone = serializers.CharField(max_length=20)
    tier = serializers.CharField(required=True)
    
    class Meta:
        model = Client
        fields = "__all__"
        
    
    def validate_tier(self, tier):
        if tier not in ["basic", "premium"]:
            self.raise_serializer_validate_exception(
                field="tier",
                exception=f"validate client failed! client tier: {tier} not match",
                exception_type="Client"
            )
            
            
    def validate(self, attrs):
        name = attrs.get('name')
        self.handle_char_validator(attrs=name, field='name', max_length=250, exception_type=self.Meta.model.__name__)
        