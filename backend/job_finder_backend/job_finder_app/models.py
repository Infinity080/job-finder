from django.db import models

class Website(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Specialization(models.Model):
    name = models.CharField(max_length=255,null=False, blank=False)

    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='specializations', default=1)

    def __str__(self):
        return f"{self.name} from {self.website.name}"
# Not currently used
class Listing(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)

    title = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    raw_text = models.TextField()

    job_roles = models.JSONField(null=True, blank=True)
    education = models.JSONField(null=True, blank=True)
    skills = models.JSONField(null=True, blank=True)
    experience_level = models.CharField(max_length=64, null=True, blank=True)
    employment_type = models.JSONField(null=True, blank=True)

    date_scraped = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title or 'Listing'} at {self.company or 'Unknown'}"
