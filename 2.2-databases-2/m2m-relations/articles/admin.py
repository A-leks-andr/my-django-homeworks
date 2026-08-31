from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_tags_count = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                if form.cleaned_data.get('is_main'):
                    main_tags_count += 1

        if main_tags_count == 0:
            raise ValidationError('Укажите основной раздел!')
        elif main_tags_count > 1:
            raise ValidationError('Основным может быть только один раздел!')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass