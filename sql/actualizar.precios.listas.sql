--Actualizar el precio de lista, incluir IVA. Siempre y cuando el producto tenga IVA de Venta. 
UPDATE   product_pricelist_item pro_lis
SET fixed_price = pro_lis.fixed_price / 1.14
where 
exists (select * from  product_product pro, product_taxes_rel tax_rel,
account_tax tax  where 
pro.id = tax_rel.prod_id 
and tax_rel.tax_id = tax.id
and tax.type_ec = 'vat'
--and tax.id = 1 --Impuesto Fijo
and pro_lis.product_tmpl_id = pro.product_tmpl_id);



--Lista de Productos que posee Impuesto de Venta tipo IVA
select pro.id,pro.name_template,pro.product_tmpl_id,tax.name,tax.amount from 
product_product pro, product_taxes_rel tax_rel,
account_tax tax where 
pro.id = tax_rel.prod_id 
and tax_rel.tax_id = tax.id
and tax.type_ec = 'vat';

--Impuestos Venta/Cliente
select * from product_taxes_rel;

--Impuestos Compra/Proveedores
select * from product_supplier_taxes_rel;

--Tax (impuestos)
--amount (monto del impuesto)
--amount_tipo (tipo del impuesto fijo, o porcentaje)
select amount,* from account_tax tax
where type_ec = 'vat';




--Listado de productos, con lista de precios
select pro.id,pro.name_template,pro_tem.name,pro_tem.list_price, pro_lis.fixed_price,pro_lis.min_quantity,
list.name from 
product_product pro,
product_template pro_tem, 
product_pricelist_item pro_lis,
product_pricelist list
where 
pro.product_tmpl_id = pro_tem.id
and pro_tem.id = pro_lis.product_tmpl_id
and pro_lis.pricelist_id = list.id
order by pro.id;


--Productos Template
--Categoria
--Precio de Venta (List_price)
--Tipo
--Nombre 
select * from product_template pro_tem;

--Productos (Nombres. Referencia Producto Template)
select * from product_product pro;

--Lista asociada productos. (Precios)
--Precio (fixed_price)
--Cantidad Minima (min_quantity)
--applied_on (product). Si el precio es aplicado a un producto
--product_tmpl_id (producto template id) a que producto se aplico la lista de precios
--compute_price (forma de aplicar el precio). fijo (fixed) formula (formula)
--date_start (fecha desde donde se aplica)
--date_end (fecha hasta que aplica la lista)
select * from product_pricelist_item;

---Lista de precios (
 select * from product_pricelist;