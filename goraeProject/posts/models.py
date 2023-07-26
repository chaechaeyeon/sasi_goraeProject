from django.db import models
from django.contrib.auth.models import User

class Post(models.Model) :
    content = models.TextField()
    image = models.ImageField(null=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writer') #보내는사람
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='received_user')
    points = models.IntegerField(default=0) #포인트 필드
    def __str__(self) :
        return self.id


class UserInfo(models.Model) :
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    # 닉네임
    nickname = models.CharField(max_length=14)
    # 프로필 사진 
    profile = models.ImageField()
    point = models.IntegerField(null=True)
    # 칭찬 메시지 받을 때마다 카운트
    count = models.IntegerField(null=True)


    def __str__(self):
        return self.user.username 
