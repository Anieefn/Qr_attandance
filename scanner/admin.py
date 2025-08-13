from django.contrib import admin
from .models import Register,Report,Attendance

# Register your models here.
admin.site.register(Register)
admin.site.register(Report)
admin.site.register(Attendance)