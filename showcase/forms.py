import os
import uuid
from datetime import date, time, datetime, timedelta
from pathlib import Path
from django import forms
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils import timezone

# Base sample directory for FilePathField
SAMPLE_FILES_DIR = os.path.join(settings.BASE_DIR, 'showcase', 'sample_files')


# Custom MultiWidget & MultiValueField demonstrating MultiValueField capabilities
class CoordinateWidget(forms.MultiWidget):
    """Custom composite widget holding Latitude and Longitude inputs."""
    def __init__(self, attrs=None):
        widgets = [
            forms.NumberInput(attrs={'placeholder': 'Latitude (e.g. -1.286389)', 'step': 'any', 'class': 'form-input'}),
            forms.NumberInput(attrs={'placeholder': 'Longitude (e.g. 36.817223)', 'step': 'any', 'class': 'form-input'}),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            if isinstance(value, (list, tuple)):
                return value
            parts = str(value).split(',')
            if len(parts) == 2:
                return [parts[0].strip(), parts[1].strip()]
        return [None, None]


class CoordinateField(forms.MultiValueField):
    """Composite MultiValueField validating Latitude (-90 to 90) and Longitude (-180 to 180)."""
    def __init__(self, *args, **kwargs):
        fields = (
            forms.FloatField(min_value=-90.0, max_value=90.0, required=False),
            forms.FloatField(min_value=-180.0, max_value=180.0, required=False),
        )
        kwargs.setdefault('widget', CoordinateWidget())
        kwargs.setdefault('require_all_fields', False)
        super().__init__(fields=fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list and data_list[0] is not None and data_list[1] is not None:
            return f"{data_list[0]}, {data_list[1]}"
        return None


class AllDjangoFieldsForm(forms.Form):
    """
    Comprehensive showcase form featuring every built-in Django form field type
    along with varied widgets, validations, and custom composite fields.
    """

    # ==========================================
    # 1. TEXT & IDENTIFICATION FIELDS
    # ==========================================
    char_field = forms.CharField(
        max_length=100,
        required=True,
        label="Full Name (CharField)",
        help_text="Standard single-line text input.",
        widget=forms.TextInput(attrs={'placeholder': 'e.g., Alex Johnson', 'class': 'form-control'}),
        initial="Alex Johnson"
    )

    textarea_char_field = forms.CharField(
        required=False,
        label="Biography / Notes (CharField - Textarea)",
        help_text="Multi-line text input.",
        widget=forms.Textarea(attrs={'placeholder': 'Enter biography or notes...', 'rows': 3, 'class': 'form-control'}),
        initial="Third-year computer science student focusing on web and mobile development."
    )

    password_field = forms.CharField(
        required=False,
        label="Password (CharField - PasswordInput)",
        help_text="Masked password input.",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password', 'class': 'form-control', 'autocomplete': 'new-password'}),
        initial="SecurePass2026!"
    )

    slug_field = forms.SlugField(
        max_length=60,
        required=False,
        label="Slug Identifier (SlugField)",
        help_text="URL-friendly text containing letters, numbers, or hyphens.",
        widget=forms.TextInput(attrs={'placeholder': 'e.g., student-project-demo', 'class': 'form-control'}),
        initial="student-project-demo"
    )

    uuid_field = forms.UUIDField(
        required=False,
        label="User UUID (UUIDField)",
        help_text="Valid 128-bit UUID format.",
        widget=forms.TextInput(attrs={'placeholder': 'e.g., 550e8400-e29b-41d4-a716-446655440000', 'class': 'form-control'}),
        initial="a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d"
    )

    regex_field = forms.RegexField(
        regex=r'^[A-Z]{3}-\d{4}$',
        required=False,
        label="Student / Employee Code (RegexField)",
        help_text="Pattern: 3 uppercase letters, hyphen, 4 digits (e.g., CSB-2026).",
        widget=forms.TextInput(attrs={'placeholder': 'e.g., CSB-2026', 'class': 'form-control'}),
        initial="CSB-2026"
    )

    email_field = forms.EmailField(
        required=True,
        label="Email Address (EmailField)",
        help_text="Valid email address.",
        widget=forms.EmailInput(attrs={'placeholder': 'student@example.edu', 'class': 'form-control'}),
        initial="student@example.edu"
    )

    url_field = forms.URLField(
        required=False,
        label="Portfolio / Website URL (URLField)",
        help_text="Web address starting with http:// or https://.",
        widget=forms.URLInput(attrs={'placeholder': 'https://example.com', 'class': 'form-control'}),
        initial="https://github.com"
    )

    # ==========================================
    # 2. NUMERIC FIELDS
    # ==========================================
    integer_field = forms.IntegerField(
        min_value=1,
        max_value=120,
        required=True,
        label="Age / Quantity (IntegerField)",
        help_text="Whole number between 1 and 120.",
        widget=forms.NumberInput(attrs={'placeholder': '21', 'class': 'form-control'}),
        initial=21
    )

    float_field = forms.FloatField(
        min_value=0.0,
        max_value=100.0,
        required=False,
        label="Grade Percentage (FloatField)",
        help_text="Decimal number between 0.0 and 100.0.",
        widget=forms.NumberInput(attrs={'placeholder': '88.5', 'step': '0.1', 'class': 'form-control'}),
        initial=88.5
    )

    decimal_field = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label="Tuition / Amount (DecimalField)",
        help_text="Currency amount with up to 2 decimal places.",
        widget=forms.NumberInput(attrs={'placeholder': '1500.00', 'step': '0.01', 'class': 'form-control'}),
        initial=1500.00
    )

    # ==========================================
    # 3. DATE & TIME FIELDS
    # ==========================================
    date_field = forms.DateField(
        required=False,
        label="Birth Date (DateField)",
        help_text="Date in YYYY-MM-DD format.",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=date(2003, 5, 14)
    )

    time_field = forms.TimeField(
        required=False,
        label="Class Time (TimeField)",
        help_text="Time in HH:MM format.",
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        initial=time(9, 30)
    )

    datetime_field = forms.DateTimeField(
        required=False,
        label="Exam Date & Time (DateTimeField)",
        help_text="Date and time picker.",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        initial=datetime(2026, 11, 15, 10, 0)
    )

    split_datetime_field = forms.SplitDateTimeField(
        required=False,
        label="Project Deadline (SplitDateTimeField)",
        help_text="Separate date and time controls.",
        widget=forms.SplitDateTimeWidget(
            date_attrs={'type': 'date', 'class': 'form-control', 'style': 'margin-bottom: 5px;'},
            time_attrs={'type': 'time', 'class': 'form-control'}
        ),
        initial=datetime(2026, 12, 1, 23, 59)
    )

    duration_field = forms.DurationField(
        required=False,
        label="Lab Duration (DurationField)",
        help_text="Duration (e.g., 02:30:00 for 2 hours 30 mins).",
        widget=forms.TextInput(attrs={'placeholder': '02:30:00', 'class': 'form-control'}),
        initial=timedelta(hours=2, minutes=30)
    )

    # ==========================================
    # 4. BOOLEAN & TRISTATE FIELDS
    # ==========================================
    boolean_field = forms.BooleanField(
        required=False,
        label="Agree to Terms & Conditions (BooleanField)",
        help_text="Check if you agree.",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        initial=True
    )

    null_boolean_field = forms.NullBooleanField(
        required=False,
        label="Enrollment Status (NullBooleanField)",
        help_text="Select Unknown, Yes, or No.",
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial="2"  # 'Yes'
    )

    # ==========================================
    # 5. CHOICE & MULTIPLE CHOICE FIELDS
    # ==========================================
    choice_field_select = forms.ChoiceField(
        choices=[
            ('django', 'Django'),
            ('react_native', 'React Native'),
            ('flutter', 'Flutter'),
            ('android_kotlin', 'Android (Kotlin)'),
            ('ios_swift', 'iOS (Swift)'),
        ],
        required=False,
        label="Primary Framework (ChoiceField)",
        help_text="Select your primary mobile/web framework.",
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial='django'
    )

    choice_field_radio = forms.ChoiceField(
        choices=[
            ('standard', 'Standard View'),
            ('compact', 'Compact View'),
            ('detailed', 'Detailed View'),
        ],
        required=False,
        label="Display Preference (ChoiceField - RadioSelect)",
        help_text="Choose one layout option.",
        widget=forms.RadioSelect(attrs={'class': 'form-radio-group'}),
        initial='standard'
    )

    typed_choice_field = forms.TypedChoiceField(
        choices=[
            (1, 'Year 1 - Freshman'),
            (2, 'Year 2 - Sophomore'),
            (3, 'Year 3 - Junior'),
            (4, 'Year 4 - Senior'),
        ],
        coerce=int,
        required=False,
        label="Academic Year (TypedChoiceField)",
        help_text="Coerced into integer on the server.",
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial=3
    )

    multiple_choice_field = forms.MultipleChoiceField(
        choices=[
            ('mobile', 'Mobile Development'),
            ('web', 'Web Applications'),
            ('database', 'Database Systems'),
            ('networking', 'Computer Networking'),
            ('security', 'Information Security'),
        ],
        required=False,
        label="Elective Courses (MultipleChoiceField)",
        help_text="Hold Ctrl (or Cmd) to select multiple options.",
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
        initial=['mobile', 'web']
    )

    multiple_choice_checkboxes = forms.MultipleChoiceField(
        choices=[
            ('email_updates', 'Email Announcements'),
            ('sms_alerts', 'SMS Urgent Notifications'),
            ('assignment_reminders', 'Assignment Due Reminders'),
        ],
        required=False,
        label="Notification Channels (MultipleChoiceField - Checkboxes)",
        help_text="Select all notification methods you prefer.",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-group'}),
        initial=['email_updates', 'assignment_reminders']
    )

    typed_multiple_choice_field = forms.TypedMultipleChoiceField(
        choices=[
            (101, 'Lab Room 101'),
            (102, 'Lab Room 102'),
            (201, 'Lecture Hall 201'),
            (202, 'Seminar Hall 202'),
        ],
        coerce=int,
        required=False,
        label="Preferred Study Rooms (TypedMultipleChoiceField)",
        help_text="Multi-select parsed as integer room numbers.",
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 4}),
        initial=[101, 201]
    )

    # ==========================================
    # 6. NETWORKING & SYSTEM DATA FIELDS
    # ==========================================
    ip_address_field = forms.GenericIPAddressField(
        protocol='both',
        unpack_ipv4=False,
        required=False,
        label="Local Server IP (GenericIPAddressField)",
        help_text="Enter a valid IPv4 or IPv6 address.",
        widget=forms.TextInput(attrs={'placeholder': '192.168.1.100', 'class': 'form-control'}),
        initial="192.168.1.100"
    )

    json_field = forms.JSONField(
        required=False,
        label="Student Preferences (JSONField)",
        help_text="Enter valid JSON format data.",
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'style': 'font-family: monospace;'}),
        initial={"theme": "light", "notifications_enabled": True, "language": "en"}
    )

    # ==========================================
    # 7. FILE & DIRECTORY FIELDS
    # ==========================================
    file_path_field = forms.FilePathField(
        path=SAMPLE_FILES_DIR,
        recursive=False,
        allow_files=True,
        allow_folders=False,
        required=False,
        label="Sample Document (FilePathField)",
        help_text="Select a file from the server directory.",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    file_field = forms.FileField(
        required=False,
        label="Upload Assignment Document (FileField)",
        help_text="Attach a PDF, document, or text file.",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    image_field = forms.ImageField(
        required=False,
        label="Upload Profile Photo (ImageField)",
        help_text="Upload an image (JPEG, PNG, etc.). Verified by Pillow.",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )

    # ==========================================
    # 8. COMPOSITE & VALIDATOR FIELDS
    # ==========================================
    combo_field = forms.ComboField(
        fields=[
            forms.CharField(max_length=50),
            forms.EmailField(),
        ],
        required=False,
        label="Alternate Contact Email (ComboField)",
        help_text="Validated as text up to 50 chars and valid email.",
        widget=forms.TextInput(attrs={'placeholder': 'contact@example.org', 'class': 'form-control'}),
        initial="contact@example.edu"
    )

    coordinates_multivalue = CoordinateField(
        required=False,
        label="Campus Coordinates (MultiValueField)",
        help_text="Latitude and Longitude values.",
        initial="-1.286389, 36.817223"
    )

    hidden_field = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        initial="form_session_token_12345"
    )


from .models import ImageShowcase

class ImageShowcaseForm(forms.ModelForm):
    """
    ModelForm demonstrating Django ImageField upload and automatic model persistence.
    """
    class Meta:
        model = ImageShowcase
        fields = ['title', 'description', 'image', 'alt_text', 'category', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Modern Glass Architecture', 'class': 'form-input'}),
            'description': forms.Textarea(attrs={'placeholder': 'Explain details, colors, story or specs...', 'rows': 3, 'class': 'form-textarea'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-file-input', 'accept': 'image/*'}),
            'alt_text': forms.TextInput(attrs={'placeholder': 'Accessible description of visuals', 'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
