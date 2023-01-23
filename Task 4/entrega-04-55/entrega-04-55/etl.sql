-- carregar d_tempo
INSERT INTO d_tempo(dia, dia_da_semana, semana, mes, trimestre, ano)
SELECT EXTRACT(DAY FROM s), EXTRACT(DOW FROM s), EXTRACT(WEEK FROM s), EXTRACT(MONTH FROM s), EXTRACT(QUARTER FROM s), EXTRACT(YEAR FROM s) FROM generate_series('2019-01-01', '2021-12-31','1 day'::interval) s;

-- carregar d_instituicao
INSERT INTO d_instituicao(nome, tipo, num_regiao, num_concelho)
SELECT nome, tipo, num_regiao, num_concelho FROM instituicao;

-- carregar f_analise
INSERT INTO f_analise
SELECT a.num_analise, a.num_cedula, a.num_doente, t.id_tempo, i.id_inst, a.nome, a.quant
FROM analise a JOIN d_instituicao i ON a.inst = i.nome 
	JOIN d_tempo t ON (EXTRACT(YEAR FROM a.data_registo) = t.ano AND EXTRACT(MONTH FROM a.data_registo) = t.mes AND EXTRACT(DAY FROM a.data_registo) = t.dia);
	
-- carregar f_presc_venda
INSERT INTO f_presc_venda
SELECT pv.num_venda, pv.num_cedula, pv.num_doente, t.id_tempo, i.id_inst, pv.substancia, vf.quant
FROM prescricao_venda pv JOIN venda_farmacia vf ON pv.num_venda = vf.num_venda
	JOIN d_instituicao i ON vf.inst = i.nome 
	JOIN d_tempo t ON (EXTRACT(YEAR FROM vf.data_registo) = t.ano AND EXTRACT(MONTH FROM vf.data_registo) = t.mes AND EXTRACT(DAY FROM vf.data_registo) = t.dia);