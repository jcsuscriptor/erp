--Cctualizar valores de venta que estan incluidos el IVA, para excluir el IVA.
update product_template pro
set  list_price =   pro.list_price / (select   (1+ (tax.amount/100)) from product_taxes_rel tax_rel,
account_tax tax where pro.id = tax_rel.prod_id 
and tax_rel.tax_id = tax.id
and tax.type_ec = 'vat');


update product_template pro
set  list_price = pro.list_price;


select   (1+ (tax.amount/100)) from product_taxes_rel tax_rel,
account_tax tax where   tax_rel.tax_id = tax.id
and tax.type_ec = 'vat' 

select 0/100 from product_template pro;

select pro.id, pro.list_price, pro.list_price / (1+ (tax.amount/100)) from 
product_template pro, product_taxes_rel tax_rel,
account_tax tax
where pro.id = tax_rel.prod_id 
and tax_rel.tax_id = tax.id
and tax.type_ec = 'vat';

--Tax
select *,amount from account_tax tax
where type_ec = 'vat';

--Productos
select * from product_product pro;

--Impuestos Venta/Cliente
select * from product_taxes_rel;

--Impuestos Compra/Proveedores
select * from product_supplier_taxes_rel;

select list_price,* from product_template;