# -*- coding: utf-8 -*-

from openerp import models, fields, api,tools

import logging
_logger = logging.getLogger(__name__)


class report_invoice(models.Model):

    _name = "campus_invoice_report.client"

    #specify the parameter _auto=False to the odoo model, so no table corresponding to the fields is created automatically.
    _auto = False
    

    ced_ruc = fields.Char(string="Ced/RUC", readonly = True)
    name = fields.Char(string="Nombres",readonly = True)
    estado = fields.Char(string="Estado",readonly = True)
    date_invoice = fields.Date(string="Fecha",readonly = True)
    numero_factura = fields.Char(string="Numero",readonly = True)

    base_imponible = fields.Float(string="Base Imponible",readonly = True)
    grabado_iva_0 = fields.Float(string="Grabado IVA 0",readonly = True)
    grabado_iva = fields.Float(string="Grabado IVA",readonly = True)
    iva = fields.Float(string="IVA",readonly = True)
    total = fields.Float(string="Total",readonly = True)

    


    def init(self, cr):
        """ Reporte de listado de facturas de clientes
        """
        tools.drop_view_if_exists(cr, 'campus_invoice_report_client')
        cr.execute("""  CREATE VIEW campus_invoice_report_client AS (
                    select 
                        inv.id,
                        par.ced_ruc,
                        par.name,
                        CASE 
                        WHEN  (inv.state = 'paid' or inv.state = 'open') THEN 'emitida'
                        WHEN (inv.state ='cancel') THEN 'cancelada'
                        END AS estado,
                        inv.date_invoice,
                        inv.move_name numero_factura, 
                        round(inv.amount_untaxed,4) base_imponible,
                        round(inv.base_amount_vat_cero,4)  grabado_iva_0,
                        round(inv.base_amount_vat,4)  grabado_iva,
                        round(inv.vat,4)  iva,
                        round(inv.invoice_total,4) total
                    from 
                        account_invoice inv
                        inner join res_partner par on inv.partner_id = par.id
                        left join  account_move mov on inv.move_id = mov.id
                    where inv.type = 'out_invoice'
                    order by move_name
                ) 
                """)
    
