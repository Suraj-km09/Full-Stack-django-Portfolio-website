# main/models.py
from django.db import models
from django_resized import ResizedImageField
from django.core.mail import send_mail
from django.conf import settings

class SingleActiveModel(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.is_active:
            # Deactivate all others of the same model
            self.__class__.objects.exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)

class HeaderTitle(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class HeroSection(models.Model):
    title = models.CharField(max_length=200, default="Suraj")
    subtitle = models.CharField(max_length=200)
    image = ResizedImageField(size=[500, 500], upload_to='hero/', force_format='WEBP', quality=90, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Counter data
    projects_count = models.PositiveIntegerField(default=42)
    clients_count = models.PositiveIntegerField(default=28)
    experience_count = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.title

class Quote(models.Model):
    text = models.TextField()
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.text[:50] + "..." if len(self.text) > 50 else self.text

class AboutSection(models.Model):
    SECTION_TYPE_CHOICES = [
        ('background', 'Background'),
        ('philosophy', 'Philosophy'),
        ('focus', 'Current Focus'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    section_type = models.CharField(max_length=20, choices=SECTION_TYPE_CHOICES)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.section_type}: {self.title}"

class TimelineItem(models.Model):
    TIMELINE_CATEGORY = [
        ('education', 'Education'),
        ('career', 'Career'),
        ('future', 'Future Plans'),
    ]
    
    title = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=TIMELINE_CATEGORY)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.category}: {self.title}"

class Skill(models.Model):
    name = models.CharField(max_length=100)
    proficiency = models.PositiveIntegerField(default=80)  # Percentage
    icon_class = models.CharField(max_length=50, default='fas fa-code')
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.name

class Certificate(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    description = models.TextField()
    image = ResizedImageField(size=[400, 300], upload_to='certificates/', force_format='WEBP', quality=90)
    issue_date = models.DateField(blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    demo_link = models.URLField(blank=True)
    github_link = models.URLField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = ResizedImageField(size=[600, 400], upload_to='projects/', force_format='WEBP', quality=90)
    alt_text = models.CharField(max_length=200)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.project.title} - {self.alt_text}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name}"

    def save(self, *args, **kwargs):
        # Only send email when creating a new message (not when updating)
        is_new = self._state.adding
        
        super().save(*args, **kwargs)
        
        # Send email notification when a new message is received
        if is_new and hasattr(settings, 'CONTACT_EMAIL'):
            try:
                send_mail(
                    subject=f"New message from {self.name}",
                    message=f"Name: {self.name}\nEmail: {self.email}\n\nMessage:\n{self.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,  # Set to True to avoid errors if email isn't configured
                )
            except:
                # Silently fail if email sending doesn't work
                pass

class ContactInfo(models.Model):
    title = models.CharField(max_length=100, default="Get In Touch")
    description = models.TextField(default="I'm currently available for freelance work and interesting projects. Feel free to reach out!")
    email = models.EmailField(default="surajkumar.sm09@gmail.com")
    address = models.CharField(max_length=255, default="Lucknow, Mohanlalganj")

    def __str__(self):
        return self.title            
    

class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter/X'),
        ('codepen', 'CodePen'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        # add more as needed
    ]
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon_class = models.CharField(max_length=100, help_text="e.g., fab fa-github")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.platform} ({'Active' if self.is_active else 'Inactive'})"    