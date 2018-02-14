odoo.define('campus_labs_pos.ejemplo_agregar_campo', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var gui = require('point_of_sale.gui');
    
    var Model = require('web.DataModel');


    var _t = core._t;

    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            
            var partner_model = _.find(this.models, function(model){ return model.model === 'res.partner'; });
            partner_model.fields.push('ced_ruc');
            partner_model.fields.push('type_ced_ruc');
             
            return _super_posmodel.initialize.call(this, session, attributes);
        }
         
    });  
 

    
    screens.ClientListScreenWidget.include({
       
        save_client_details: function(partner){
          
            var self = this;
        
            var fields = {};
            this.$('.client-details-contents .detail').each(function(idx,el){
                fields[el.name] = el.value;
            });

            if (!fields.name) {
                this.gui.show_popup('error',_t('A Customer Name Is Required'));
                return;
            }

            if (!fields.type_ced_ruc) {
                this.gui.show_popup('error',_t('Tipo ID es requerido'));
                return;
            }

            if (!fields.ced_ruc) {
                this.gui.show_popup('error',_t('Cedula/ RUC es requerido'));
                return;
            }

            if (this.uploaded_picture) {
                fields.image = this.uploaded_picture;
            }

            fields.id           = partner.id || false;
            fields.country_id   = fields.country_id || false;
            fields.barcode      = fields.barcode || '';

            //TODO: Se puede llamar  a las validaciones de Identificacion. Cedula, RUC
            //Pero tambien existe una validacion a nivel de base de datos, de clave unica (ced_ruc,type_ced_ruc,tipo_persona,company_id)
            //Para no hacer varias llamadas, llamar directamente create_from_ui
            /*
             new Model('res.partner').call('check_ced_ruc', [fields.type_ced_ruc,fields.ced_ruc] ).then(function(result){
                if (!result){
                   
                }else{
 
                }
            });
            */

            new Model('res.partner').call('create_from_ui',[fields]).then(function(partner_id){
                   self.saved_client_details(partner_id);
                },function(err,event){
                    event.preventDefault();
                    var _msg = _t('Your Internet connection is probably down.');
                    if (err.data !== undefined && err.data.message !== undefined) {
                        _msg = err.data.message;
                    }        

                    self.gui.show_popup('error',{
                        'title': _t('Error: Could not Save Changes'),
                        'body': _msg,
                    });
           });    

        } 
    });

     

    var PosDB = require('point_of_sale.DB');
    PosDB.include({
        /**Permitir buscar partner por ced_ruc */
        _partner_search_string: function(partner){
                    
                    var str =  partner.name;
                    if(partner.ced_ruc){
                        str += '|' + partner.ced_ruc;
                    }
                    if(partner.barcode){
                        str += '|' + partner.barcode;
                    }
                    if(partner.address){
                        str += '|' + partner.address;
                    }
                    if(partner.phone){
                        str += '|' + partner.phone.split(' ').join('');
                    }
                    if(partner.mobile){
                        str += '|' + partner.mobile.split(' ').join('');
                    }
                    if(partner.email){
                        str += '|' + partner.email;
                    }
                    str = '' + partner.id + ':' + str.replace(':','') + '\n';
                    return str;
         } 
    });
 
    return PosDB;
   
 
});
