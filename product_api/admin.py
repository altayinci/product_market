from .models import Product, DeliveryOptions
from django import forms
from django.contrib import admin


class ProductAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'price', 'description', 'currency', 'seller_id', 'in_stock', 'last_updated_on')
    list_filter = ('name', 'price', 'currency', 'seller_id', 'in_stock', 'last_updated_on')
    search_fields = ('name',)
    readonly_fields = ['last_updated_on']
    save_as = True

    fieldsets = (
        ('General', {
            'fields': ('name', 'price', 'description', 'currency', 'seller_id', 'in_stock', 'last_updated_on')
        }),
    )

    def save_model(self, request, obj, form, change):
        result = super(ProductAdmin, self).save_model(request, obj, form,
                                                             change)

        return result


class DeliveryOptionsAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DeliveryOptionsAdminForm, self).__init__(*args, **kwargs)


class DeliveryOptionsAdmin(admin.ModelAdmin):
    form = DeliveryOptionsAdminForm
    list_display = ('name', 'price', 'currency', 'product')
    list_filter = ('name', 'price', 'currency', 'product')
    search_fields = ('name',)
    readonly_fields = []
    save_as = True

    fieldsets = (
        ('General', {
            'fields': ('name', 'price', 'currency', 'product')
        }),
    )

    def save_model(self, request, obj, form, change):
        result = super(DeliveryOptionsAdmin, self).save_model(request, obj, form,
                                                             change)

        return result


admin.site.register(Product, ProductAdmin)
admin.site.register(DeliveryOptions, DeliveryOptionsAdmin)
