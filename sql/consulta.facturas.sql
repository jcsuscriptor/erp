--Facturas de Clientes, Cruzado con Account_Move (Asientos Contables)
select inv.type,inv.state,inv.number,inv.move_name, mov.name, mov.id from account_invoice inv
left join  account_move mov on inv.move_id = mov.id
where inv.type = 'out_invoice'
order by move_name 