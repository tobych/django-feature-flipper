from django.contrib import admin

from featureflipper.models import Feature


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'status')

    def enable_features(self, request, queryset):
        for feature in queryset:
            feature.enable()
            feature.save()
        self.message_user(request, "Successfully enabled %d features." % len(queryset))
    enable_features.short_description = "Enable selected features"

    def disable_features(self, request, queryset):
        for feature in queryset:
            feature.disable()
            feature.save()
        self.message_user(request, "Successfully disabled %d features." % len(queryset))
    disable_features.short_description = "Disable selected features"

    def flip_features(self, request, queryset):
        for feature in queryset:
            feature.flip()
            feature.save()
        self.message_user(request, "Successfully flipped %d features." % len(queryset))
    flip_features.short_description = "Flip selected features"

    actions = [enable_features, disable_features, flip_features]

admin.site.register(Feature, FeatureAdmin)
