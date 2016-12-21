# -*- coding: utf-8 -*-

from openerp import models, fields

from stdnum import ec


class ResPartner(models.Model):

    _inherit = 'res.partner'
     
    def check_ced_ruc(self, cr, uid,type_ced_ruc,ced_ruc):
        if type_ced_ruc == 'cedula':
            return ec.ci.is_valid(ced_ruc)
        elif type_ced_ruc == 'ruc':
            return ec.ruc.is_valid(ced_ruc)
        else:
            return True