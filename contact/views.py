from django.shortcuts import render
from django.template import Context, Template
from .forms import ContactForm
from minisettings.get_values import mini_settings
from django.http.response import HttpResponseRedirect
from django.core.mail import send_mail


def contact(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_addr = x_forwarded_for.split(',')[0]
    else:
        ip_addr = request.META.get('REMOTE_ADDR')
    usr_agent = request.META.get('HTTP_USER_AGENT')

    if request.method == 'POST':
        form = ContactForm(data=request.POST)

        if form.is_valid():
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            message = request.POST.get('message', '')

            addresses = mini_settings('contact_emails')
            addresses = addresses.split(";")
            addresses = [x.strip("\n\r\t ") for x in addresses]
            print("New contact form submission! Send email to addresses: " + ", ".join(addresses))
            
            # Email the profile with the contact information
            template = Template(mini_settings('email_contact_template'))
            context = Context({
                'name': name,
                'email': email,
                'message': message,
                'ip': ip_addr,
                'agent': usr_agent
            })
            content = template.render(context)
            
            send_mail("New message via contact form", content,
                      'mailer@example.com', addresses, html_message=content, fail_silently=False)
            
            return HttpResponseRedirect("/contact/done/")
        else:
            form = ContactForm()
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})


def done(request):
    return render(request, 'contact/done.html')
