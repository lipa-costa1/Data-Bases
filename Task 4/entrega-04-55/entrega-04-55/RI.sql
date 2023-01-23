--RI-100
CREATE OR REPLACE FUNCTION ri_100() RETURNS TRIGGER AS
$$
DECLARE
	total INTEGER;
BEGIN
	SELECT COUNT(*) INTO total
	FROM consulta c
	WHERE c.num_cedula = new.num_cedula AND EXTRACT(WEEK FROM new.data) = EXTRACT(WEEK FROM c.data) 
	AND EXTRACT(YEAR FROM new.data) = EXTRACT(YEAR FROM c.data) AND new.nome_instituicao = c.nome_instituicao;
	IF total > 100 THEN
		RAISE EXCEPTION 'O médico com nº de cédula % já realizou 100 consultas na semana % de % na instituição %.',
		new.num_cedula, EXTRACT(WEEK FROM new.data), EXTRACT(YEAR FROM new.data), new.nome_instituicao;
	END IF;
	RETURN new;
END;
$$
LANGUAGE plpgsql;	

DROP TRIGGER IF EXISTS insert_consulta_trigger ON consulta;
CREATE TRIGGER insert_consulta_trigger AFTER INSERT ON consulta 
  FOR EACH ROW EXECUTE PROCEDURE ri_100();

DROP TRIGGER IF EXISTS update_consulta_trigger ON consulta;
CREATE TRIGGER update_consulta_trigger AFTER UPDATE ON consulta 
  FOR EACH ROW EXECUTE PROCEDURE ri_100();


--RI-analise
CREATE OR REPLACE FUNCTION ri_analise() RETURNS TRIGGER AS
$$
DECLARE
	esp VARCHAR(50);
BEGIN
	IF new.num_cedula IS NOT NULL THEN 
		SELECT especialidade INTO esp
		FROM medico m WHERE m.num_cedula = new.num_cedula;
		IF new.especialidade != esp THEN
			RAISE EXCEPTION 'A especialidade da análise deve ser igual à do médico da consulta.';
		END IF;
	END IF;
	RETURN new;	
END;
$$
LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS insert_analise_trigger ON analise;
CREATE TRIGGER insert_analise_trigger AFTER INSERT ON analise 
  FOR EACH ROW EXECUTE PROCEDURE ri_analise();
  
DROP TRIGGER IF EXISTS update_analise_trigger ON analise;
CREATE TRIGGER update_analise_trigger AFTER UPDATE ON analise 
  FOR EACH ROW EXECUTE PROCEDURE ri_analise();