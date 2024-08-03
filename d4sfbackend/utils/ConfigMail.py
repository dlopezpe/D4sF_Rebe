from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from_email_const = "D4SmartFarming <soporte@d4smartfarming.com>"

bbc_const = 'backups@smartbits.es'


def send_email(subject, to, template, context):
    # Renderizar el contenido HTML desde una plantilla
    html_content = render_to_string(template, context)

    # text_content = strip_tags(html_content)  # Elimina las etiquetas HTML para obtener el texto plano

    # Crear el objeto EmailMultiAlternatives
    email = EmailMultiAlternatives(subject, html_content, from_email_const, [to], [bbc_const])
    email.attach_alternative(html_content, "text/html")

    # Enviar el correo electrónico
    email.send()
