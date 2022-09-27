from distutils.command.upload import upload
import email
from email.headerregistry import Address
from email.policy import default
from multiprocessing import context
from unicodedata import name
from xml.dom import ValidationErr
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from requests import request
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

cat = (
    ('motor cycle','motor cycle'),
    ('spare parts', 'spare parts'),
    ('electronic parts','electronic parts'),
    ('tyre','tyre')
)
cc_choice = (
    ('70','70'),
    ('100', '100'),
    ('125','125'),
    ('150','150'),
    ('200','200'),
    ('250','250'),
)
# def get_shop(self, request):
#     s = Shop.objects.get(user__username=request.user)
#     return s 
# Create your models here.
class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    shop_no = models.IntegerField()
    address = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner')
    
    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    price = models.FloatField()
    image = models.FileField(upload_to = 'static/images',validators=[FileExtensionValidator (allowed_extensions=['png','jpg'])], default="")
    company = models.CharField(max_length=50, default = None)
    category = models.CharField(choices=cat,max_length=50)
    bike_color = models.CharField(max_length=20, default="red")
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE, related_name='shop', blank=True, null=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        def __init__(self):
            self.shop = Shop.name
            print(self.shop)
    # @classmethod
    # def get_shop(cls,request = None):
    #     username = request.user
    #     cls.shop = User.Shop
    #     return cls.objects.filter(shop__owner=username)
        
    # def __init__(self, *args, **kwargs):
    #     super(Product, self).__init__(*args, **kwargs)
    #     self.username=kwargs.get("request").user.username
        
    #     return self.objects.filter(shop_user_username=self.username)
    # def save(self,*args,**kwargs):
        
    #     super(Product,self).save(request,*args,**kwargs)
    # def get_shop(self, request):
    #     return Shop.objects.get(user__username=request.user) 
    def update_quantity(self, qty=None, product_id=None):
        self.quantity = self.quantity - qty
        if self.quantity ==0:
            self.availability = False
        return self.quantity




city_choice = (('lahore','lahore'), ('Karachi','Karachi'),('Faislbad', 'Faislbad'))

class mechanic(models.Model):
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=13)
    address = models.CharField(max_length=255)
    city = models.CharField(choices=city_choice, max_length=50)
    lat = models.DecimalField(max_digits=12,decimal_places=9)
    lang = models.DecimalField(max_digits=12,decimal_places=9)

    def __str__(self):
        return self.name

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    review = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    rating = models.IntegerField()
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

from django.template.loader import render_to_string
class order_detail(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_id = models.CharField(max_length=20,null=True, blank=True)
    items = models.JSONField(default=dict)
    total = models.FloatField(default=None, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    is_approve = models.BooleanField(default=False)
    order_status = models.CharField(max_length=20,choices=(('Cancel','Cancel'),('Pending','Pending'),('Deliver','Deliver')), default="Pending")
    first_name = models.CharField(max_length=30, null=True, blank=True, default=None)
    last_name = models.CharField(max_length=30, default=None)
    email = models.EmailField(blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=13, blank=False, default=None)
    address = models.CharField(max_length=150, default=" ")
    city = models.CharField(choices=city_choice, max_length=50, default=None)
    delivery_instruction = models.CharField(max_length=250, blank=True, null=True)
    deliver_date = models.DateField(null=True, blank=True)
    is_deliver = models.BooleanField(default=False, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.order_id

    @classmethod
    def send_mail(cls, sender, context):
        message = render_to_string('myapp/order_msg.html',context=context)
        msg = EmailMessage(
        'Order Detail',
        message,
        'f2018105044@umt.edu.pk',
        [sender],
    )
        msg.content_subtype ="html/txt"# Main content is now text/html
        msg.send(fail_silently=True)

    
    

    
