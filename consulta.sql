WITH PLAYER_ROUND AS (

select mapnumber
	 , "round"
	 , author_id
	 , map_name
	 , max(author_name) nome
	 , sum(case when "type" = 'threw flashbang' then 1 else 0 end) flashbangs_usadas
	 , COUNT(DISTINCT(case when "type" = 'blinded' and author_side <> victim_side AND VICTIM_side in ('CT', 'TERRORIST') then flashbang_id else NULL end)) flash_cegou_inimigo
	 , COUNT(DISTINCT(case when "type" = 'blinded' and author_side = victim_side then flashbang_id else NULL end)) flash_cegou_amigo
	 , sum(case when "type" = 'blinded' and author_side = victim_side then 1 else 0 end) amigos_cegados
	 , sum(case when "type" = 'blinded' and author_side <> victim_side AND VICTIM_side in ('CT', 'TERRORIST') then 1 else 0 end) inimigos_cegados
	 , sum(case when "type" = 'blinded' and author_side = victim_side then blinded_time else 0 end) amigos_cegados_tempo
	 , sum(case when "type" = 'blinded' and author_side <> victim_side AND VICTIM_side in ('CT', 'TERRORIST') then blinded_time else 0 end) inimigos_cegados_tempo
	 , SUM(case when "type" = 'killed' and author_side = 'CT' and victim_side = 'TERRORIST' then 1 else 0 end) kills_ct
	 , SUM(case when "type" = 'killed' and victim_side = 'CT' and author_side = 'TERRORIST' then 1 else 0 end) kills_tr
	 , SUM(case when "type" = 'assisted killing' and author_side = 'CT' and victim_side = 'TERRORIST' then 1 else 0 end) assists_ct
	 , SUM(case when "type" = 'assisted killing' and victim_side = 'CT' and author_side = 'TERRORIST' then 1 else 0 end) assists_tr
	 , COUNT(DISTINCT("round")) rounds
	 , COUNT(DISTINCT(case when author_side = 'CT' then "round" else NULL end)) rounds_ct
	 , COUNT(DISTINCT(case when author_side = 'TERRORIST' then "round" else NULL end)) rounds_tr
	 , SUM(case when "type" = 'killed' and victim_side <> author_side and throughsmoke = 1 then 1 else 0 end) kills_smoke
	 , SUM(case when "type" = 'killed' and victim_side <> author_side and weapon like '%knife%' then 1 else 0 end) kills_faca
	 , SUM(case when "type" = 'Got_The_Bomb' then 1 else 0 end) pegou_c4
	 , SUM(case when "type" = 'Dropped_The_Bomb' then 1 else 0 end) c4_dropada
	 , SUM(case when "type" = 'Bomb_Begin_Plant' then 1 else 0 end) tentativa_plant_c4
	 , SUM(case when "type" = 'Planted_The_Bomb' then 1 else 0 end) plantou_c4
	 , SUM(case when "type" = 'attacked' and weapon not in ('flashbang', 'hegrenade', 'inferno') then 1 else 0 end) tiros_acertados
	 , SUM(case when "type" = 'attacked' and weapon not in ('flashbang', 'hegrenade', 'inferno') and hitgroup in ('left leg', 'right leg') then 1 else 0 end) tiros_na_perna
	 , SUM(case when "type" = 'attacked' and weapon not in ('flashbang', 'hegrenade', 'inferno') and hitgroup in ('head') then 1 else 0 end) tiros_na_cabeca

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
	 , sum(flash_cegou_inimigo) flash_cegou_inimigo
	 , sum(flash_cegou_amigo) flash_cegou_amigo
	 , sum(amigos_cegados) amigos_cegados
	 , sum(inimigos_cegados) inimigos_cegados 
	 , sum(amigos_cegados_tempo) amigos_cegados_tempo
	 , sum(inimigos_cegados_tempo) inimigos_cegados_tempo
	 , sum(kills_ct) kills_ct
	 , sum(kills_tr) kills_tr
	 , sum(assists_ct) assists_ct
	 , sum(assists_tr) assists_tr
	 , sum(rounds) rounds
	 , sum(rounds_ct) rounds_ct
	 , sum(rounds_tr) rounds_tr
	 , sum(kills_smoke) kills_smoke
	 , sum(pegou_c4) pegou_c4
	 , sum(c4_dropada) c4_dropada
	 , sum(tentativa_plant_c4) tentativa_plant_c4
	 , sum(plantou_c4) plantou_c4
	 , sum(tiros_acertados) tiros_acertados
	 , sum(tiros_na_perna) tiros_na_perna
	 , sum(tiros_na_cabeca) tiros_na_cabeca
	 , sum(kills_faca) kills_faca
from PLAYER_ROUND
group by author_id, nome, mapnumber, map_name
having sum(rounds_ct) + sum(rounds_tr) > 5