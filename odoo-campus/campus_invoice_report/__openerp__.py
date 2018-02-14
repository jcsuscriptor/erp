
{
    'name': 'Reportes Facturas Ecuatorianas',
    'version': '0.0.1',
    'author': 'Juan Carlos Saavedra',
    'category': 'Ecuador',
    'complexity': 'normal',
    'data': [
         'report/report_invoice_client.xml',
         'view/report_invoice_client.view.xml',
         'view/menuitem.xml',

    ],
     'depends': [ 
        'date_range',
        'account_fiscal_year',
        'report_xlsx',
        'report',        
        'campus_invoice' 
    ],
     "description":
     """
     
     """,
    'installable': True,
}

 