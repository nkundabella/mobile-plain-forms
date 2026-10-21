# ⚡ Django All Form Fields Showcase (Django Omniverse)

A Django demo application showcasing built-in Django form fields, custom composite fields (`MultiValueField`, `ComboField`), HTML5 inputs, file uploads, and server-side validation. It is intended for local development and is not configured as a production deployment.

---

## 🚀 Quick Start

From this directory (`django_form_fields_app`), create and activate a virtual environment, then install the dependencies:

```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# Initialize the local database and start the development server
python manage.py migrate
python manage.py runserver
```

Then open your browser at:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

The development server uses a local-only secret key by default. Before deploying, set `DJANGO_SECRET_KEY` to a private, randomly generated value, set `DJANGO_DEBUG=false`, and set `DJANGO_ALLOWED_HOSTS` to a comma-separated list of your hostnames. Production deployment also requires completing Django's deployment checklist.

---

## 📋 Comprehensive Catalog of Included Fields (32 Fields)

| # | Django Field Class | Widget / Input Type | Description & Purpose |
|---|--------------------|---------------------|-----------------------|
| 1 | `forms.CharField` | `TextInput` | Single-line text input |
| 2 | `forms.CharField` | `Textarea` | Multi-line text for notes or biography |
| 3 | `forms.CharField` | `PasswordInput` | Masked sensitive credential input |
| 4 | `forms.SlugField` | `TextInput` | URL-safe slug validation (alphanumeric, dashes, underscores) |
| 5 | `forms.UUIDField` | `TextInput` | 128-bit RFC 4122 standard UUID identifier |
| 6 | `forms.RegexField` | `TextInput` | Custom strict regex pattern matching (`DEV-2026`) |
| 7 | `forms.EmailField` | `EmailInput` | RFC-compliant email address validation |
| 8 | `forms.URLField` | `URLInput` | Fully qualified web address with protocol |
| 9 | `forms.IntegerField` | `NumberInput` | Whole integer number with `min_value` / `max_value` |
| 10 | `forms.FloatField` | `NumberInput` | Floating-point decimal with precision steps |
| 11 | `forms.DecimalField` | `NumberInput` | High-precision currency / financial fixed-point decimal |
| 12 | `forms.DateField` | `DateInput (type='date')` | HTML5 calendar date picker |
| 13 | `forms.TimeField` | `TimeInput (type='time')` | HTML5 clock time picker |
| 14 | `forms.DateTimeField` | `DateTimeInput (type='datetime-local')` | Unified date and time selector |
| 15 | `forms.SplitDateTimeField` | `SplitDateTimeWidget` | Dual compound synchronized date and time inputs |
| 16 | `forms.DurationField` | `TextInput` | Timedelta representation (e.g. `2 days, 03:15:00`) |
| 17 | `forms.BooleanField` | `CheckboxInput` | Binary True/False checkbox toggle |
| 18 | `forms.NullBooleanField` | `Select` | Tristate choice (Unknown, Yes, No) |
| 19 | `forms.ChoiceField` | `Select` | Single choice dropdown menu |
| 20 | `forms.ChoiceField` | `RadioSelect` | Single choice visual radio cards |
| 21 | `forms.TypedChoiceField` | `Select` | Automatically coerces selection to Python `int` |
| 22 | `forms.MultipleChoiceField` | `SelectMultiple` | Multi-selection list box |
| 23 | `forms.MultipleChoiceField` | `CheckboxSelectMultiple` | Multi-selection checkboxes |
| 24 | `forms.TypedMultipleChoiceField` | `SelectMultiple` | Multi-selection yielding list of parsed integers |
| 25 | `forms.GenericIPAddressField` | `TextInput` | Validates IPv4 or IPv6 network addresses |
| 26 | `forms.JSONField` | `Textarea` | Parses and validates JSON dictionaries & arrays |
| 27 | `forms.FilePathField` | `Select` | Selects existing filesystem template from server directory |
| 28 | `forms.FileField` | `ClearableFileInput` | Document/attachment file upload (`request.FILES`) |
| 29 | `forms.ImageField` | `ClearableFileInput` | Image binary upload validated using Pillow |
| 30 | `forms.ComboField` | `TextInput` | Subclasses `CharField` to run multi-validator chains |
| 31 | `forms.MultiValueField` | `MultiWidget` (`CoordinateWidget`) | Custom composite field orchestrating Latitude & Longitude |
| 32 | `forms.CharField` | `HiddenInput` | Hidden token for session or tracking data |

---

## 🎨 Key Features & UI Highlights

- **Dark Glassmorphic UI**: Ambient glows, blur effects, clean gradients, and responsive typography using Google Fonts (`Outfit` + `JetBrains Mono`).
- **Interactive Sticky Category Nav**: Easily jump across 8 categorized field sections.
- **One-Click Demo Data Pre-fill**: Button to instantly populate valid values across all fields for testing.
- **`cleaned_data` Inspection Dashboard**: Displays a formatted summary table of all submitted values with their native Python data types.
- **File Upload Storage**: Uploaded files and images are processed, validated, and saved to the `media/` directory.

---

## 📂 Project Architecture

```
django_form_fields_app/
│
├── manage.py                          # Django management CLI
├── db.sqlite3                         # Created locally by migrations; not committed
│
├── config/                            # Project configuration
│   ├── __init__.py
│   ├── settings.py                   # App config, media/static settings
│   ├── urls.py                       # Project URL routes
│   ├── wsgi.py
│   └── asgi.py
│
├── showcase/                          # Showcase Django app
│   ├── forms.py                      # AllDjangoFieldsForm with all 32 fields
│   ├── views.py                      # Form processing & cleaned_data inspector
│   ├── urls.py                       # App URL definitions
│   │
│   ├── sample_files/                 # Sample files for FilePathField
│   │   ├── config_template.yaml
│   │   └── report_template.md
│   │
│   ├── templates/showcase/           # HTML templates
│   │   ├── base.html                 # Shell layout & ambient lighting
│   │   └── form_showcase.html        # Form and results dashboard
│   │
│   └── static/css/                   # Static assets
│       └── styles.css                # Glassmorphic CSS design system
│
└── media/                             # Destination for user file uploads
```
