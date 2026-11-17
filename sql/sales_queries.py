
CATEGORY_SALES_SQL = """
with base_data as (
	select p.catg_cd
		  ,date_format(o.order_dttm, '%Y-%m') 	as mnth
          ,o.stat_cd 
          ,count(distinct o.member_id)			as member_cnt
          ,count(distinct d.product_id) 		as product_cnt 
		  ,count(distinct o.order_id)			as order_cnt
		  ,sum(o.order_amont)					as order_amt 
          ,sum(d.qty)							as qty
	from dt_pjt.ORDER o
		 inner join ORDER_DESC d
				 on d.order_id = o.order_id 

		 inner join PRODUCT p 
				 on p.product_id = d.product_id 
	where 1=1
	group by mnth, p.catg_cd, o.stat_cd
)
select bd.catg_cd
	  ,cc.cd_name as catg_nm
      ,bd.mnth 
      ,bd.stat_cd
      ,sc.cd_name as stat_nm 
      ,bd.member_cnt
      ,bd.product_cnt
      ,bd.order_cnt
      ,bd.order_amt
      ,bd.qty
 from base_data bd
	  inner join CD_CMMN cc 
			  on cc.cd = bd.catg_Cd
	  inner join CD_CMMN sc 
			  on sc.cd = bd.stat_cd 
"""


