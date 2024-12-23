from django.contrib import admin
from .models import News,Category, Contact

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title','category','published_time', 'status', 'id')
    list_filter = ('status', 'created_time', 'published_time')      # Filter qismi
    prepopulated_fields = {'slug': ('title',)}          # slugni title ga yozilgan narsa bilan avtomatik to'ldirish
    date_hierarchy = 'published_time'
    search_fields = ['title', 'body']
    ordering = ['status','-published_time']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

# admin.site.register(Contact)
@admin.register(Contact)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')