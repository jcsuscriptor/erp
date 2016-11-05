# -*- coding: utf-8 -*-
# © <2016> <Cristian Salamea>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import time

from openerp import (
    models,
    fields,
    api
)
from openerp.exceptions import (
    except_orm,
    Warning as UserError
    )
import openerp.addons.decimal_precision as dp



class AccountWithdrawingLine(models.Model):
    """ Implementacion de detalle del documento de retencion """
 
    _name = 'account.retention.linea'
    _description = 'Detalle de retenciones'
   
    STATES_VALUE = {'draft': [('readonly', False)]}

    withhold_id = fields.Many2one(
        'account.retention',
        string='Documento',
        ondelete='cascade',
        index=True
    )

  
    #'fiscalyear_id': fields.many2one('account.fiscalyear', 'Fiscal Year',
    #                                         help="Fiscal Year of transaction"),
    fiscal_year = fields.Char('Ejercicio Fiscal', size=4)
    
    invoice_tax_id = fields.Many2one(
        'account.invoice.tax',
        string='Impuesto' 
    )


    #'description': fields.selection([('iva', 'IVA'), ('renta', 'RENTA'), ], 'Tax',
    #                                        help="Type of Tax (IVA/RENTA)"),


    base = fields.Monetary(string='Base imponible para la retencion')                                     
                                
    percent = fields.Float('Porcentaje', size=20)
 
    amount = fields.Monetary(
        string='Valor Retenido',
        digits_compute=dp.get_precision('Account')
    )

    currency_id = fields.Many2one('res.currency', related='withhold_id.currency_id', store=True)
 

class AccountWithdrawing(models.Model):
    """ Implementacion de documento de retencion """
 
    _name = 'account.retention'
    _description = 'Withdrawing Documents'
    _order = 'date ASC'

    STATES_VALUE = {'draft': [('readonly', False)]}


    @api.multi
    def _get_in_type(self):
        context = self._context
        if 'type' in context and context['type'] in ['in_invoice', 'liq_purchase']:  # noqa
            return 'ret_in_invoice'
        else:
            return 'ret_out_invoice' 
    """
    
    @api.model
    def _default_currency(self):
        _logger.debug('_default_currency') 
        journal = self._default_journal()
        return journal.currency_id or journal.company_id.currency_id
    """

    name = fields.Char(
        'Número',
        size=64,
        readonly=True,
        required=True,
        states=STATES_VALUE
        )
 
    num_document = fields.Char(
        'Num. Comprobante',
        size=50,
        readonly=True,
        states=STATES_VALUE
        )

    internal_number = fields.Char(
        'Número Interno',
        size=64,
        readonly=True,
        required=True,
        default='/'
        )

    date = fields.Date(
        'Fecha Emision',
        readonly=True,
        states={'draft': [('readonly', False)]}, required=True)

   

    invoice_id = fields.Many2one(
        'account.invoice',
        string='Documento',
        required=False,
        readonly=True,
        states=STATES_VALUE,
        domain=[('state', '=', 'open')]
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Empresa',
        required=True,
        readonly=True,
        states=STATES_VALUE
     )

    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True,
        change_default=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env['res.company']._company_default_get('account.invoice')  # noqa
        )
   
    currency_id = fields.Many2one('res.currency', related='invoice_id.currency_id', store=True, readonly=True)

    type = fields.Selection(
        related='invoice_id.type',
        string='Tipo Comprobante',
        readonly=True,
        store=True
        )

    in_type = fields.Selection(
        [
            ('ret_in_invoice', u'Retención a Proveedor'),
            ('ret_out_invoice', u'Retención de Cliente')
        ],
        string='Tipo',
        states=STATES_VALUE,
        readonly=True,
        default=_get_in_type
        )
 
      
     
    state = fields.Selection(
        [
            ('draft', 'Borrador'),
            ('early', 'Anticipado'),
            ('done', 'Validado'),
            ('cancel', 'Anulado')
        ],
        readonly=True,
        string='Estado',
        default='draft'
        )

 
    auth_id = fields.Many2one(
        'account.authorisation',
        'Autorizacion',
        required=True,
        readonly=True,
        states=STATES_VALUE,
        domain=[('in_type', '=', 'interno')]
        )
       
   
    amount_total = fields.Float(
        compute='_amount_total',
        string='Total',
        store=True,
        digits_compute=dp.get_precision('Account')
        )   

    

    withhold_line_ids = fields.One2many(
        'account.retention.linea',
        'withhold_id',
        string='Detalle de Retenciones',
        readonly=True,
        states=STATES_VALUE
        )
 

        #========================
    """
    
        manual = fields.Boolean(
            'Numeración Manual',
            readonly=True,
            states=STATES_VALUE,
            default=True
            )

        
        move_id = fields.Many2one(
            related='invoice_id.move_id',
            string='Asiento Contable',
            readonly=True,
            store=True
            )

            

        to_cancel = fields.Boolean(
            string='Para anulación',
            readonly=True,
            states=STATES_VALUE
            )
    


    _columns = {
    
        

            'account_voucher_ids': fields.one2many('account.move.line', 'withhold_id', 'Withhold',
                                                help="List of account moves", track_visibility='onchange'),
            'automatic': fields.boolean('Automatic?',track_visibility='onchange'),
            'period_id': fields.related('invoice_id','period_id', type='many2one', relation='account.period', string='Period', store=True,
                                        help="Period related with this transaction", track_visibility='onchange'), 
            'shop_id': fields.many2one('sale.shop', 'Shop', readonly=True, states={'draft':[('readonly',False)]},
                                    help="Shop related with this transaction, only need in Purchase", track_visibility='onchange'),
        

        
            #P.R: Required to show in the ats report
            'total_iva': fields.function(_total_iva, method=True, type='float', string='Total IVA', store = False,
                                    help="Total IVA value of withhold", track_visibility='always'),   
            'total_renta': fields.function(_total_renta, method=True, type='float', string='Total RENTA', store = False,
                                    help="Total renta value of withhold", track_visibility='always'),      
            #P.R: Required to show in the tree view
            'total_base_iva': fields.function(_total_base_iva, method=True, type='float', string='Total Base IVA', store = False,
                                    help="Total base IVA of withhold", track_visibility='always'),   
            'total_base_renta': fields.function(_total_base_renta, method=True, type='float', string='Total Base RENTA', store = False,
                                    help="Total base renta of withhold", track_visibility='always'),      
            'comment': fields.text('Additional Information', track_visibility='onchange',
                                help="Text can be use to comment the withhold, if it's necesary"),
            # auxiliar fields to hold the amounts to use in base tax
            'invoice_amount_untaxed': fields.float('Invoice amount untaxed', digits_compute=dp.get_precision('Account'),
                                        help="Invoice amount untaxed used like base for the compute of tax"),  
            'invoice_vat_doce_subtotal': fields.float('Invoice vat doce subtotal', digits_compute=dp.get_precision('Account'),
                                        help="Invoice vat doce subtotal used like base for the compute of tax"),
            
        }

        _sql_constraints = [
            (
                'unique_number_partner',
                'unique(name,partner_id,type)',
                u'El número de retención es único.'
            )
        ]
    
    """