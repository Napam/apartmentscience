SELECT DATE(_created, '-2 day') FROM preview WHERE _batch = 0

SELECT * FROM preview LIMIT 10

-- DELETE FROM preview WHERE _batch != 0

-- SELECT COUNT(_batch) FROM preview GROUP BY _batch;

-- UPDATE preview
-- SET _created = DATE(_created, '-2 day')
-- WHERE _batch = 0