# -*- coding: utf-8 -*-
{
    'name': 'Modulo Laboratorio. Aprender Conceptos de Odoo - Pos (Punto de Venta) - Javascript',
    'version': '0.0.1',
    'author': 'Juan Carlos Saavedra',
    'summary': 'Laboratorios de Pos. Punto de Venta',
    'depends': [
        'point_of_sale'
    ],
    'data': [
        'static/src/xml/validar.orden.xml',
        'static/src/xml/visualizar.total.lineas.orden.xml',
        'static/src/xml/partner.add.field.xml'
    ],
    'qweb': [
         'static/src/xml/templates.visualizar.total.lineas.orden.xml',
         'static/src/xml/templates.partner.add.field.xml' 
    ],

    'installable': True,
}