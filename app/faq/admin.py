from django.contrib import admin

from .models import FAQ, AboutUs, Question, UsefulLinks


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "email")
    readonly_fields = ("text", "name", "email")


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ("char",)


@admin.register(UsefulLinks)
class UsefulLinksAdmin(admin.ModelAdmin):
    list_display = ("url",)
