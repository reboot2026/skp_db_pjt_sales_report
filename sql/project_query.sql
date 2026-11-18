-- --------------------------------------- 카테고리별.월별매출현황 
-- --------------------------------------- 카테고리별.월별매출현황 
with base_data as (
	select p.catg_cd
		  -- ,date_format(o.order_dttm, '%Y-%m') 	as mnth
		  ,date_format(o.order_dttm, '%m') 	as mnth
		  ,sum(o.order_amont)					as order_amt 
	from dt_pjt.ORDER o
		 inner join ORDER_DESC d
				 on d.order_id = o.order_id 
		 inner join PRODUCT p 
				 on p.product_id = d.product_id 
	where 1=1
      and o.order_dttm >= '2025-01-01'	-- param (start_date) 
      and o.order_dttm <  '2026-01-01'	-- param (end_date)  
	group by mnth, p.catg_cd
)
select cc.cd_name 	as 카테고리
      ,bd.mnth  	as 월
      ,bd.order_amt	as 매출금액
 from base_data bd
	  inner join CD_CMMN cc 
			  on cc.cd = bd.catg_Cd
where 1=1
;

-- --------------------------------------- 카테고리별.상품수.평균가 
-- --------------------------------------- 카테고리별.상품수.평균가
-- ####  카테고리별 상품 수·평균가
SELECT c.cd_name 						as 카테고리 
	  ,count(distinct p.product_id) 	as 상품수 
      ,round(avg(p.product_price),0) 	as 평균가 
  FROM PRODUCT p
	   inner join CD_CMMN c
			   on c.cd = p.catg_cd 
WHERE 1=1
group by c.cd_name
;


-- --------------------------------------- 카테고리별.상품수.평균가 
-- --------------------------------------- 카테고리별.상품수.평균가
-- ########  카테고리별 판매수량 top 2 상품

 with category_order_qty as (
	select 
		  p.catg_cd
		 ,c.cd_name 	as catg_nm
         ,p.product_id	
         ,p.product_name 
		 ,sum(od.qty)	as order_qty  
	from ORDER_DESC od
	 	 inner join dt_pjt.ORDER o 
	 			 on o.order_id = od.order_id 
		 inner join PRODUCT p
				 on p.product_id = od.product_id 
		 inner join CD_CMMN c 
				 on c.cd = p.catg_cd 
	where 1=1
      and o.order_dttm >= '2025-01-01'	-- param (start_date) 
      and o.order_dttm <  '2026-01-01'	-- param (end_date)  
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
		  ,row_number() over (partition by catg_cd order by order_qty desc) as rn 
	 from category_order_qty
)
select catg_nm			as 카테고리
	  ,product_name		as 상품명
      ,order_qty		as 판매수량
      ,rn 				as top
 from category_order_qty_rn
where rn <= 2 
order by catg_nm, rn 
;





