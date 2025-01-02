from django.contrib import admin
from .models import News,Category, Contact, Comment

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

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'created_time', 'active')
    list_filter = ('active', 'created_time')
    search_fields = ['user', 'body']
    actions = ['disable_comment', 'activate_comment']
    def disable_comments(self, request, queryset):
        queryset.update(active=False)

    def active_comments(self, request, queryset):
        queryset.update(active=True)

# admin.site.register(Comment, CommentAdmin)