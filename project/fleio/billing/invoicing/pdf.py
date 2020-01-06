from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import logging

try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
    from reportlab.lib import enums
    from reportlab.lib import pagesizes
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
except Exception as e:
    logging.exception(e)


LOG = logging.getLogger(__name__)


def footer_pagination(canvas, doc):
    canvas.saveState()
    canvas.translate(0, 0)
    canvas.setFont('Helvetica-Bold', 6)
    width, height = pagesizes.A4
    canvas.drawCentredString(width / 2, cm, "Page {}".format(doc.page))
    canvas.restoreState()


def pdf_invoice(
        pdf_file, invoice_display_number, invoice_status, customer_details, company_details,
        invoice_items, invoice_totals, invoice_issue_date=None, invoice_due_date=None,
        text_after_invoice_items=None, invoice_title=None, invoice_author=None, invoice_creator=None,
        invoice_lang=None, invoice_subject=None, invoice_currency='',
):
    pdf_invoice_callable = getattr(settings, 'PDF_INVOICE_CALLABLE', pdf_invoice_impl)
    if not callable(pdf_invoice_callable):
        LOG.error('PDF_INVOICE_CALLABLE value is not callable, falling back to default implementation.')
        pdf_invoice_callable = pdf_invoice_impl

    pdf_invoice_callable(
        pdf_file=pdf_file,
        invoice_display_number=invoice_display_number,
        invoice_status=invoice_status,
        customer_details=customer_details,
        company_details=company_details,
        invoice_items=invoice_items,
        invoice_totals=invoice_totals,
        invoice_issue_date=invoice_issue_date,
        invoice_due_date=invoice_due_date,
        text_after_invoice_items=text_after_invoice_items,
        invoice_title=invoice_title,
        invoice_author=invoice_author,
        invoice_creator=invoice_creator,
        invoice_lang=invoice_lang,
        invoice_subject=invoice_subject,
        invoice_currency=invoice_currency,
    )


def pdf_invoice_impl(
        pdf_file, invoice_display_number, invoice_status, customer_details, company_details,
        invoice_items, invoice_totals, invoice_issue_date=None, invoice_due_date=None,
        text_after_invoice_items=None, invoice_title=None, invoice_author=None, invoice_creator=None,
        invoice_lang=None, invoice_subject=None, invoice_currency='',
):
    invoice_lang = invoice_lang or 'en'

    # Define paragraph styles
    title_style = ParagraphStyle(
        name='invTitleStyle',
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor='#404040',
        testTransform='upper',
        leading=20
    )
    sub_title_style = ParagraphStyle(
        name='invTitleStyle',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor='#404040',
        testTransform='upper'
    )
    norm_style = ParagraphStyle(
        name='invNormStyle',
        fontName='Helvetica',
        textColor='#606060',
        fontSize=8,
        leading=10,
        splitLongWords=1,
    )
    norm_style_bold = ParagraphStyle(
        name='invNormStyle',
        fontName='Helvetica-Bold',
        textColor='#606060',
        fontSize=8,
        leading=10
    )
    totals_style_bold = ParagraphStyle(
        name='invNormStyle',
        fontName='Helvetica-Bold',
        textColor='#000000',
        fontSize=8,
        leading=10,
        alignment=enums.TA_RIGHT
    )
    cost_style = ParagraphStyle(
        name='invCostStyle',
        fontName='Helvetica',
        textColor='#000000',
        fontSize=8,
        leading=10,
        alignment=enums.TA_CENTER
    )
    norm_style_right = ParagraphStyle(
        name='invNormStyleRight',
        fontName='Helvetica',
        textColor='#606060',
        fontSize=8,
        leading=10,
        alignment=enums.TA_RIGHT
    )
    head_style = ParagraphStyle(
        name='headStyle',
        fontName='Helvetica',
        textColor='#ffffff',
        backColor='#404040',
        fontSize=10,
        leading=12
    )
    # Begin invoice pdf generation
    invoice_title = invoice_title or invoice_display_number
    invoice_author = invoice_author or 'Fleio Billing'
    invoice_creator = invoice_creator or 'Fleio Billing'
    invoice_subject = invoice_subject or '{} {}'.format(invoice_display_number, invoice_status)

    doc = SimpleDocTemplate(pdf_file,
                            pagesize=pagesizes.A4,
                            leftMargin=cm,
                            rightMargin=cm,
                            topMargin=cm,
                            bottomMargin=cm,
                            title=invoice_title,
                            author=invoice_author,
                            creator=invoice_creator,
                            lang=invoice_lang,
                            subject=invoice_subject)

    # noinspection PyListCreation
    pdf_story = [Spacer(1, cm)]

    # Add invoice display number and header
    pdf_story.append(Paragraph(invoice_display_number, style=title_style))
    pdf_story.append(Paragraph(invoice_status, style=sub_title_style))
    pdf_story.append(Spacer(1, cm / 3))

    # Add customer and company info
    customer_paragraph = []
    # adds issue and due dates
    if invoice_issue_date:
        customer_paragraph.append(Paragraph(_('Issue Date: {}').format(invoice_issue_date), norm_style))
    if invoice_due_date:
        customer_paragraph.append(Paragraph(_('Due Date: {}').format(invoice_due_date), norm_style))
    # adds customer info
    customer_paragraph.append(Paragraph(_('Invoiced to:'), norm_style_bold))
    customer_details = customer_details or 'Customer details missing'
    for cinf in customer_details.splitlines():
        customer_paragraph.append(Paragraph(cinf, norm_style))
    # adds company info
    company_details = company_details or 'Company details missing'
    company_paragraph = [Paragraph(cinf, norm_style_right) for cinf in company_details.splitlines()]

    invoice_info = Table(data=[[customer_paragraph, company_paragraph]],
                         style=[('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                ('LEFTPADDING', (0, 0), (0, 0), 0),
                                ('RIGHTPADDING', (0, 0), (-1, -1), 0)])

    pdf_story.append(invoice_info)

    # Add invoice items
    # Set some items styles first
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), '#404040'),
        ('ALIGN', (3, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (3, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (1, 0), (-1, 0), '#ffffff'),
        ('SPAN', (0, 0), (2, 0)),
        ('LINEAFTER', (0, 1), (-2, -len(invoice_totals) - 1), 0.1, '#707070', None, (2, 2, 2)),
        ('LINEBELOW', (0, 1), (-1, -len(invoice_totals) - 1), 0.1, '#707070', None, (2, 2, 2)),
    ]

    items_table = []
    items_header = [Paragraph(_('Description'), head_style), '', '', _('Quantity'), _('Unit Price'), _('Cost')]
    items_table.append(items_header)

    last_item_num = 1
    for item in invoice_items:
        item_description = item['description']
        for option in item.get('options', []):
            item_description = '{} <br/> - {}'.format(item_description, option['display'])
            if option.get('price', 0) > 0:
                item_description = '{} ({} {})'.format(item_description, option['price'], invoice_currency)
        items_table.append([Paragraph(item_description.replace('\n', '<br/>'), norm_style), '', '',
                            Paragraph(str(item.get('quantity', '1')), cost_style),
                            Paragraph(str(item.get('unit_price')), cost_style),
                            Paragraph(str(item.get('cost')), cost_style)])
        table_style.append(('SPAN', (0, last_item_num), (2, last_item_num)))
        last_item_num += 1

    # Add totals
    for inv_total in invoice_totals:
        items_table.append(['', '', '', '',
                            Paragraph(str(inv_total['name']), totals_style_bold),
                            Paragraph(str(inv_total['value']), cost_style)])
    table_style.append(('LINEAFTER', (4, last_item_num), (-2, -1), 0.1, '#707070', None, (2, 2, 2)))
    table_style.append(('LINEBELOW', (4, last_item_num), (-1, -2), 0.1, '#707070', None, (2, 2, 2)))

    size_unit = pagesizes.A4[0] / 100
    invoice_items_table = Table(
        data=items_table,
        colWidths=(size_unit * 58, 1, 1, size_unit * 10, size_unit * 10, size_unit * 10),
        style=table_style,
    )

    pdf_story.append(invoice_items_table)

    if text_after_invoice_items:
        pdf_story.append(Paragraph(text=text_after_invoice_items, style=norm_style))

    doc.build(pdf_story, onFirstPage=footer_pagination, onLaterPages=footer_pagination)
