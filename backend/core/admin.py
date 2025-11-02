from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "status", "created_at")
    list_filter = ("status", "created_at", "author")
    search_fields = ("title", "content", "author__username", "author__email")
    autocomplete_fields = ("author",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    actions = ("approve_posts", "deny_posts")

    @admin.action(description="Approve selected blog posts")
    def approve_posts(self, request, queryset):
        updated = queryset.update(status=Blog.Status.APPROVED)
        self.message_user(request, f"Approved {updated} post(s).")

    @admin.action(description="Deny selected blog posts")
    def deny_posts(self, request, queryset):
        updated = queryset.update(status=Blog.Status.DENIED)
        self.message_user(request, f"Denied {updated} post(s).")
