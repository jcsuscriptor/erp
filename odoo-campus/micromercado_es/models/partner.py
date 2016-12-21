# -*- coding: utf-8 -*-

from openerp import models, fields

 
class ResPartner(models.Model):

    _inherit = 'res.partner'
     
    type_ced_ruc = fields.Selection(
        default='cedula'
    )

    tipo_persona = fields.Selection(
        default='6'
    )

    company_type = fields.Selection(default='person') 

 