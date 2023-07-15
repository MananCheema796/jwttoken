from django.contrib import admin
from .models import CustomUser
from .models import Student
# Register your models here.


admin.site.register(CustomUser)

@admin.register(Student)

class StudentAdmin(admin.ModelAdmin):
    list_display=['id', 'name', 'roll', 'city']