from django.shortcuts import render, redirect
from django.contrib import messages
from .models import HeaderTitle, HeroSection, Quote, AboutSection, TimelineItem, Skill, Certificate, Project, ContactInfo, SocialLink
from .forms import ContactForm
from django.core.mail import BadHeaderError
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
import io


def portfolio_home(request):
    header_title = HeaderTitle.objects.filter(is_active=True).first()
    hero_section = HeroSection.objects.filter(is_active=True).first()
    quotes = Quote.objects.filter(is_active=True)
    about_sections = AboutSection.objects.filter(is_active=True)
    
    # Timeline grouping
    timeline_items = TimelineItem.objects.filter(is_active=True)
    education_timeline = timeline_items.filter(category='education')
    career_timeline = timeline_items.filter(category='career')
    future_timeline = timeline_items.filter(category='future')
    
    skills = Skill.objects.filter(is_active=True)
    certificates = Certificate.objects.filter(is_active=True)
    projects = Project.objects.filter(is_active=True)
    
    # ✅ Add Contact Info (first record only)
    contact_info = ContactInfo.objects.first()
    social_links = SocialLink.objects.filter(is_active=True)
    
    form = ContactForm()
    
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                contact_msg = form.save()
                # Email sending is handled in model save()
                
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('portfolio_home')
            except BadHeaderError:
                error_msg = 'Invalid header found. Could not send email.'
            except Exception as e:
                error_msg = f'There was an error sending your message: {e}'

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': error_msg})

            messages.error(request, error_msg)
        else:
            error_msg = form.errors.as_json()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': error_msg})

            messages.error(request, 'Please correct the errors below.')

    context = {
        'header_title': header_title,
        'hero_section': hero_section,
        'quotes': quotes,
        'about_sections': about_sections,
        'education_timeline': education_timeline,
        'career_timeline': career_timeline,
        'future_timeline': future_timeline,
        'skills': skills,
        'certificates': certificates,
        'projects': projects,
        'contact_info': contact_info,   
        'form': form,
        'social_links': social_links,
        
    }
    return render(request, 'main/index.html', context)



def generate_cv_pdf(request):
    # Fetch data from your models
    context = {
        'herosection_set': HeroSection.objects.filter(is_active=True),
        'headertitle_set': HeaderTitle.objects.filter(is_active=True),
        'aboutsection_set': AboutSection.objects.filter(is_active=True),
        'timelineitem_set': TimelineItem.objects.filter(is_active=True).order_by('display_order'),
        'skill_set': Skill.objects.filter(is_active=True).order_by('display_order'),
        'certificate_set': Certificate.objects.filter(is_active=True).order_by('display_order'),
        'project_set': Project.objects.filter(is_active=True).order_by('display_order'),
        'quote_set': Quote.objects.filter(is_active=True).order_by('display_order'),
        'contactinfo_set': ContactInfo.objects.all(),
        'sociallink_set': SocialLink.objects.filter(is_active=True),
    }
    
    # Render HTML template
    html_string = render_to_string('main/cv_template.html', context)
    
    # Create PDF in memory without temporary files
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    
    # Create a bytes buffer for the PDF
    pdf_buffer = io.BytesIO()
    html.write_pdf(target=pdf_buffer)
    
    # Create HTTP response with PDF
    response = HttpResponse(
        pdf_buffer.getvalue(),
        content_type='application/pdf'
    )
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    
    return response