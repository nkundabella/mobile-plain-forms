import os
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import ImageShowcase
from .forms import AllDjangoFieldsForm, ImageShowcaseForm

def form_showcase_view(request):
    """
    Renders and processes the All-Fields Django Form.
    Displays submitted cleaned data with field types, values, and upload metadata.
    """
    submitted = False
    cleaned_data_display = []
    uploaded_files_summary = []

    if request.method == 'POST':
        form = AllDjangoFieldsForm(request.POST, request.FILES)
        if form.is_valid():
            submitted = True
            cleaned = form.cleaned_data

            # Save uploaded files temporarily to media if provided
            if form.cleaned_data.get('file_field'):
                file_obj = form.cleaned_data['file_field']
                saved_path = default_storage.save(f"uploads/{file_obj.name}", ContentFile(file_obj.read()))
                uploaded_files_summary.append({
                    'field': 'General File Attachment (FileField)',
                    'name': file_obj.name,
                    'size_bytes': file_obj.size,
                    'content_type': getattr(file_obj, 'content_type', 'unknown'),
                    'saved_path': saved_path,
                })

            if form.cleaned_data.get('image_field'):
                img_obj = form.cleaned_data['image_field']
                saved_path = default_storage.save(f"uploads/images/{img_obj.name}", ContentFile(img_obj.read()))
                uploaded_files_summary.append({
                    'field': 'Profile Image / Avatar (ImageField)',
                    'name': img_obj.name,
                    'size_bytes': img_obj.size,
                    'content_type': getattr(img_obj, 'content_type', 'image/jpeg'),
                    'saved_path': saved_path,
                })

            # Format cleaned_data for elegant display
            for field_name, field_def in form.fields.items():
                if field_name in ('file_field', 'image_field'):
                    val = str(cleaned.get(field_name)) if cleaned.get(field_name) else "None uploaded"
                else:
                    raw_val = cleaned.get(field_name)
                    if isinstance(raw_val, (dict, list)):
                        val = json.dumps(raw_val, indent=2, default=str)
                    else:
                        val = str(raw_val)

                cleaned_data_display.append({
                    'name': field_name,
                    'label': field_def.label or field_name,
                    'type': field_def.__class__.__name__,
                    'value': val,
                    'python_type': type(cleaned.get(field_name)).__name__,
                })
    else:
        # Prepopulate with defaults
        form = AllDjangoFieldsForm()

    # Group fields into logical sections for the template
    sections = [
        {
            'title': 'Text & Identity Fields',
            'icon': '📝',
            'desc': 'Text, password, slugs, UUIDs, regex, and identifiers',
            'fields': ['char_field', 'textarea_char_field', 'password_field', 'slug_field', 'uuid_field', 'regex_field', 'email_field', 'url_field']
        },
        {
            'title': 'Numeric & Metrics Fields',
            'icon': '🔢',
            'desc': 'Integers, floating points, and high-precision currency decimals',
            'fields': ['integer_field', 'float_field', 'decimal_field']
        },
        {
            'title': 'Temporal Fields (Date, Time, Duration)',
            'icon': '⏱️',
            'desc': 'HTML5 date, clock time, datetime-local, split datetime, and duration',
            'fields': ['date_field', 'time_field', 'datetime_field', 'split_datetime_field', 'duration_field']
        },
        {
            'title': 'Boolean & Tristate Fields',
            'icon': '🔘',
            'desc': 'Binary checkbox toggles and 3-state (Yes / No / Unknown) NullBooleanField',
            'fields': ['boolean_field', 'null_boolean_field']
        },
        {
            'title': 'Selection & Choice Fields',
            'icon': '📋',
            'desc': 'Single Select, Radio Cards, Multi-Select, Checkboxes, and Type-Coerced Choices',
            'fields': ['choice_field_select', 'choice_field_radio', 'typed_choice_field', 'multiple_choice_field', 'multiple_choice_checkboxes', 'typed_multiple_choice_field']
        },
        {
            'title': 'Networking & Structured Data',
            'icon': '🌐',
            'desc': 'IPv4/IPv6 address parsing and JSON schema/payload formatting',
            'fields': ['ip_address_field', 'json_field']
        },
        {
            'title': 'Files, Media & Filesystem',
            'icon': '📁',
            'desc': 'Server filesystem file picker, document file uploads, and Pillow image validation',
            'fields': ['file_path_field', 'file_field', 'image_field']
        },
        {
            'title': 'Advanced & Composite Fields',
            'icon': '🧩',
            'desc': 'ComboField validator chaining, custom MultiValueField with MultiWidget, and HiddenInput',
            'fields': ['combo_field', 'coordinates_multivalue', 'hidden_field']
        },
    ]

    # Fetch featured and recent ImageShowcase models to display on the page
    recent_images = ImageShowcase.objects.all()[:4]

    context = {
        'form': form,
        'sections': sections,
        'submitted': submitted,
        'cleaned_data_display': cleaned_data_display,
        'uploaded_files_summary': uploaded_files_summary,
        'total_fields_count': len(form.fields),
        'recent_images': recent_images,
    }

    return render(request, 'showcase/form_showcase.html', context)


def image_gallery_view(request):
    """
    Renders the ImageShowcase model gallery displaying images stored in the database,
    and provides a form to upload new image instances.
    """
    upload_success = False

    if request.method == 'POST':
        upload_form = ImageShowcaseForm(request.POST, request.FILES)
        if upload_form.is_valid():
            new_image = upload_form.save()
            upload_success = True
            messages.success(request, f'Image "{new_image.title}" successfully uploaded and saved to database!')
            return redirect('showcase:image_gallery')
    else:
        upload_form = ImageShowcaseForm()

    images = ImageShowcase.objects.all()
    featured_image = ImageShowcase.objects.filter(is_featured=True).first() or images.first()

    context = {
        'images': images,
        'featured_image': featured_image,
        'upload_form': upload_form,
        'upload_success': upload_success,
        'total_images': images.count(),
    }
    return render(request, 'showcase/image_gallery.html', context)
    return render(request, 'showcase/image_gallery.html', context)
