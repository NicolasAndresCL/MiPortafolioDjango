from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    github_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)
    technologies = models.CharField(max_length=255) # Ej: "Python, Django, React, DRF"
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=5) # Nivel de 1 a 10, o porcentaje
    category = models.CharField(max_length=100, blank=True, null=True) # Ej: "Backend", "Frontend", "Database"

    def __str__(self):
        return self.name
