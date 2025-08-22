# main/admin.py
from django.contrib import admin
from .models import HeaderTitle, HeroSection, Quote, AboutSection, TimelineItem, Skill, Certificate, Project, ProjectImage, ContactMessage, ContactInfo, SocialLink
from django.utils.html import format_html

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

# Base class for models WITH display_order
class OrderedBaseAdmin(admin.ModelAdmin):
    list_display = ("__str__", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    list_filter = ("is_active",)
    ordering = ("display_order",)

# Base class for models WITHOUT display_order
class SimpleBaseAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)

@admin.register(HeaderTitle)
class HeaderTitleAdmin(SimpleBaseAdmin):
    list_display = ['title', 'subtitle', 'is_active']
    list_editable = ('is_active',)

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'image_preview', 'is_active')
    list_editable = ('is_active',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:cover; border-radius:8px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Hero Image"

@admin.register(Quote)
class QuoteAdmin(OrderedBaseAdmin):
    list_display = ['text_preview', 'display_order', 'is_active']
    list_editable = ('is_active', 'display_order')
    
    def text_preview(self, obj):
        return obj.text[:75] + "..." if len(obj.text) > 75 else obj.text
    text_preview.short_description = 'Quote'

@admin.register(AboutSection)
class AboutSectionAdmin(OrderedBaseAdmin):
    list_display = ['title', 'section_type', 'content_preview', 'display_order', 'is_active']
    list_editable = ('is_active',)
    
    def content_preview(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(TimelineItem)
class TimelineItemAdmin(OrderedBaseAdmin):
    list_display = ['title', 'category', 'period', 'display_order', 'is_active']
    list_editable = ('is_active',)

@admin.register(Skill)
class SkillAdmin(OrderedBaseAdmin):
    list_display = ['name', 'proficiency', 'icon_class', 'display_order', 'is_active']
    list_editable = ['proficiency', 'display_order', 'is_active']

@admin.register(Certificate)
class CertificateAdmin(OrderedBaseAdmin):
    list_display = ['title', 'issuer', 'issue_date', 'display_order', 'is_active']
    list_filter = ['is_active', 'issue_date']
    date_hierarchy = 'issue_date'
    list_editable = ('is_active',)

@admin.register(Project)
class ProjectAdmin(OrderedBaseAdmin):
    list_display = ['title', 'display_order', 'is_active']
    inlines = [ProjectImageInline]
    search_fields = ['title', 'description']
    list_editable = ('is_active',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'is_read']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'message', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    date_hierarchy = 'created_at'
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'email', 'address']
    
    def has_add_permission(self, request):
        # Allow only one ContactInfo instance
        return not ContactInfo.objects.exists()
    
@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url")    