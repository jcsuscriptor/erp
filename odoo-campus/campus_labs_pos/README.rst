Realizar laboratorios, para personalizar POS.
Agregar Validaciones, en la screen "PaymentScreenWidget". Modificando el Metodo "validate_order"
    Validacion si el total de lineas de la orden es mayor a 2.
        Activar: 'static/src/xml/templates.validar.orden.xml' 

Agregar total de lineas, que posee la orden.
    Modificar el screen "OrderWidget", en el Metodo "update_summary"        