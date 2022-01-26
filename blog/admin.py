from django.contrib import admin
from .models import Profile, Post, Contact


admin.site.register(Profile)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'view_count')
    prepopulated_fields = {"slug": ("title",)}
    
admin.site.register(Post, PostAdmin)
admin.site.register(Contact)
