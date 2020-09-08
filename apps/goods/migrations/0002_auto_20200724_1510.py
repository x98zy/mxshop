# Generated by Django 3.0.7 on 2020-07-24 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='click_num',
            field=models.IntegerField(default=0, help_text='点击量', verbose_name='点击量'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='is_hot',
            field=models.BooleanField(default=False, help_text='是否热卖', verbose_name='是否热卖'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='sold_num',
            field=models.IntegerField(default=0, help_text='销售量', verbose_name='商品售卖量'),
        ),
        migrations.AlterField(
            model_name='goodscategory',
            name='category_type',
            field=models.IntegerField(blank=True, choices=[(1, '一级类目'), (2, '二级类目'), (3, '三级类目')], help_text='类目级别', max_length=10, null=True, verbose_name='类目级别'),
        ),
        migrations.AlterField(
            model_name='goodscategorybrand',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brands', to='goods.GoodsCategory', verbose_name='种类'),
        ),
    ]
