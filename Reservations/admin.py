from django.contrib import admin

from Reservations.models import *


class BranchAdmin(admin.ModelAdmin):
    list_display = ['place', 'manager']
    list_display_links = ['place']
    search_fields = ['place', 'manager']
    list_filter = ['place', 'manager']

    class Meta:
        model = Branch


admin.site.register(Branch, BranchAdmin)


class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'isReserved', 'isActive', 'buyingDate']
    list_display_links = ['brand', 'model', 'isReserved', 'isActive', 'buyingDate']
    list_filter = ['brand', 'model', 'isReserved', 'isActive', 'buyingDate']
    search_fields = ['brand', 'model', 'isReserved', 'isActive', 'buyingDate']

    class Meta:
        model = Car


admin.site.register(Car, CarAdmin)


class ReservationsAdmin(admin.ModelAdmin):
    list_display = ['receiveDate', 'deliveryDate', 'buyer', 'car', 'reservationDate']
    list_display_links = ['receiveDate', 'deliveryDate', 'buyer', 'car', 'reservationDate']
    search_fields = ['receiveDate', 'deliveryDate', 'buyer', 'car', 'reservationDate']
    list_filter = ['receiveDate', 'deliveryDate', 'buyer', 'car', 'reservationDate']

    class Meta:
        model = Reservations


admin.site.register(Reservations, ReservationsAdmin)
admin.site.register(Visitor)

