from django.db import models


class GoodsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class Goods(models.Model):
    objects = GoodsManager()
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    cost = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name='Стоимость', default=0)

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()
