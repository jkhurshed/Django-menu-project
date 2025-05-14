from django.db import models
from django.urls import reverse


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    menu_name = models.CharField(max_length=100, help_text="Identifier for the menu this item belongs to")
    url = models.CharField(max_length=255, blank=True)
    named_url = models.CharField(max_length=100, blank=True, help_text="Named URL (takes precedence over URL if both are specified)")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['menu_name']),
        ]

    def __str__(self):
        return self.name

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except:
                return self.url
        return self.url 