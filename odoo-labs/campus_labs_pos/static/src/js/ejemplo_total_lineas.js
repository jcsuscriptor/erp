odoo.define('campus_labs_pos.ejemplo_total_lineas', function (require) {
    "use strict";

    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var core = require('web.core');
    var _t = core._t;

    
    screens.OrderWidget.include({
        
        update_summary: function(){
        
            var order = this.pos.get_order();
            if (!order.get_orderlines().length) {
                return;
            }

            var total_linea  = order ? order.get_orderlines().length : 0;

            this.el.querySelector('.summary .total .total_lineas .value').textContent = total_linea;

            this._super();
        } 
    });
 

});
