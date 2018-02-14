{
    'name': 'Modulo Laboratorio Reportes. Aprender Reportes de Odoo',
    'version': '0.0.1',
    'author': 'Juan Carlos Saavedra',
    'category': 'Ecuador',
    'complexity': 'normal',
    'depends': [
        #'date_range',
        #'report_xlsx',
        'campus_labs',
        'report',
    ],
    'data': [
        'report/report_client.xml',
        'wizard/simple_wizard_view.xml',
        #'wizard/date_range_wizard_view.xml',
        'view/client.report.view.xml',
        'view/reports.xml',
        'view/menuitems.xml',
    ],
     "description":"""

    """,
    'installable': True,
}

 