from django.conf import settings
from django.db import models
from django.utils.timezone import now
from mdeditor.fields import MDTextField


class LinkShowType(models.TextChoices):
    """
    链接展示类型
    """
    I = ('i', '首页')
    L = ('l', '列表页')
    P = ('p', '文章页面')
    A = ('a', '全站')
    S = ('s', '友情链接页面')


class BaseModel(models.Model):
    """
    抽象基类
    """
    id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)

    class Meta:
        abstract = True  # 表明这是一个抽象基类，不会创建任何数据表


class Article(BaseModel):
    """
    文章-模型类
    """
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
    COMMENT_CHOICES = (
        ('o', '打开'),
        ('c', '关闭'),
    )
    TYPE = (
        ('a', '文章'),
        ('p', '页面'),
    )
    title = models.CharField('标题', max_length=200, unique=True)
    body = MDTextField('正文')
    pub_time = models.DateTimeField(
        '发布时间', blank=True, null=True, default=now)
    status = models.CharField(
        '文章状态', 
        max_length=1, 
        choices=STATUS_CHOICES, 
        default='p')
    comment_status = models.CharField(
        '评论状态', 
        max_length=1, 
        choices=COMMENT_CHOICES,
        default='o')
    type = models.CharField('类型', max_length=1, choices=TYPE, default='a')
    views = models.PositiveIntegerField('浏览量', default=0)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='作者',
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    article_order = models.IntegerField(
        '排序, 数字越大越靠前', blank=False, null=False, default=0)
    show_toc = models.BooleanField('是否显示toc目录', blank=False, null=False, default=False)
    category = models.ForeignKey(
        'Category',
        verbose_name='分类',
        on_delete=models.CASCADE,
        blank=False,
        null=False)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)

    class Meta:
        ordering = ['-article_order', '-pub_time']  # 用于获取对象列表时的默认排序
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        get_latest_by = 'id'  # last(), 返回查询集中的最后一个对象

class Category(BaseModel):
    """
    文章分类
    """
    name = models.CharField('分类名', max_length=30, unique=True)
    parent_category = models.ForeignKey(
        'self', 
        verbose_name="父级分类", 
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)
    index = models.IntegerField(default=0, verbose_name='权重排序-越大越靠前')

    class Meta:
        ordering = ['-index']
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Tag(BaseModel):
    """
    文章标签
    """
    name = models.CharField('标签名', max_length=30, unique=True)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Links(models.Model):
    """
    友情链接
    """
    name = models.CharField('链接名称', max_length=30, unique=True)
    link = models.URLField('链接地址')
    sequence = models.IntegerField('排序', unique=True)
    is_enable = models.BooleanField(
        '是否显示', default=True, blank=True, null=True)
    show_type = models.CharField(
        '显示类型',
        max_length=1,
        choices=LinkShowType.choices,
        default=LinkShowType.I)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)

    class Meta:
        ordering = ['sequence']
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name


class SideBar(models.Model):
    """
    侧边栏，可以展示一些html内容
    """
    name = models.CharField('标题', max_length=100)
    content = models.TextField('内容')
    sequence = models.IntegerField('排序', unique=True)
    is_enable = models.BooleanField('是否启用', default=True)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)

    class Meta:
        ordering = ['sequence']
        verbose_name = '侧边栏'
        verbose_name_plural = verbose_name
    

class BlogSetting(models.Model):
    """
    博客设置-模型类
    """
    sitename = models.CharField(
        '网站名称',
        max_length=200,
        null=False,
        blank=False,
        default='')
    site_description = models.TextField(
        '网站描述',
        max_length=1000,
        null=False,
        blank=False,
        default='')
    site_seo_description = models.TextField(
        '网站SEO描述',
        max_length=1000,
        null=False,
        blank=False,
        default='')
    site_keywords = models.TextField(
        '网站关键字',
        max_length=1000,
        null=False,
        blank=False,
        default='')
    article_sub_length = models.IntegerField('文章摘要长度', default=300)
    sidebar_article_count = models.IntegerField('侧边栏文章数目', default=10)
    sidebar_comment_count = models.IntegerField('侧边栏评论数目', default=5)
    show_google_adsense = models.BooleanField('是否显示谷歌广告', default=False)
    google_adsense_codes = models.TextField(
        '广告内容', max_length=2000, null=True, blank=True, default='')
    open_site_comment = models.BooleanField('是否打开网站评论功能', default=True)
    beiancode = models.CharField(
        '备案号',
        max_length=2000,
        null=True,
        blank=True,
        default='')
    analyticscode = models.TextField(
        '网站统计代码',
        max_length=1000,
        null=False,
        blank=False,
        default='')
    show_gongan_code = models.BooleanField(
        '是否显示公安备案号', default=False, null=False)
    gongan_beiancode = models.TextField(
        '公安备案号',
        max_length=2000,
        null=True,
        blank=True,
        default='')
    resource_path = models.CharField(
        '静态文件保存地址',
        max_length=300,
        null=False,
        default='/var/www/resource/')
    
    class Meta:
        verbose_name = '网站配置'
        verbose_name_plural = verbose_name
