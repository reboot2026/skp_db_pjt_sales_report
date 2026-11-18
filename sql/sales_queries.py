GET_YEARS = """
select distinct Year(o.order_dttm) as ORDER_YEAR
 from `ORDER` o 
order by 1 
"""

CATEGORY_MONTHLY_SALES = """
with base_data as (
	select p.catg_cd
		  ,Month(o.order_dttm) 				as mnth
		  ,sum(d.qty * p.product_price)		as order_amt 
	from `ORDER` o
		 inner join ORDER_DESC d
				 on d.order_id = o.order_id 
		 inner join PRODUCT p 
				 on p.product_id = d.product_id 
	where 1=1
      and o.order_dttm >= %(start_date)s 
      and o.order_dttm <  %(end_date)s
	group by mnth, p.catg_cd
)
select cc.cd_name 	as 카테고리
      ,bd.mnth  	as 월
      ,bd.order_amt	as 매출금액
 from base_data bd
	  inner join CD_CMMN cc 
			  on cc.cd = bd.catg_Cd
where 1=1
"""


CATEGORY_PRODUCT_AVG_PRICE = """
SELECT c.cd_name 						as 카테고리 
	  ,count(distinct p.product_id) 	as 상품수 
      ,round(avg(p.product_price),0) 	as 평균가 
  FROM PRODUCT p
	   inner join CD_CMMN c
			   on c.cd = p.catg_cd 
WHERE 1=1
group by c.cd_name
"""

CATEGORY_TOP2_PRODUCT = """
 with category_order_qty as (
	select 
		  p.catg_cd
		 ,c.cd_name 	as catg_nm
         ,p.product_id	
         ,p.product_name 
		 ,cast(sum(od.qty) as signed)	as order_qty  
	from ORDER_DESC od
	 	 inner join `ORDER` o 
	 			 on o.order_id = od.order_id 
		 inner join PRODUCT p
				 on p.product_id = od.product_id 
		 inner join CD_CMMN c 
				 on c.cd = p.catg_cd 
	where 1=1
      and o.order_dttm >= %(start_date)s  
      and o.order_dttm <  %(end_date)s  
	group by p.catg_cd
			,c.cd_name
            ,p.product_id
            ,p.product_name 
), category_order_qty_rn as (
	select catg_cd
		  ,catg_nm
		  ,product_id
		  ,product_name 
          ,order_qty
		  ,row_number() over (partition by catg_cd 
          						  order by order_qty desc
                                  	  , product_name
                                      , product_id) as rn 
	 from category_order_qty
)
select catg_nm			as 카테고리
	  ,product_name		as 상품명
      ,order_qty		as 판매수량
      ,rn 				as 순위
 from category_order_qty_rn
where rn <= 2 
order by catg_nm, rn 
"""
