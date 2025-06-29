from django.contrib import admin
from backoffice_engine.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Logo)
admin.site.register(Plan)
admin.site.register(Category)
admin.site.register(Suggested_prompt)
admin.site.register(Subscription)
admin.site.register(Feedback)