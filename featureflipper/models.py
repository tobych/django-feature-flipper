from django.db import models

class Feature(models.Model):

    name = models.SlugField(max_length=40, db_index=True,
        help_text="Required. Used in templates (eg {% feature search %}) and URL parameters.")
    description = models.TextField(max_length=400, blank=True)
    enabled = models.BooleanField(default=False)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def flip(self):
        self.enabled = not self.enabled

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        
    @property
    def status(self):
        return "Enabled" if self.enabled else "Disabled"
