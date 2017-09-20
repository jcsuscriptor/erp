# -*- coding: utf-8 -*-

import dateutil.parser
import StringIO

from openerp import (
    models,
    fields,
    api
)

import datetime

from openerp.tools.mimetypes import guess_mimetype

from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT

from openerp.exceptions import UserError

import itertools
try:
    import xlrd
    try:
        from xlrd import xlsx
    except ImportError:
        xlsx = None
except ImportError:
    xlrd = xlsx = None


import logging
_logger = logging.getLogger(__name__)




class formato_banco_loja(models.TransientModel):
   
    _name = 'campus_bancos.formato_banco_loja'
     
    fecha = fields.Char('fecha')
    transaccion = fields.Char('transaccion')
    rubro = fields.Char('rubro')
    concepto = fields.Char('concepto')
    referencia = fields.Char('referencia')
    oficina = fields.Char('oficina')
    debitos = fields.Char('debitos')
    creditos = fields.Char('creditos')
    saldo = fields.Char('saldo')
  

class ImportarFormatoBancoLoja(models.TransientModel):
    
    _inherit = "account.bank.statement.import"

  
    def _read_xls(self, file_contents, options):
        book = xlrd.open_workbook(file_contents=file_contents)
        return self._read_xls_book(book)
    
    def _read_xls_book(self, book):
        sheet = book.sheet_by_index(0)
        # emulate Sheet.get_rows for pre-0.9.4
        for row in itertools.imap(sheet.row, range(sheet.nrows)):
            values = []
            for cell in row:
                if cell.ctype is xlrd.XL_CELL_NUMBER:
                    is_float = cell.value % 1 != 0.0
                    values.append(
                        unicode(cell.value)
                        if is_float
                        else unicode(int(cell.value))
                    )
                elif cell.ctype is xlrd.XL_CELL_DATE:
                    is_datetime = cell.value % 1 != 0.0
                    # emulate xldate_as_datetime for pre-0.9.3
                    dt = datetime.datetime(*xlrd.xldate.xldate_as_tuple(
                        cell.value, book.datemode))
                    values.append(
                        dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                        if is_datetime
                        else dt.strftime(DEFAULT_SERVER_DATE_FORMAT)
                    )
                elif cell.ctype is xlrd.XL_CELL_BOOLEAN:
                    values.append(u'True' if cell.value else u'False')
                elif cell.ctype is xlrd.XL_CELL_ERROR:
                    raise ValueError(
                        _("Error cell found while reading XLS/XLSX file: %s") %
                        xlrd.error_text_from_code.get(
                            cell.value, "unknown error code %s" % cell.value)
                    )
                else:
                    values.append(cell.value)
            if any(x for x in values if x.strip()):
                yield values

    @api.model
    def _check_qif(self, data_file):
        return data_file.strip().startswith('!Type:')


    @api.model
    def _parse_file(self, data_file):
        """ Each module adding a file support must extends this method. It processes the file if it can, returns super otherwise, resulting in a chain of responsability.
            This method parses the given file and returns the data required by the bank statement import process, as specified below.
            rtype: triplet (if a value can't be retrieved, use None)
                - currency code: string (e.g: 'EUR')
                    The ISO 4217 currency code, case insensitive
                - account number: string (e.g: 'BE1234567890')
                    The number of the bank account which the statement belongs to
                - bank statements data: list of dict containing (optional items marked by o) :
                    - 'name': string (e.g: '000000123')
                    - 'date': date (e.g: 2013-06-26)
                    -o 'balance_start': float (e.g: 8368.56)
                    -o 'balance_end_real': float (e.g: 8888.88)
                    - 'transactions': list of dict containing :
                        - 'name': string (e.g: 'KBC-INVESTERINGSKREDIET 787-5562831-01')
                        - 'date': date
                        - 'amount': float
                        - 'unique_import_id': string. # Ensure transactions can be imported only once (if the import format provides unique transaction ids)
                        -o 'account_number': string
                            Will be used to find/create the res.partner.bank in odoo
                        -o 'note': string
                        -o 'partner_name': string
                        -o 'ref': string
        """

        #Validar Formato
        # guess mimetype from file content
        mimetype = guess_mimetype(data_file)
        _logger.debug('JC mimetype  %s',mimetype)

        #Leer Archivo
        Import = self.env['base_import.import']
        id = Import.create({
            'res_model': 'campus_bancos.formato_banco_loja',
            'file': data_file,
            'file_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        #raise UserError(_('El arhivo no tiene formato correcto'))
 

        #obtener los campos del modelo
        fields = Import.get_fields('campus_bancos.formato_banco_loja')
        _logger.debug('JC fields  %s',fields)
        
        _logger.debug('JC _parse_file self %s',self)
        #_logger.debug('JC data_file %s',data_file)
        _logger.debug('JC id %s',id)
 
        #record = Import.browse(id)
        #_logger.debug('record %s',record)
        
        #error: can't adapt type 'base_import.import'
        #rows = Import._read_file(record.file_type, record, {'headers': True})
        #_read_xls(self, record, options)
        options = {'headers': True}
        rows_to_import = self._read_xls(data_file, options)
       
        headers, matches = Import._match_headers(rows_to_import, fields, options)
        _logger.debug('headers %s',headers)
        _logger.debug('matches %s',matches)
        if options.get('headers'):
            rows_to_import = itertools.islice(rows_to_import, 1, None)
        
        #TODO: Ver la forma de mapear los indices
        #{0: ['fecha'], 1: ['transaccion'], 2: ['rubro'], 3: ['concepto'], 4: ['referencia'], 
        #5: ['oficina'], 6: ['debitos'], 7: ['creditos'], 8: ['saldo'], 9: ['id']}
        #[u'2016/12/01 00:00:00', u'Saldo Inicial', u'Saldo', u'', u'12', u'', u'0', u'0', u'9656.4', u''], [u'2016/12/05 15:58:36', u'NOTA DE DEBITO', u'RETIRO EN CAJERO AUTOM\xc1TICO', u'Universidad Internacional', u'5267', u'OFICINA MATRIZ', u'60', u'0', u'9596.4', u''],

        #TODO: saltar la fila Saldo Inicial. 0

        transactions = []
        vals_line = {}
        total = 0
        vals_bank_statement = {}
        #TODO: Utilizar itertools, para mejor rendimiento
        #for line in itertools.imap(rows_to_import, len(rows_to_import)):
        for line in rows_to_import:
            vals_line['date'] =  dateutil.parser.parse(line[0], fuzzy=True).date()
            vals_line['name'] = line[1] + ' : ' + line[2] + ' : ' + line[3]
            vals_line['ref'] = line[4] 
            vals_line['note'] = line[1] + ' : ' + line[2] 
            
            #TODO: Separador de decimales, y decenas
            if line[6] and float(line[6].replace(',', '')) != 0:
               vals_line['amount'] =  float(line[6].replace(',', ''))*-1
            elif line[7] and float(line[7].replace(',', '')) != 0:
               vals_line['amount'] =  float(line[7].replace(',', ''))

            total +=  vals_line['amount']  
            transactions.append(vals_line)
            vals_line = {}

        _logger.debug('JC total %s',total)
        _logger.debug('JC transactions %s',transactions)    
        
        # initialize a new statement
        #statement = {
        #    'name'              : account + '-' + st.statement + '-' + st.information,
        #    'date'              : st.end_balance.date,
        #    'balance_start'     : st.start_balance.amount,
        #    'balance_end_real'  : st.end_balance.amount,
        #    'transactions'      : []
        #}


        vals_bank_statement.update({
            'balance_end_real': total,
            'transactions': transactions
        })
        #return currency, account, statements
        return None, None, [vals_bank_statement]

    def _complete_stmts_vals(self, stmt_vals, journal_id, account_number):
        """Match partner_id if hasn't been deducted yet."""
        res = super(ImportarFormatoBancoLoja, self)._complete_stmts_vals(
            stmt_vals, journal_id, account_number,
        )
        # doesn't provide account numbers (normal behaviour is to
        # provide 'account_number', which the generic module uses to find
        # the partner), we have to find res.partner through the name
        partner_obj = self.env['res.partner']
        for statement in res:
            for line_vals in statement['transactions']:
                if not line_vals.get('partner_id') and line_vals.get('name'):
                    partner = partner_obj.search(
                        [('name', 'ilike', line_vals['name'])], limit=1,
                    )
                    line_vals['partner_id'] = partner.id
        return res

    