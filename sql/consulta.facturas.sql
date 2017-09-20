--Facturas de Clientes. 
select par.ced_ruc,par.name,
--inv.id,
-- inv.state,
CASE 
  WHEN  (inv.state = 'paid' or inv.state = 'open') THEN 'emitida'
  WHEN (inv.state ='cancel') THEN 'cancelada'
END AS estado,
--inv.create_date,
inv.date_invoice,
--inv.number,
inv.move_name numero_factura, 
--mov.name,
--inv.amount_total_company_signed,inv.amount_total_signed,
--inv.amount_tax,inv.amount_total,inv.amount_untaxed_signed,inv.base_amount_withholding_rent,
--inv.withholding_rent,
--inv.invoice_total,
--to_char(round(inv.amount_untaxed,4), '999D9999') base_imponible,
round(inv.amount_untaxed,4) base_imponible,
round(inv.base_amount_vat_cero,4)  grabado_iva_0,
round(inv.base_amount_vat,4)  grabado_iva_12,
round(inv.vat,4)  iva,
round(inv.invoice_total,4) total
 
from 
account_invoice inv
inner join res_partner par on inv.partner_id = par.id
left join  account_move mov on inv.move_id = mov.id
where inv.type = 'out_invoice'
--and inv.number = '002-001-000015580'
--and (inv.date_invoice, inv.date_invoice) OVERLAPS ('2017-08-01'::DATE, '2017-08-31'::DATE)
and  inv.date_invoice BETWEEN '2017-08-01' AND '2017-08-31' 
order by move_name;

--1722

--Convertir punto a coma. Redondear a 4 decimales
select 	to_char(round(-7.6000000000000005,4), '999D9999');

Base imponible
	$ 34,56
Gravado IVA 0%
	$ 33,00
Gravado IVA 14%
	$ 1,56
14% IVA
	$ 0,19
Total
	$ 34,75
	Pagado en 02/08/2017 	$ 34,75
Monto adeudado
	$ 0,00



--Facturas de Clientes, Cruzado con Account_Move (Asientos Contables)
select inv.type,inv.state,inv.number,inv.move_name, mov.name, mov.id from 
account_invoice inv
left join  account_move mov on inv.move_id = mov.id
where inv.type = 'out_invoice'
order by move_name;


select * from  account_move mov ;


--Facturas Borrador
select  inv.move_id,inv.date_invoice,* from account_invoice inv
where state = 'draft';


--Estados de Facturas. Totales

--open
--draft
--paid
--cancel
select state,count(*) from 
account_invoice inv
group by inv.state;

select * from account_invoice;