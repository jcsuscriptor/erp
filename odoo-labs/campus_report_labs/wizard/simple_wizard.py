# -*- coding: utf-8 -*-
# Author: Juan Carlos Saavedra
 

from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class SimpleWizard(models.TransientModel):
    """Simple wizard"""

    _name = "campus.labs.simple.wizard"
    _description = "Simple Wizard"

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)

 
    @api.multi
    def button_action_one(self):
        self.ensure_one()
        _logger.debug('button_action_one. date_from %s. date_to %s',self.date_from,self.date_to) 
        return True


    @api.multi
    def button_action_two(self):
        self.ensure_one()
        _logger.debug('button_action_two. date_from %s. date_to %s',self.date_from,self.date_to) 
        return True
       