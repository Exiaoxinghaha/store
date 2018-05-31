from django.contrib import admin
from account.models import UserProfile,ReceiverAddress

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username','email']
    search_fields = ['username','email']

@admin.register(ReceiverAddress)
class ReceiverAddressAdmin(admin.ModelAdmin):
    list_display = ['receiver_name','receiver_telephone','receiver_city']
    search_fields = ['receiver_name']

