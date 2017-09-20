# -*- coding: utf-8 -*-
{
    'name': 'Modulo - Pos (Punto de Venta)',
    'version': '0.0.1',
    'author': 'Juan Carlos Saavedra',
    'summary': 'Personalizacion del Punto de Venta',
    'depends': [
        'point_of_sale',
         'l10n_ec_partner'
    ],
    'data': [
        'static/src/xml/visualizar.total.lineas.orden.xml',
        'static/src/xml/partner.add.field.xml'
    ],
    'qweb': [
         'static/src/xml/templates.visualizar.total.lineas.orden.xml',
         'static/src/xml/templates.partner.add.field.xml' 
    ],
    'installable': True,
}