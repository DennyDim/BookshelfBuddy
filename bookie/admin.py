from django.contrib import admin

from book import models as book_models
from author import models as author_models

from bookie import models as bookie_models
from comment import models as comment_models

from category import models as category_models
from reviews import models as review_models
# Register your models here.


admin.site.register(book_models.Book)
admin.site.register(author_models.Author)


admin.site.register(bookie_models.Bookie)
admin.site.register(bookie_models.BookieProfile)

admin.site.register(comment_models.Comment)

admin.site.register(category_models.Category)

admin.site.register(review_models.ReviewAndRating)
