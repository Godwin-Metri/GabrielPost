from django.contrib import admin
from .models import BlogModel, CommentModel, AddBlogModel

admin.site.register(BlogModel)
admin.site.register(CommentModel)
admin.site.register(AddBlogModel)
# admin.site.register(LikesModel)
