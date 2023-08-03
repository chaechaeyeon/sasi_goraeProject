from rest_framework import permissions
from .models import Message

#게시글 생성 사용자만 해당 편지를 수정하거나 삭제할 수 있도록 권한 제어 
class IsAuthorOrReadOnly(permissions.BasePermission): 
    def has_object_permission(self, request, view, obj):
        # 읽기 권한 모두 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 요청자 확인
        return obj.writer == request.user
    

#게시글 받은 사람만 해당 편지를 삭제할 수 있는 권한, 수정은 불가능 
class IsReceiverOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        
        if request.method in ['PUT', 'PATCH']:
            return False
        
        if isinstance(obj, Message):
            return obj.receiver  == request.user
        
        return True