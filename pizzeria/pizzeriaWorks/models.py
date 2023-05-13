from django.db import models
from django.contrib.auth.models import User


class PizzaType(models.Model):
    id = models.AutoField('ID', primary_key=True)
    name = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    id = models.AutoField('ID', primary_key=True)
    name = models.CharField('Название', max_length=50)
    price = models.IntegerField('Цена')
    img = models.ImageField('Изображение пиццы', upload_to='pizzaImages/')
    description = models.CharField('Описание', max_length=300)
    type_id = models.ForeignKey(PizzaType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilePic = models.ImageField('Изображение профиля', upload_to='images/')
    #pizzaRating = models.ManyToManyField(Pizza, through="PizzaRating")
    #basket = models.ManyToManyField(Pizza, through="Basket")
    def __str__(self):
        return self.user.username


class Basket(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pizza_id = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    count = models.IntegerField('Количество')


class PizzaRating(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pizza_id = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    rating = models.IntegerField('Рейтинг')

class Specifications(models.Model):
    pizza_id = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=100)
    description = models.CharField('Описание', max_length=300)