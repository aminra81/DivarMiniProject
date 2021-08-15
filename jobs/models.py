from django.contrib import admin
from django.db import models
from django.shortcuts import get_object_or_404

from authentication.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator

from django.utils.translation import gettext_lazy as _



class EducationalLevel(models.TextChoices):
    DIPLOMA = 'DI', _('High School Diploma')
    ASSOCIATE = 'A', _('Associate Degree')
    BACHELORS_DEGREE = 'B', _('Bachelors Degree')
    MASTERS_DEGREE = 'M', _('Masters Degree')
    DOCTORAL_DEGREE = 'DO', _('Doctoral Degree')
    POSTDOCTORAL_DEGREE = 'P', _('Post Doctoral Degree')
    OTHERS = 'O', _('Others')


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(blank=True)
    logo = models.ImageField(upload_to='images', blank=True)
    description = models.TextField(blank=True)
    link = models.URLField(max_length=200)
    telephone_number = models.CharField(max_length=12)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Skill(models.Model):
    """
    Each skills consists of a title.
    UserProfile has ManyToMany relationship with fields.
    """
    title = models.CharField(max_length=80, primary_key=True)

    def __str__(self):
        return self.title


class JobOffer(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    salary = models.IntegerField(blank=True, null=True)
    minimum_work_experience = models.IntegerField(default=0)
    CHOICES_TIME = [
        ('full_time', 'full time'),
        ('part_time', 'part time'),
    ]

    type_of_cooperation = models.CharField(choices=CHOICES_TIME, max_length=10)
    minimum_degree = models.CharField(max_length=2, choices=EducationalLevel.choices, null=True, blank=True)
    skills_required = models.ManyToManyField(Skill, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    """
    UserProfile model, first_name & last_name of users are stored in CustomUser,
    other personal fields are stored here.
    """

    class MilitaryServiceStatus(models.TextChoices):
        CONSCRIPT = 'CO', _('Conscript')
        EDUCATIONAL_EXEMPTION = 'EE', _('Educational Exemption')
        EXEMPT = 'E', _('Exempt')
        DISCHARGE = 'D', _('Discharge')

    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHERS = 'O', _('Other')

    class MaritalStatus(models.TextChoices):
        SINGLE = 'S', _('Single')
        MARRIED = 'M', _('Married')

        # WIDOWED = 'W', _('Widowed')
        # DIVORCED = 'D', _('Divorced')
        # SEPARATED = 'S', _('Separated')

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    mobile_number = models.CharField(max_length=11, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    address = models.CharField(max_length=280, blank=True, null=True)
    military_service_status = models.CharField(max_length=2,
                                               choices=MilitaryServiceStatus.choices,
                                               blank=True, null=True
                                               )
    gender = models.CharField(max_length=1,
                              choices=Gender.choices,
                              blank=True, null=True
                              )
    marital_status = models.CharField(max_length=1,
                                      choices=MaritalStatus.choices,
                                      blank=True, null=True
                                      )
    city_of_residence = models.CharField(max_length=80, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return str(self.user) + " Profile"


class EducationalBackground(models.Model):
    """
    Each UserProfile can have multiple EducationalBackground instances (OneToMany relationship).
    """
    MIN_YEAR = 1300
    MAX_YEAR = 1450

    field = models.CharField(max_length=80)
    institute = models.CharField(max_length=80)
    level = models.CharField(max_length=2,
                             choices=EducationalLevel.choices)
    start_year = models.IntegerField(validators=[MinValueValidator(MIN_YEAR),
                                                 MaxValueValidator(MAX_YEAR)])
    finish_year = models.IntegerField(validators=[MinValueValidator(MIN_YEAR),
                                                  MaxValueValidator(MAX_YEAR)])

    is_currently_studying = models.BooleanField()
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        _str = f"{str(self.user_profile)} Education"
        if self.level:
            _str += f" @ {self.get_level_display()}"
        if self.institute:
            _str += f" @ {self.institute}"
        if self.start_year:
            _str += f" ({self.start_year})"
        return _str


class Application(models.Model):
    class State(models.TextChoices):
        ACCEPTED = 'A', _('Accepted')
        REJECTED = 'R', _('Rejected')
        PENDING = 'P', _('Pending')

    state = models.CharField(choices=State.choices, max_length=1, default=State.PENDING)
    offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE, related_name='applications')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    resume = models.FileField(upload_to='resumes/', null=True)


