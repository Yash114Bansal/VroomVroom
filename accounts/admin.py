from django.contrib import admin
from import_export.admin import ImportExportMixin
from import_export import resources
from .models import UserProfile

# Initializing base class for import/export data from admin panel
class BaseImportExportAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

class UserProfileResource(resources.ModelResource):
    class Meta:
        model = UserProfile
        exclude = ('id', 'last_login', 'is_superuser', 'groups', 'user_permissions')
        import_id_fields=("email",)

@admin.register(UserProfile)
class UserProfileAdmin(BaseImportExportAdmin):
    list_display = ("name","email")
    fields = (
        "name",
        "email",
        "phone_number",
        "password", 
        "profile_picture",
        "email_verified",
        "phone_verified",
        "verified_driver",
        "age",
        "gender",
        "subscribed_to_email",
        "fcm_token"
    )
    resource_class = UserProfileResource

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(form.cleaned_data["password"])

        super().save_model(request, obj, form, change)
