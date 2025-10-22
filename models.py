from django.db import models
from django.contrib.auth.models import User

class TODO(models.Model):
    status_choices = [
        ('C', 'COMPLETED'),
        ('P', 'PENDING'),
    ]

    priority_choices = [
        ('1', '①'), ('2', '②'), ('3', '③'), ('4', '④'), ('5', '⑤'),
        ('6', '⑥'), ('7', '⑦'), ('8', '⑧'), ('9', '⑨'), ('10','⑩'),
    ]

    category_choices = [
        ('Personal', 'Personal'),
        ('Work', 'Work'),
        ('Study', 'Study'),
        ('Shopping', 'Shopping'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)              # new
    due_date = models.DateField(null=True, blank=True)      # new
    status = models.CharField(max_length=2, choices=status_choices, default='P')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)  # new (when completed)
    priority = models.CharField(max_length=2, choices=priority_choices, default='5')
    category = models.CharField(max_length=30, choices=category_choices, default='Other')  # new

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
