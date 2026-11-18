/*
문제 1. 카테고리별 상품 수와 평균 가격
PRODUCT.catg_cd 는 CD_CMMN.cd(catg001~005) 를 네이밍 규칙으로 참조한다.
카테고리 코드 대신 카테고리명을 표시하고, 카테고리별 등록 상품 수와 평균 판매가를 구하
라. 평균가는 반올림하여 정수로 표시한다.
*/

select p.catg_cd
	  ,c.cd_name as catg_nm 
	  ,count(distinct p.product_id) 	as 상품수
      ,round(avg(p.product_price), 0)	as 평균단가 
 from PRODUCT p 
	  inner join CD_CMMN c
			  on c.cd = p.catg_cd 
where 1=1
group by p.catg_cd, c.cd_name
;


/*
문제 2. 회원 등급별 회원 수와 총 주문금액
MEMBER.grad_cd(grad001~004) 를 CD_CMMN 과 조인해 등급명을 표시하고, 등급별 회원 수
와 해당 등급 회원들이 발생시킨 총 주문금액 합계를 구하라.
주문이 하나도 없는 회원이 있어도 등급별 "회원 수" 집계에서는 제외되면 안 된다.
*/

select m.grad_cd
	  ,g.cd_name 						as grad_nm
      ,count(distinct m.member_id)		as 회원수
      ,count(distinct o.member_id)		as 주문회원수 
      ,sum(o.order_amont) 				as 주문금액
      ,count(distinct o.order_id)		as 주문건수
 from MEMBER m
	  inner join CD_CMMN g
			  on g.cd = m.grad_cd
	  left  join `ORDER` o
			  on o.member_id = m.member_id
where 1=1
group by m.grad_cd
 ;
 
/* 
select 'MEMBER', count(distinct member_id) from MEMBER
union all
select 'ORDER', count(distinct member_id) from dt_pjt.ORDER 
*/
/*
문제 3. 회원별 총 주문건수 / 총 주문금액 (미주문 회원 포함)
모든 회원에 대해 총 주문건수와 총 주문금액을 구하고, 주문이 없는 회원은 0으로 표시하라.
결과는 총 주문금액 내림차순으로 정렬한다. 
*/

select * from CD_CMMN where cd like 'stat%'; -- stat001 주문완료/배송중/배송완료/구매확정

select m.member_id
	  ,m.member_name
      ,count(distinct order_id) 	as 주문건수
      ,sum(o.order_amont) 			as 주문금액
  from MEMBER m
	   left join `ORDER` o
			  on m.member_id = o.member_id
where 1=1
group by m.member_id
	    ,m.member_name 
order by 주문금액 desc 
;

/*
문제 4. 특정 주문의 상태 변경 이력 조회
order_id = 1001 주문이 지금까지 어떤 상태를 거쳐왔는지, 상태명과 함께 시작 시각(start_dttm)
순으로 출력하라.
*/

select oh.start_dttm, sc.cd_name
 from ORDER_STAT_HISTORY oh
	  inner join CD_CMMN sc
			  on sc.cd = oh.stat_cd 
where oh.order_id = 1001
order by start_dttm 
;


/*
문제 5. 배송중(stat002) 단계 소요 시간 분석
이미 배송중 단계를 지나간(end_dttm 이 채워진) 모든 주문에 대해, 배송중 상태에 머문 시간을
"시간" 단위로 구하고 오래 걸린 순으로 정렬하라.
*/

select *
	  ,timestampdiff(hour, start_dttm, end_dttm) as 배송소요시간 
 from ORDER_STAT_HISTORY oh
where oh.stat_cd = 'stat002'
  and oh.end_dttm is not null 
order by 배송소요시간 desc 
;

/*
문제 6. 월별 매출 추이와 전월 대비 증감률
월별 주문 건수, 매출 합계를 구하고, 윈도우 함수를 이용해 전월 대비 매출 증감률(%)을 함께
표시하라.
*/

with monthly_sales as (
	select date_format(o.order_dttm, '%Y-%m') 	as mnth
		  ,count(distinct o.order_id)			as ordr_cnt
		  ,sum(o.order_amont)					as ordr_amt
	from `ORDER` o
	where 1=1
	group by mnth
), monthly_sales_with_prvs as (
	select mnth 									as 월
		  ,ordr_cnt 								as 주문건수
		  ,ordr_amt									as 당월
		  ,lag(ordr_amt) over (order by mnth) 		as 전월 
		  ,ordr_amt 
			- lag(ordr_amt) over (order by mnth)	as 증감 
	from monthly_sales 
)
select 월
	  ,주문건수
      ,당월
      ,전월
      ,증감
      ,case when ifnull(전월, 0) = 0 
			then 0
			else concat(round((증감 / 전월) * 100,1), '%') 
		end 증감률
  from monthly_sales_with_prvs 
;

/*
문제 7. 카테고리별 판매 수량 TOP 2 상품
ORDER_DESC 의 qty 를 상품별로 합산한 뒤, 카테고리별로 판매 수량이 많은 상위 2개 상품만
추출하라.
*/
with category_order_qty as (
	select 
		  p.catg_cd
		 ,c.cd_name 	as catg_nm
         ,p.product_id	
         ,p.product_name 
		 ,sum(od.qty)	as order_qty  
	from ORDER_DESC od
		 inner join PRODUCT p
				 on p.product_id = od.product_id 
		 inner join CD_CMMN c 
				 on c.cd = p.catg_cd 
	where 1=1
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
select catg_nm
	  ,product_name
      ,order_qty
      ,rn 			as top
 from category_order_qty_rn
where rn <= 2 
order by catg_nm, rn 
;

/*
문제 8. 주문 이력이 전혀 없는 회원 조회
가입 후 한 번도 주문한 적 없는 회원의 회원번호와 이름을 조회하라.
*/

select m.member_id
	  ,m.member_name 
 from MEMBER m
	  left join `ORDER` o
			 on m.member_id = o.member_id
where 1=1
  and o.member_id is null  -- 주문 없는 회원 없음  
 ;
  
-- insert into MEMBER( member_name, grad_cd, join_dttm) values ('무주문', 'grad004', now())

/*
문제 9. 장기 미처리 주문 탐지
현재 상태가 '주문완료(stat001)' 이면서, 그 상태로 진입한 지 3일 이상 지난(=아직 배송 준비가
시작되지 않은) 주문을 찾아라.
*/

select o.*, h.*
      ,datediff(now(), start_dttm) as days 
 from `ORDER` o
	  inner join ORDER_STAT_HISTORY h
			  on o.order_id = h.order_id 
where 1=1 
  and o.stat_cd = 'stat001'
  and h.end_dttm is null 
  and datediff(now(), start_dttm) >= 3 
  ;

/*
문제 10. 회원 등급별 최다 구매 회원(등급 내 1 위) 조회
회원 등급별로 총 구매금액을 구하고, 등급 내에서 구매금액이 가장 높은 회원 1명씩만 추출하
라.
*/
with grad_member_order_amt as ( 
	select 
		   m.grad_cd
		  ,m.member_id 
		  ,m.member_name 
          ,sum(o.order_amont) as order_amt 
	 from MEMBER m
		  left  join `ORDER` o
				  on o.member_id = m.member_id 
	where 1=1
	group by m.grad_cd
		  ,m.member_id 
		  ,m.member_name
) , grad_member_amt_with_rnk as (
	select  
		   grad_cd
		  ,member_id
		  ,member_name
		  ,order_amt
		  ,row_number() over (partition by grad_cd order by order_amt desc) as rn
		  ,sum(order_amt) over (partition by grad_cd) as grad_order_amt 
	 from grad_member_order_amt
 ) 
select r.grad_cd
	  ,c.cd_name as grad_nm 
	  ,r.member_id
      ,r.member_name
      ,r.order_amt as member_order_amt
      ,r.grad_order_amt 
 from grad_member_amt_with_rnk r 
	  inner join CD_CMMN c 
			  on c.cd = r.grad_cd 
where rn = 1 
;

/*
grad001	1497000
grad002	3221000
grad003	2545000
grad004	1774000


select m.grad_cd
	  ,sum(o.order_amont) as order_amt 
from dt_pjt.ORDER o
	 inner join MEMBER m
			 on m.member_id = o.member_id
where 1=1
group by m.grad_cd
;

*/ 

/*
select m.grad_cd, m.member_id
	  ,sum(o.order_amont) as order_amt 
from dt_pjt.ORDER o
	 inner join MEMBER m
			 on m.member_id = o.member_id
where 1=1
 -- and m.grad_cd = 'grad003'
group by m.grad_cd, m.member_id
order by m.grad_cd, order_amt desc 
;
*/

