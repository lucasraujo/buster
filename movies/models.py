from django.db import models


class RatingChoices(models.TextChoices):
    G = "G"
    PG = "PG"
    PG13 = "PG-13"
    R = "R"
    NC17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, default=None)
    rating = models.CharField(
        max_length=20, choices=RatingChoices.choices, default=RatingChoices.G
    )
    synopsis = models.TextField(blank=True, default=None, null=True)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="movies"
    )

    users_ords = models.ManyToManyField(
        "users.User",
        through="movies.MovieOrder",
        related_name="movies_ords"
    )


class MovieOrder(models.Model):
    movies_orders = models.ForeignKey("movies.Movie", on_delete=models.CASCADE)
    users_ordes = models.ForeignKey("users.User", on_delete=models.CASCADE)
    buyed_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
