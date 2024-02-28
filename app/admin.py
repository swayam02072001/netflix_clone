from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header='Netfilx Clone || Admin'
admin.site.register(Movie)
admin.site.register(Movielist)
admin.site.register(Genre)