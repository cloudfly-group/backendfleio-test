"""Email sending utility module"""

from django.core.mail import EmailMessage
from django.template import Context, Template


def send_email(
        from_field,
        to_emails,
        subject_template,
        body_template,
        params,
        cc=None,
        is_html: bool = False,
        auto_replied: bool = False,
        auto_generated: bool = True,
        attachments=None,
):
    """
    Sends email.
    from_field = From name <from@email>
    to_emails = string or list/tuple
    """

    if not isinstance(to_emails, (tuple, list)):
        to_emails = [to_emails]

    subject = Template(subject_template).render(Context(params))
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    text_body = Template(body_template).render(Context(params)).strip()
    # set appropriate headers
    headers = None
    if auto_generated:
        # all emails sent are auto generated
        headers = {
            'Auto-Submitted': 'auto-generated',
            'X-Auto-Response-Suppress': 'All',
        }
    if auto_replied and auto_generated:
        # mark the email as auto-replied rather than auto-generated when the message is
        # in direct response to another message
        headers['Auto-Submitted'] = 'auto-replied'

    if not cc:
        cc = list()

    msg = EmailMessage(subject=subject, body=text_body, from_email=from_field, to=to_emails, cc=cc, headers=headers,
                       attachments=attachments)
    if is_html:
        msg.content_subtype = 'html'
    msg.send()
