-- this query takes from the CSV created by my collab file_predictions.csv
-- and moves to the standart sqlite table images_predicted. file_predictions
-- has to be imported from CSV for this to work

INSERT INTO images_predicted (image_id, real, predicted, success, filename)
SELECT SUBSTR(
	SUBSTR(field1, 0, INSTR(field1, '.')),
	INSTR(field1,'/') + 1),
field2, field3,
CASE field2 = field3 WHEN 1 THEN 'T' ELSE 'F' END, field1

FROM file_predictions
