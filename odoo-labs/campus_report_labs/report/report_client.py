# -*- coding: utf-8 -*-

from openerp import models, fields, api,tools

import logging
_logger = logging.getLogger(__name__)


class report_client(models.Model):

    _name = "campus.labs.report.client"

    #specify the parameter _auto=False to the odoo model, so no table corresponding to the fields is created automatically.
    _auto = False
    
    name = fields.Char(string="Nombre", readonly = True)
    date = fields.Date(string="Fecha Registro",readonly = True)
    description = fields.Text(string="Descripcion",readonly = True)

    _logger.debug('report_client....') 

    def init(self, cr):
        """ main report 
            El nombre de la vista, debe coincidir con el nombre del modelo. Reemplazar . por _
            Ejemplo: 
                Nombre Modelo: "campus.labs.report.client"
                Nombre Vista: "campus_labs_report_client"
        """
        _logger.debug('report_client.init') 
        
        tools.drop_view_if_exists(cr, 'campus_labs_report_client')
        cr.execute("""  CREATE VIEW campus_labs_report_client AS (
                    select id,name,date,description from campus_cliente
                ) 
                """)