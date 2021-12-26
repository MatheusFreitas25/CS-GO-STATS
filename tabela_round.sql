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
order by "match_id"
	 , mapnumber
	 , "round"




/*
select * from round_info
order by "match_id"
	 , mapnumber
	 , "round"
	 */