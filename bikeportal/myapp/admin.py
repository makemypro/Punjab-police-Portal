from django.contrib import admin
from .models import Shop, Product, mechanic, Rating, order_detail
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# Register your models here.
admin.site.register(Shop)
admin.site.register(mechanic)
admin.site.register(Rating)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id',)
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     username = request.user
    #     qs.shop = qs.filter(username = shop_user)
    #     print(qs)
    #     return qs
    def get_queryset(self, request):
        qs = super(ProductAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            print('a--------------->')
            return qs
        user = request.user
        shop = Shop.objects.filter(user = user)

        val = shop.values()
        for v in val:
            s = v.get('id')
        print(s)

        queryset = qs.filter(shop=s).all()
        return queryset
    
    # def save_model(self, request, obj, form, change):
    #     obj.shop = 1
    #     super().save_model(request, obj, form, change)

        # return qs.filter(author=request.user)

@admin.register(order_detail)
class order_detailAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_deliver', 'order_status','created_at']
    list_filter = ('created_at','deliver_date', 'is_approve','order_status')
    fieldsets = (
        ('Order Information', {
            'fields': ( 'order_id', 'items','total','is_approve','order_status','is_deliver')
        }),
        ('Shipping Detail',
            {
        'fields': ('first_name','last_name','email','phone_number', 'city', 'address','zip_code','deliver_date','user')
            }
        )
    )
    actions = ['Mark Delivered']
    @admin.action(description = "Mark as Deliver")
    def case_registeretd_today(self, request, queryset):
        queryset.update(is_deliver =True)  
    
    change_form_template = "admin/AdminAproval.html"
    def response_change(self, request, obj):
        if "_approve" in request.POST:
            obj.is_aprove = True
            obj.save()
            self.message_user(request, "Complain Approve successfully")
            return HttpResponseRedirect("../")
        return super().response_change(request, obj)