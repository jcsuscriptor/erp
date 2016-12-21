#Problemas para reemplazar reportes 'data': ['view/report_invoice_document_templates.xml'
#'data': ['view/campus_invoice.xml',
        
{
    'name': 'Facturas Ecuatorianas',
    'version': '0.0.1',
    'author': 'Juan Carlos Saavedra',
    'category': 'Ecuador',
    'complexity': 'normal',
    'data': [
        'view/campus_invoice.xml',
        'view/account_tax_view.xml',
		'view/invoice_view.xml',
        'data/report_paperformat.xml'
    ],
     'depends': [
        'base',
        'sale',
        'stock',
        'account',
        'account_accountant',
        #https://github.com/odoo-ecuador/odoo-ecuador
        'l10n_ec_authorisation',
        'l10n_ec_partner'

    ],
     "description":
     """
     
     """,
    'installable': True,
}

 