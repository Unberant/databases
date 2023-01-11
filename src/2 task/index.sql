
-- btree
create table strs(
    str varchar,
    str_indexed varchar
);
CREATE INDEX strs_indexed ON strs using btree (str_indexed);

insert into strs SELECT
    md5(random()::text),
    md5(random()::text)
from (
    SELECT * FROM generate_series(1,500000) AS id
) AS ser;

select * from strs order by str desc;
select * from strs order by str_indexed desc;

---- brin
DROP table airport_log;
CREATE TABLE wind_log (
    id int, 
    time_st timestamp without time zone,
    speed int
);

INSERT INTO wind_log
(
    id,
    time_st,
    speed
)
VALUES
(
    round(random()*1000)::int,
    generate_series('2020-01-01'::timestamp,'2022-01-01'::timestamp,'1 second'),
    round(random()*50)::int
);


SELECT AVG(speed)
FROM wind_log
WHERE time_st>='2021-10-15' AND time_st<'2021-10-16';

DROP INDEX IF EXISTS average_speed;
CREATE INDEX average_speed ON wind_log
USING btree (time_st);
--
SELECT AVG(speed)
FROM wind_log
WHERE time_st>='2021-10-15' AND time_st<'2021-10-16';

DROP INDEX IF EXISTS average_speed;
CREATE INDEX average_speed ON wind_log
USING BRIN (time_st) WITH (pages_per_range = 128);
--
SELECT AVG(speed)
FROM wind_log
WHERE time_st>='2021-10-15' AND time_st<'2021-10-16';

