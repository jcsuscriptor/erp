odoo.define('campus_labs_pos.ejemplo_validar_orden', function (require) {
    "use strict";

    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var core = require('web.core');
    var _t = core._t;

    /*
        Modifica el metodo validate_order del screen PaymentScreenWidget, para verificar
        si la cantidad de lineas de la orden es mayor, si es el caso 
        visualiza mensaje de error
    */
    screens.PaymentScreenWidget.include({
        validate_order: function(options) {
            var self = this;
            var order = this.pos.get_order();
            
            //El valor se puede obtener desde configuracion
            if (order.get_orderlines().length > 2) {
                this.gui.show_popup('error',{
                    'title': _t('Cantidad Maxima de Lineas.'),
                    'body':  _t('No se puede seleccionar mas de 2 Productos'),
                });
                return;
            }
            
            return this._super(options);
        }
    });
 

});
