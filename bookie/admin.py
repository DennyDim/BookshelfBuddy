from django.contrib import admin

from book import models as book_models
from author import models as author_models

from bookie import models as bookie_models

from Genre import models as category_models
from reviews import models as review_models
# Register your models here.


admin.site.register(book_models.Book, book_models.BookAdmin)


admin.site.register(author_models.Author)
admin.site.register(author_models.Country)


admin.site.register(bookie_models.Bookie, bookie_models.UserAdmin)
admin.site.register(bookie_models.BookieProfile)


admin.site.register(category_models.Genre)

admin.site.register(review_models.ReviewAndRating, review_models.ReviewAndRatingAdmin)
