

{
    'name': 'Retenciones Ecuatorianas',
    'version': '0.0.1',
    'author': 'Juan Carlos Saavedra',
    'category': 'Ecuador',
    'complexity': 'normal',
    'data': [
         'security/ir.model.access.csv'
    ],

    'depends': [
        'base',
        'sale',
        'stock',
        'account',
        'account_accountant',
        #https://github.com/odoo-ecuador/odoo-ecuador
        'l10n_ec_authorisation',
        'l10n_ec_partner',
        #modulos propios
        'campus_invoice'
    ],
     "description":
     """
     
     """,
    'installable': True,
}

 