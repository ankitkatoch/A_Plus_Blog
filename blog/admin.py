from django.contrib import admin
from .models import BlogModel
# Register your models here.

admin.site.register(BlogModel)


# class BlogModelAdmin(admin.ModelAdmin):
#     list_display = ('title', 'slug', 'created_on')
#     search_fields = ['title', 'description']
#     prepopulated_fields = {'slug': ('title',)}
#
#
# admin.site.register(BlogModel, BlogModelAdmin)
