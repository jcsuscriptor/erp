# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
import amount_to_text_es
import logging
_logger = logging.getLogger(__name__)




class account_invoice(models.Model):
    _inherit = "account.invoice"

    #TODO: JSA, analizar si se utiliza el campo referencia como numero de factura de proveedor.
    supplier_invoice_number = fields.Char(string='Numero Factura Proveedor',
        help="The reference of this invoice as provided by the supplier.",
        readonly=True, states={'draft': [('readonly', False)]})
 
    #TODO: Existe varios campos para direccion en partner.
    #street street2. Buscar una forma para guardar concatenado
    invoice_address = fields.Char("Dirección", 
      help="Dirección de facturación, guardando en la factura no sólo en el cliente",
      related='partner_id.street', store=True)

    #TODO: Existe varios campos de telefonos. Ver la forma de concatenar todos los datos.
    #phone mobile
    invoice_phone = fields.Char("Teléfono", 
        help="Teléfono de facturación, guardando en la factura no sólo en el cliente",
        related='partner_id.phone', store=True)
  
    base_amount_vat = fields.Monetary(string='Gravado IVA 14%',
        store=True, readonly=True, compute='_get_ecuador_amounts')
    base_amount_vat_cero = fields.Monetary(string='Gravado IVA 0%',
        store=True, readonly=True, compute='_get_ecuador_amounts')
    #
    #base_amount_novat = fields.Monetary(string='Base No IVA',
    #    store=True, readonly=True, compute='_get_ecuador_amounts')

    base_amount_withholding_rent = fields.Monetary(string='Base Impuesto Renta',
        store=True, readonly=True, compute='_get_ecuador_amounts')
  
    vat = fields.Monetary(string='14% IVA', 
        store=True, readonly=True, compute='_get_ecuador_amounts')
    
    withholding_rent = fields.Monetary(string='Impuesto Renta', 
        store=True, readonly=True, compute='_get_ecuador_amounts')
   
    invoice_total = fields.Monetary(string='Total', 
        store=True, readonly=True, compute='_get_ecuador_amounts')


    #'invoice_address':fields.char("Invoice address", help="Invoice address as in VAT document, saved in invoice only not in partner"),
    #'invoice_phone':fields.char("Invoice phone", help="Invoice phone as in VAT document, saved in invoice only not in partner"),     
    #reference = fields.Char(string='Vendor Reference',
    #    help="The partner reference of this invoice.", readonly=True, states={'draft': [('readonly', False)]})


    @api.multi
    def action_move_create(self):
        _logger.debug('action_move_create. partner_id.id %s',self.partner_id.id) 
        return super(account_invoice, self).action_move_create()

    @api.multi
    def amount_to_text(self, amount, currency='Euro'):
       return amount_to_text_es.amount_to_text(amount, currency)


    @api.model
    def create(self, vals):
        _logger.debug('create. vals: %s',vals) 
        auth_inv_id = vals.get('auth_inv_id')
        type_invoice = vals.get('type')
   
        if type_invoice and type_invoice in ['out_invoice'] and not auth_inv_id :
           _logger.debug('No existe auth_inv_id. Type Invoice is out_invoice') 
           journal = self.env['account.journal'].browse(vals.get('journal_id'))
           if journal:
              #TODO: JSA. Si no existe la autorizacion asociada, lanzar error ?? 
              if journal.auth_id:
                 vals['auth_inv_id'] = journal.auth_id.id   
              else: 
                msg = u'No se ha configurado una autorización en este diario: ' + journal.name
                raise Exception(msg)
       
        invoice = super(account_invoice, self).create(vals)
        return invoice

    
 
    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id')
    def _get_ecuador_amounts(self):
        """
        Calcular los impuestos Ecuador. Gravado IVA,  Gravado IVA 0%, IVA, Renta
        """
        _logger.debug('_get_ecuador_amounts') 
        vat_taxes = self.tax_line_ids.filtered(
            lambda r: (
                r.tax_id.type_ec == 'vat'))

        vat_taxes_cero = self.tax_line_ids.filtered(
            lambda r: (
                r.tax_id.type_ec == 'vat0'))

        ret_ir = self.tax_line_ids.filtered(
            lambda r: (
                r.tax_id.type_ec == 'ret_ir'))
  
        self.base_amount_vat = sum(vat_taxes.mapped('base'))
        self.base_amount_vat_cero = sum(vat_taxes_cero.mapped('base'))
        self.base_amount_withholding_rent = sum(ret_ir.mapped('base'))

        self.vat = sum(vat_taxes.mapped('amount'))  
        self.withholding_rent = sum(ret_ir.mapped('amount'))          
 
        self.invoice_total = self.amount_untaxed + self.vat 
       
    @api.one
    @api.constrains('supplier_invoice_number')
    def _check_unique_supplier_invoice_number_insensitive(self):
        """
           Numero de factura, debe ser unico por proveedor. 
            
           Copy from: account_invoice_supplier_ref_unique
           https://github.com/OCA/account-invoicing/tree/9.0/account_invoice_supplier_ref_unique 
        """
        #TODO: JSA. El objeto account_invoice base, tiene un campo referencia, y posee una validacion
        #que no se repita por proveedor. Analizar si este campo se utiliza como numero de factura. 
        _logger.debug('_check_unique_supplier_invoice_number_insensitive') 
        if (
                self.supplier_invoice_number and
                self.type in ('in_invoice', 'in_refund')):
            same_supplier_inv_num = self.search([
                ('commercial_partner_id', '=', self.commercial_partner_id.id),
                ('type', 'in', ('in_invoice', 'in_refund')),
                ('supplier_invoice_number',
                 '=ilike',
                 self.supplier_invoice_number),
                ('id', '!=', self.id),
                ])
            if same_supplier_inv_num:
                raise ValidationError(
                    _("The invoice/refund with supplier invoice number '%s' "
                      "already exists in Odoo under the number '%s' "
                      "for supplier '%s'.") % (
                        same_supplier_inv_num[0].supplier_invoice_number,
                        same_supplier_inv_num[0].number or '-',
                        same_supplier_inv_num[0].partner_id.display_name))

    
    @api.onchange('journal_id') #, 'company_id')
    def _set_authorisation_sri(self):
        """
            Establecer la autorizacion del SRI, asociada al diario de la factura. Si no existe
            lanzar Warning.
        """
        _logger.debug('_set_authorisation_sri')
       
        if not self.journal_id or self.type not in ['out_invoice']:
            return;

        #journal = self.env['account.journal'].browse(self.journal_id.id)

        #if not journal:
        #    return;
        
        if not self.journal_id.auth_id:
                msg = u'No se ha configurado una autorización en este diario: ' + self.journal_id.name
                return {
                    'warning': {
                        'title': 'Error',
                        'message': msg
                        }
                    }
         
        self.auth_inv_id = self.journal_id.auth_id  
        



       
    """
    def get_taxes_values(self):
        _logger.debug('get_taxes_values') 
        tax_grouped = {}
        for line in self.invoice_line_ids:
            price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.invoice_line_tax_ids.compute_all(price_unit, self.currency_id, line.quantity, line.product_id, self.partner_id)['taxes']
            for tax in taxes:
                tax_browse = self.env['account.tax'].browse(tax['id'])
                _logger.debug('get_taxes_values. tax.id %s, tax.type_ec %s',tax['id'],tax_browse.type_ec)
             
                val = {
                    'invoice_id': self.id,
                    'name': tax['name'],  
                    'tax_id': tax['id'],
                    'amount': tax['amount'],
                    'manual': False,
                    'sequence': tax['sequence'],
                    'type_ec': "iva",
                    'account_analytic_id': tax['analytic'] and line.account_analytic_id.id or False,
                    'account_id': self.type in ('out_invoice', 'in_invoice') and (tax['account_id'] or line.account_id.id) or (tax['refund_account_id'] or line.account_id.id),
                }

                
                # If the taxes generate moves on the same financial account as the invoice line,
                # propagate the analytic account from the invoice line to the tax line.
                # This is necessary in situations were (part of) the taxes cannot be reclaimed,
                # to ensure the tax move is allocated to the proper analytic account.
                if not val.get('account_analytic_id') and line.account_analytic_id and val['account_id'] == line.account_id.id:
                    val['account_analytic_id'] = line.account_analytic_id.id

                key = self.env['account.tax'].browse(tax['id']).get_grouping_key(val)

                if key not in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['amount'] += val['amount']
        return tax_grouped
    """
    
     