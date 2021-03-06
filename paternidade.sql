WITH round_info as (
select "match_id"
	 , mapnumber
	 , "round"
	 , "map_name"
	 , min("time") inicio
	 , max("time") fim
	 , DATEDIFF(ss, min("time"), max("time")) duracao
	 , sum(case when "type" = 'Defused_The_Bomb' then 1 else 0 end) bomb_defused
	 , sum(case when "type" = 'Planted_The_Bomb' then 1 else 0 end) bomb_planted
	 , sum(case when "type" in ('SFUI_Notice_Terrorists_Win', 'SFUI_Notice_Target_Bombed') then 1 else 0 end) t_win
	 , sum(case when "type" in ('SFUI_Notice_CTs_Win', 'SFUI_Notice_Bomb_Defused', 'SFUI_Notice_Target_Saved') then 1 else 0 end) ct_win
	 , sum(case when author_side = 'CT' and "type" = 'left buyzone' then equipment_value else 0 end) equipment_value_ct
	 , sum(case when author_side = 'TERRORIST' and "type" = 'left buyzone' then equipment_value else 0 end) equipment_value_tr
from ALL_EVENTS
group by "match_id"
	 , mapnumber
	 , "round"
	 , "map_name"
	),

PLAYER_ROUND_AUTHOR AS (

select p.mapnumber
     , p.match_id
	 , p."round"
	 , p.author_id
	 , p.map_name
	 , max(author_name) nome
	 , sum(case when "type" = 'threw flashbang' then 1 else 0 end) flashbangs_usadas
	 , COUNT(DISTINCT(case when "type" = 'blinded' and author_side <> victim_side AND VICTIM_side in ('CT', 'TERRORIST') then flashbang_id else NULL end)) flash_cegou_inimigo
	 , COUNT(DISTINCT(case when "type" = 'blinded' and author_side = victim_side then flashbang_id else NULL end)) flash_cegou_amigo
	 , sum(case when "type" = 'blinded' and author_side = victim_side then 1 else 0 end) amigos_cegados
	 , sum(case when "type" = 'blinded' and author_side <> victim_side AND VICTIM_side in ('CT', 'TERRORIST') then 1 else 0 end) inimigos_cegados
	 , sum(case when "type" = 'blinded' and author_side = victim_side then blinded_time else 0 end) amigos_cegados_tempo
	 , sum(case when "type" = 'blinded' and author_side <> victim_side AND VICTIM_side in ('CT', 'TERRORIST') then blinded_time else 0 end) inimigos_cegados_tempo
	 , SUM(case when "type" = 'killed' and author_side = 'CT' and victim_side = 'TERRORIST' then 1 else 0 end) kills_ct
	 , SUM(case when "type" = 'killed' and author_side = 'CT' and equipment_value_tr < 7000 and not p."round" in (1, 16) then 1 else 0 end) kills_eco_ct
	 , COUNT(DISTINCT(case when equipment_value_tr < 7000 and author_side = 'CT' and not p."round" in (1, 16) then CONCAT(r.match_id, '|', r.mapnumber, '|', r."round")
						   when equipment_value_ct < 7000 and author_side = 'TERRORIST' and not p."round" in (1, 16) then CONCAT(r.match_id, '|', r.mapnumber, '|', r."round")
						   else NULL end)) eco_inimigo
	 , SUM(case when "type" = 'killed' and victim_side = 'CT' and author_side = 'TERRORIST' then 1 else 0 end) kills_tr
	 , SUM(case when "type" = 'killed' and author_side = 'TERRORIST' and equipment_value_ct < 7000 and not p."round" in (1, 16) then 1 else 0 end) kills_eco_tr
	 , SUM(case when "type" = 'assisted killing' and author_side = 'CT' and victim_side = 'TERRORIST' then 1 else 0 end) assists_ct
	 , SUM(case when "type" = 'assisted killing' and victim_side = 'CT' and author_side = 'TERRORIST' then 1 else 0 end) assists_tr
	 , COUNT(DISTINCT(CONCAT(r.match_id, '|', r.mapnumber, '|', r."round"))) rounds
	 , COUNT(DISTINCT(case when author_side = 'CT' then CONCAT(r.match_id, '|', r.mapnumber, '|', r."round") else NULL end)) rounds_ct
	 , COUNT(DISTINCT(case when author_side = 'TERRORIST' then CONCAT(r.match_id, '|', r.mapnumber, '|', r."round") else NULL end)) rounds_tr
	 , SUM(case when "type" = 'killed' and victim_side <> author_side and throughsmoke = 1 then 1 else 0 end) kills_smoke
	 , SUM(case when "type" = 'killed' and victim_side <> author_side and weapon like '%knife%' then 1 else 0 end) kills_faca
	 , SUM(case when "type" = 'Got_The_Bomb' then 1 else 0 end) pegou_c4
	 , SUM(case when "type" = 'Dropped_The_Bomb' then 1 else 0 end) c4_dropada
	 , SUM(case when "type" = 'Bomb_Begin_Plant' then 1 else 0 end) tentativa_plant_c4
	 , SUM(case when "type" = 'Planted_The_Bomb' then 1 else 0 end) plantou_c4
	 , SUM(case when "type" = 'attacked' and weapon not in ('flashbang', 'hegrenade', 'inferno') then 1 else 0 end) tiros_acertados
	 , SUM(case when "type" = 'attacked' and weapon not in ('flashbang', 'hegrenade', 'inferno') and hitgroup in ('left leg', 'right leg') then 1 else 0 end) tiros_na_perna
	 , SUM(case when "type" = 'attacked' and weapon not in ('flashbang', 'hegrenade', 'inferno') and hitgroup in ('head') then 1 else 0 end) tiros_na_cabeca
from ALL_EVENTS p
LEFT JOIN round_info r on p.match_id = r.match_id and p.mapnumber = r.mapnumber and p."round" = r."round"
where p.mapnumber > 0
and p."round" > 0
and author_side in ('CT', 'TERRORIST')
group by p.mapnumber
	 , p."round"
	 , p.author_id
	 , p.map_name
	 , p.match_id
),

PLAYER_ROUND_VICTIM AS (

select p.mapnumber
     , p.match_id
	 , p."round"
	 , p.victim_id
	 , p.map_name
	 , max(author_name) nome
	 , sum(case when "type" = 'blinded' and author_side = victim_side then 1 else 0 end) cegado_por_amigos
	 , sum(case when "type" = 'blinded' and author_side <> victim_side AND VICTIM_side in ('CT', 'TERRORIST') then 1 else 0 end) cegado_por_inimigos
	 , sum(case when "type" = 'blinded' and author_side = victim_side then blinded_time else 0 end) cegado_por_amigos_tempo
	 , sum(case when "type" = 'blinded' and author_side <> victim_side AND VICTIM_side in ('CT', 'TERRORIST') then blinded_time else 0 end) cegado_por_inimigos_tempo
	 , SUM(case when "type" = 'killed' and author_side = 'TERRORIST' and victim_side = 'CT' then 1 else 0 end) mortes_ct
	 , SUM(case when "type" = 'killed' and author_side = 'TERRORIST' and equipment_value_tr < 7000 and not p."round" in (1, 16) then 1 else 0 end) mortes_eco_ct
	 , SUM(case when "type" = 'killed' and author_side = 'CT' and victim_side = 'TERRORIST' then 1 else 0 end) mortes_tr
	 , SUM(case when "type" = 'killed' and author_side = 'CT' and equipment_value_ct < 7000 and not p."round" in (1, 16) then 1 else 0 end) mortes_eco_tr
	 , SUM(case when "type" = 'killed' and victim_side <> author_side and throughsmoke = 1 then 1 else 0 end) mortes_smoke
	 , SUM(case when "type" = 'killed' and victim_side <> author_side and weapon like '%knife%' then 1 else 0 end) mortes_faca
	 , SUM(case when "type" = 'attacked' and weapon not in ('flashbang', 'hegrenade', 'inferno') then 1 else 0 end) tiros_tomados
	 , SUM(case when "type" = 'attacked' and weapon not in ('flashbang', 'hegrenade', 'inferno') and hitgroup in ('left leg', 'right leg') then 1 else 0 end) tiros_na_perna_tomados
	 , SUM(case when "type" = 'attacked' and weapon not in ('flashbang', 'hegrenade', 'inferno') and hitgroup in ('head') then 1 else 0 end) tiros_na_cabeca_tomados
from ALL_EVENTS p
LEFT JOIN round_info r on p.match_id = r.match_id and p.mapnumber = r.mapnumber and p."round" = r."round"
where p.mapnumber > 0
and p."round" > 0
and author_side in ('CT', 'TERRORIST')
group by p.mapnumber
	 , p."round"
	 , p.victim_id
	 , p.map_name
	 , p.match_id
)






select p.author_id
	 , p.nome
	 , p.mapnumber
	 , p.map_name
	 , sum(flashbangs_usadas) bangs
	 , sum(flash_cegou_inimigo) flash_cegou_inimigo
	 , sum(flash_cegou_amigo) flash_cegou_amigo
	 , sum(amigos_cegados) amigos_cegados
	 , sum(inimigos_cegados) inimigos_cegados 
	 , sum(amigos_cegados_tempo) amigos_cegados_tempo
	 , sum(inimigos_cegados_tempo) inimigos_cegados_tempo
	 , sum(kills_ct) kills_ct
	 , sum(kills_eco_ct) kills_eco_ct
	 , sum(eco_inimigo) eco_inimigo
	 , sum(kills_tr) kills_tr
	 , sum(kills_eco_tr) kills_eco_tr
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
	 , sum(cegado_por_amigos) cegado_por_amigos
	 , sum(cegado_por_inimigos) cegado_por_inimigos
	 , sum(cegado_por_amigos_tempo) cegado_por_amigos_tempo
	 , sum(cegado_por_inimigos_tempo) cegado_por_inimigos_tempo
	 , sum(mortes_ct) mortes_ct
	 , sum(mortes_eco_ct) mortes_eco_ct
	 , sum(mortes_tr) mortes_tr
	 , sum(mortes_eco_tr) mortes_eco_tr
	 , sum(mortes_smoke) mortes_smoke
	 , sum(mortes_faca) mortes_faca
	 , sum(tiros_tomados) tiros_tomados
	 , sum(tiros_na_perna_tomados) tiros_na_perna_tomados
	 , sum(tiros_na_cabeca_tomados) tiros_na_cabeca_tomados
from PLAYER_ROUND_AUTHOR p
LEFT JOIN PLAYER_ROUND_VICTIM pm on p.mapnumber = pm.mapnumber
								and p.match_id = pm.match_id
							    and p."round" = pm."round"
								and p.author_id = pm.victim_id
group by p.author_id
	 , p.nome
	 , p.mapnumber
	 , p.map_name
having sum(rounds_ct) + sum(rounds_tr) > 5