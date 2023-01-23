--1
SELECT m.especialidade, t.mes, t.ano, COUNT(*) as numero_de_analises
FROM (f_analise f INNER JOIN medico m ON f.id_medico=m.num_cedula) INNER JOIN d_tempo t ON t.id_tempo=f.id_data_registo
WHERE f.nome='glicémia' AND t.ano BETWEEN '2017' AND '2020'
GROUP BY 
   CUBE(m.especialidade, t.mes, t.ano)
ORDER BY m.especialidade, t.mes, t.ano;

--2
(SELECT p.substancia, c.nome, t.dia_da_semana, t.mes, SUM(p.quant) AS quantidade_total, COUNT(*)::DECIMAL(5,1)/(SELECT COUNT(*) FROM d_tempo WHERE 
	trimestre='1' AND ano='2020' AND dia_da_semana=t.dia_da_semana AND mes=t.mes) AS nr_medio_presc_diario
FROM d_tempo t JOIN f_presc_venda p ON t.id_tempo=p.id_data_registo JOIN d_instituicao i ON p.id_inst = i.id_inst 
	JOIN concelho c ON (c.num_regiao=i.num_regiao AND c.num_concelho = i.num_concelho) JOIN regiao r ON r.num_regiao = i.num_regiao
WHERE t.trimestre = 1 AND t.ano= 2020 AND r.nome = 'Lisboa'
GROUP BY p.substancia, c.nome, t.dia_da_semana, t.mes)
UNION
(SELECT p.substancia, c.nome, t.dia_da_semana, null, SUM(p.quant) AS quantidade_total, COUNT(*)::DECIMAL(5,1)/(SELECT COUNT(*) FROM d_tempo WHERE
    trimestre='1' AND ano='2020' AND dia_da_semana=t.dia_da_semana)  AS nr_medio_presc_diario
FROM d_tempo t JOIN f_presc_venda p ON t.id_tempo=p.id_data_registo JOIN d_instituicao i ON p.id_inst = i.id_inst 
	JOIN concelho c ON (c.num_regiao=i.num_regiao AND c.num_concelho = i.num_concelho) JOIN regiao r ON r.num_regiao = i.num_regiao
WHERE t.trimestre = 1 AND t.ano= 2020 AND r.nome = 'Lisboa'
GROUP BY p.substancia, c.nome, t.dia_da_semana)
UNION
(SELECT p.substancia, c.nome,null, null, SUM(p.quant) AS quantidade_total, COUNT(*)::DECIMAL(5,1)/(SELECT COUNT(*) FROM d_tempo WHERE 
	trimestre='1' AND ano='2020') AS nr_medio_presc_diario
FROM d_tempo t JOIN f_presc_venda p ON t.id_tempo=p.id_data_registo JOIN d_instituicao i ON p.id_inst = i.id_inst 
	JOIN concelho c ON (c.num_regiao=i.num_regiao AND c.num_concelho = i.num_concelho) JOIN regiao r ON r.num_regiao = i.num_regiao
WHERE t.trimestre = 1 AND t.ano= 2020 AND r.nome = 'Lisboa'
GROUP BY p.substancia, c.nome)
UNION
(SELECT p.substancia, null,null, null, SUM(p.quant) AS quantidade_total, COUNT(*)::DECIMAL(5,1)/(SELECT COUNT(*) FROM d_tempo WHERE 
	trimestre='1' AND ano='2020') AS nr_medio_presc_diario
FROM d_tempo t JOIN f_presc_venda p ON t.id_tempo=p.id_data_registo JOIN d_instituicao i ON p.id_inst = i.id_inst 
	JOIN concelho c ON (c.num_regiao=i.num_regiao AND c.num_concelho = i.num_concelho) JOIN regiao r ON r.num_regiao = i.num_regiao
WHERE t.trimestre = 1 AND t.ano= 2020 AND r.nome = 'Lisboa'
GROUP BY p.substancia)
ORDER BY substancia, nome, dia_da_semana, mes;


--2  alternativa com médias apenas nos dias em que há prescrições
SELECT p.substancia, c.nome, t.dia_da_semana, t.mes, SUM(p.quant) AS quantidade_total, COUNT(p.id_presc_venda)::DECIMAL(5,1)/COUNT(DISTINCT t.id_tempo) AS nr_medio_presc_diario
FROM d_tempo t JOIN f_presc_venda p ON t.id_tempo=p.id_data_registo JOIN d_instituicao i ON p.id_inst = i.id_inst 
	JOIN concelho c ON (c.num_regiao=i.num_regiao AND c.num_concelho = i.num_concelho) JOIN regiao r ON r.num_regiao = i.num_regiao
WHERE t.trimestre = 1 AND t.ano= 2020 AND r.nome = 'Lisboa'
GROUP BY p.substancia, ROLLUP(c.nome, t.dia_da_semana, t.mes)
ORDER BY substancia, nome, dia_da_semana, mes;

