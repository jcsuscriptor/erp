from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class campus_cliente(models.Model):
    
    _name = "campus.cliente"

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text()