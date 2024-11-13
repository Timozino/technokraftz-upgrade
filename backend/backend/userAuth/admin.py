from django.contrib import admin

from . models import CustomUser, Profile

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username", "fullName", "email"]
    list_filter = ["username", "fullName", "email"]
   # search_fields = ["username", "fullName", "email"]
    list_per_page = 20
    readonly_fields = ["email"]
   # ordering=["fullName", -"date"]

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "fullName", "country"]
    list_filter = ["user", "fullName", "country"]
   # search_fields = ["user", "fullName", "country"]
    list_per_page = 20
    readonly_fields = ["bio"]
    ordering=["fullName"]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)


