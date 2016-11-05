# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

class account_invoice_tax(models.Model):
    _inherit = 'account.invoice.tax'  
    
    type_ec = fields.Selection(
        [
            ('iva', 'IVA'),
            ('renta', 'Renta'),
            ('ice', 'ICE'),
            ('other', 'Otro')
            ],
        'Tipo Impuesto - Ecuador',
         required=False,
         help="""Tipo de Impuesto. Ecuador"""
    )

  