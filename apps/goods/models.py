from django.db import models


from DjangoUeditor.models import UEditorField
# Create your models here.


class GoodsCategory(models.Model):
    """
    用来描述商品类别
    """
    CATEGORY_TYPE=(
        (1,'一级类目'),
        (2,'二级类目'),
        (3,'三级类目')
    )
    name=models.CharField(max_length=30,verbose_name="类别名",help_text="类别名")
    code=models.CharField(max_length=30,verbose_name="类别code",help_text="类别code")#商品类别的一个编码
    desc=models.TextField(verbose_name="类别描述",help_text="类别描述")#商品类别的一个简单描述
    category_type=models.IntegerField(choices=CATEGORY_TYPE,null=True,blank=True,verbose_name="类目级别",help_text="类目级别")#描述商品时属于哪个类别，是一级类别到三级类别的哪一个
    parent_category=models.ForeignKey('self',null=True,blank=True,verbose_name='父类别',on_delete=models.CASCADE,help_text="类别",related_name="sub_cat")#该外键用来指向自己，这样便可以分成多个级别
    is_table=models.BooleanField(default=False,verbose_name="是否导航",help_text="是否导航")#确定商品类别是否要放到导航栏
    add_time=models.DateTimeField(auto_now_add=True,verbose_name="添加时间",help_text="添加时间")#添加时间
    class Meta:
        verbose_name="商品类别"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    商品的品牌名
    """
    category=models.ForeignKey(GoodsCategory,on_delete=models.CASCADE,related_name="brands",null=True,blank=True,verbose_name="种类")
    name=models.CharField(max_length=30,verbose_name="品牌名",help_text="品牌名")
    desc=models.TextField(verbose_name="品牌描述",help_text="品牌描述")
    image=models.ImageField(max_length=200,upload_to="brand/")
    add_time=models.DateTimeField(auto_now_add=True,verbose_name="添加时间")
    class Meta:
        verbose_name="品牌名"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name


class Goods(models.Model):
    category=models.ForeignKey(GoodsCategory,on_delete=models.CASCADE,verbose_name="商品类目")#商品类别
    name=models.CharField(max_length=30,verbose_name="商品名称",help_text="商品名称")
    goods_sn=models.CharField(max_length=30,verbose_name="商品编码",help_text="商品编码")
    click_num=models.IntegerField(default=0,verbose_name="点击量",help_text="点击量")#商品点击数
    sold_num=models.IntegerField(default=0,verbose_name="商品售卖量",help_text="销售量")#商品卖出的数量
    fav_num=models.IntegerField(default=0,verbose_name="商品收藏量")#商品的收藏数
    goods_num=models.IntegerField(default=0,verbose_name="商品库存量")#商品的库存数量
    market_price=models.FloatField(default=0,verbose_name="市场价格")#商品的市场价格
    shop_price=models.FloatField(default=0,verbose_name="网站价格")#目前购物网站的商品价格
    goods_desc=UEditorField(verbose_name="内容",imagePath="goods/images/",width=1000,height=1000,filePath="goods/files",default="")#商品简介
    goods_brief=models.TextField(verbose_name="简介",default="")
    ship_free=models.BooleanField(default=False)#该商品是否免运费
    goods_front_image=models.ImageField(upload_to="goods/images",max_length=300)#商品封面图
    is_new=models.BooleanField(default=False,verbose_name="是否为新品")#商品是否为新产品
    is_hot=models.BooleanField(default=False,verbose_name="是否热卖",help_text="是否热卖")#是否为热卖商品
    add_time=models.DateTimeField(auto_now_add=True,verbose_name="添加时间")#商品添加时间
    class Meta:
        verbose_name="商品"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name


class GoodsImage(models.Model):#因为一个商品可能有多个种类，所以需要定义一个商品图片的类
    """
    商品轮播图
    """
    goods=models.ForeignKey(Goods,on_delete=models.CASCADE,related_name="images",verbose_name="商品")
    images=models.ImageField(upload_to="",verbose_name="图片",max_length=300)
    add_time=models.DateTimeField(auto_now_add=True,verbose_name="添加时间")
    class Meta:
        verbose_name="图片"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.goods.name


class Bananer(models.Model):#这是首页用来轮播的图片
    """轮播图片"""
    goods=models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name="商品")
    index=models.IntegerField(default=1,verbose_name="轮播顺序")
    image=models.ImageField(upload_to="bananer",verbose_name="轮播图片",max_length=200)
    class Meta:
        verbose_name="轮播图片"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.goods.name