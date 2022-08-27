from django.contrib import admin
from . models import postmodel,Like,Comment


class frushgahmodeladmin (admin.ModelAdmin):
     pass

admin.site.register(postmodel, frushgahmodeladmin)
admin.site.register(Like)
admin.site.register(Comment)


