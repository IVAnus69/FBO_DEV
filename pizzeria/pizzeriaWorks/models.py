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
    isAlive = models.BooleanField(default=True)




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilePic = models.ImageField('Изображение профиля', upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Basket(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pizza_id = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    count = models.IntegerField('Количество')

    def sum(self):
        return self.pizza_id.price * self.count


class PizzaRating(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pizza_id = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    rating = models.IntegerField('Рейтинг')


class Specifications(models.Model):
    pizza_id = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=100)
    description = models.CharField('Описание', max_length=300)

    def __str__(self):
        return self.pizza_id.name + ": " + self.description


class Order(models.Model):
    id = models.AutoField('ID', primary_key=True)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def sum(self):
        order_items = Order_Item.objects.filter(order_id=self)
        s = 0
        for order_item in order_items:
            s += order_item.pizza_id.price
        return s

class Order_Item(models.Model):
    pizza_id = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    count = models.IntegerField('Количество')

    def sum(self):
        return self.count * self.pizza_id.price

