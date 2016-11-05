# -*- coding: utf-8 -*-

from openerp import models, fields, api



class account_tax(models.Model):

    _inherit = 'account.tax'
    
    type_ec = fields.Selection(
        [
            ('vat', 'IVA Diferente de 0%'),
            ('vat0', 'IVA 0%'),
            ('novat', 'No objeto de IVA'),
            ('ret_ir', 'Renta'),
            ('ice', 'ICE'),
            ('other', 'Otro')
            ],
        'Tipo Impuesto - Ecuador',
         required=False,
         help="""Tipo de Impuesto Ecuador"""
    )

 


class account_tax(models.Model):
    
    _inherit = "account.tax.template"
    
    type_ec = fields.Selection(
        [
            ('iva', 'IVA'),
            ('renta', 'Renta'),
            ('ice', 'ICE'),
            ('other', 'Otro')
            ],
        'Tipo Impuesto - Ecuador',
         required=False,
         help="""Tipo de Impuesto Ecuador"""
    )

    