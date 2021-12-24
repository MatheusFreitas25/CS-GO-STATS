CREATE DATABASE CSGO_STATS

CREATE TABLE "ALL_EVENTS" (
--"event_id" INT PRIMARY KEY IDENTITY(1,1),
"lineno" INT,
"time" DATETIME,
moment VARCHAR(100),
mapnumber INT,
"round" INT,
map_name VARCHAR(100),
match_id VARCHAR(255),
"type" VARCHAR(255),
author_name VARCHAR(255),
author_id VARCHAR(255),
author_side VARCHAR(100),
victim_id VARCHAR(255),
victim_name VARCHAR(255),
victim_side VARCHAR(100),
weapon VARCHAR(255),
damage INT,
blinded_time NUMERIC(5, 2),
flashbang_id INT,
damage_armor INT,
victim_health INT,
victim_armor INT,
hitgroup VARCHAR(255),
hs INT,
penetrated INT,
throughsmoke INT,
author_coord VARCHAR(255),
victim_coord VARCHAR(255)

PRIMARY KEY ("time", match_id, "type", "author_id", "lineno")
)