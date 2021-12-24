WITH PLAYER_ROUND AS (

select mapnumber
	 , "round"
	 , author_id
	 , map_name
	 , max(author_name) nome
	 , sum(case when "type" = 'threw flashbang' then 1 else 0 end) flashbangs_usadas
	 , sum(case when "type" = 'blinded' and author_side = victim_side then 1 else 0 end) amigos_cegados
	 , sum(case when "type" = 'blinded' and author_side <> victim_side AND VICTIM_side in ('CT', 'TERRORIST') then 1 else 0 end) inimigos_cegados
	 , sum(case when "type" = 'blinded' and author_side = victim_side then blinded_time else 0 end) amigos_cegados_tempo
	 , sum(case when "type" = 'blinded' and author_side <> victim_side AND VICTIM_side in ('CT', 'TERRORIST') then blinded_time else 0 end) inimigos_cegados_tempo
	 , SUM(case when "type" = 'killed' and author_side = 'CT' and victim_side = 'TERRORIST' then 1 else 0 end) kills_ct
	 , SUM(case when "type" = 'killed' and victim_side = 'CT' and author_side = 'TERRORIST' then 1 else 0 end) kills_tr
	 , COUNT(DISTINCT(case when author_side = 'CT' then "round" else NULL end)) rounds_ct
	 , COUNT(DISTINCT(case when author_side = 'TERRORIST' then "round" else NULL end)) rounds_tr
	 , SUM(case when "type" = 'killed' and victim_side <> author_side and throughsmoke = 1 then 1 else 0 end) kills_smoke
	 , SUM(case when "type" = 'Got_The_Bomb' then 1 else 0 end) pegou_c4
	 , SUM(case when "type" = 'Dropped_The_Bomb' then 1 else 0 end) c4_dropada
	 , SUM(case when "type" = 'Bomb_Begin_Plant' then 1 else 0 end) tentativa_plantar
	 , SUM(case when "type" = 'Planted_The_Bomb' then 1 else 0 end) plantou

from ALL_EVENTS
where mapnumber > 0
and "round" > 0
and author_side in ('CT', 'TERRORIST')
group by mapnumber
	 , "round"
	 , author_id
	 , map_name
)





select author_id
	 , nome
	 , mapnumber
	 , map_name
	 , sum(flashbangs_usadas) bangs
	 , sum(amigos_cegados) amigos_cegados
	 , sum(inimigos_cegados) inimigos_cegados 
	 , sum(amigos_cegados_tempo) amigos_cegados_tempo
	 , sum(inimigos_cegados_tempo) inimigos_cegados_tempo
	 , sum(kills_ct) kills_ct
	 , sum(kills_tr) kills_tr
	 , sum(rounds_ct) rounds_ct
	 , sum(rounds_tr) rounds_tr
	 , sum(kills_smoke) kills_smoke
	 , sum(pegou_c4) pegou_c4
	 , sum(c4_dropada) c4_dropada
	 , sum(tentativa_plantar) tentativa_plantar
	 , sum(plantou) plantou
from PLAYER_ROUND
group by author_id, nome, mapnumber, map_name
having sum(rounds_ct) + sum(rounds_tr) > 5