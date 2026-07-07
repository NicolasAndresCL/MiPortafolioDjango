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
    logo = models.ImageField(upload_to="skills/logos/", blank=True, null=True)  # Nuevo campo

    def __str__(self):
        return self.name

class Experience(models.Model):
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    location = models.CharField(max_length=150, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)  # None = "Actualidad"
    summary = models.TextField()
    technologies = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    @property
    def is_current(self):
        return self.end_date is None

    def __str__(self):
        return f"{self.role} @ {self.company}"

class ExperienceHighlight(models.Model):
    experience = models.ForeignKey(Experience, related_name='highlights', on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.text[:50]
