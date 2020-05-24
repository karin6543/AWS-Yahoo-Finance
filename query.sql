SELECT name,high,Datetime,Hour FROM
(SELECT name,ROW_NUMBER() OVER (PARTITION BY name,Hour ORDER BY high DESC)Rank,high,Datetime,Hour
FROM
(SELECT name,high,ts Datetime,split_part(split_part(ts,' ',2),':',1)Hour  
 FROM "finance-db"."16" 
 WHERE  ts LIKE '%2020-05-14%' 
 AND CAST(high AS VARCHAR) NOT LIKE '%NaN%')sq1)sq2
 WHERE Rank=1
 ORDER BY name,Hour,Rank DESC