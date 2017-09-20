


select ced_ruc,type_ced_ruc,tipo_persona,name,street,city,phone,mobile, customer,supplier,is_company  from res_partner
order by id;


select * from res_partner
where is_company = 't';

--Proveedores
select * from res_partner
where supplier = 't';

--clientes
select * from res_partner
where customer = 't';

select is_company,count(*) from res_partner
group by is_company; 

select company_id,count(*) from res_partner
group by company_id; 

select company_type,count(*) from res_partner
group by company_type; 

--Partner
select * from res_partner; 

