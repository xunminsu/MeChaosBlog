from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class BlogUser(AbstractUser):
    """
    自定义用户，需要中 settings 中指明。
    """
    nickname = models.CharField('昵称', max_length=100, blank=True)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', max_length=100, blank=True)
    source = models.CharField('创建来源', max_length=100, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    def __str__(self):
        return self.email
