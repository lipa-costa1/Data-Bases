-- 1:
SELECT c.nome AS concelho
FROM venda_farmacia v, instituicao i, concelho c
WHERE v.inst=i.nome AND i.num_regiao = c.num_regiao AND i.num_concelho = c.num_concelho
AND data_registo = CURRENT_DATE
GROUP BY c.nome 
HAVING sum(preco) >= ALL(   SELECT sum(preco)
						    FROM venda_farmacia v, instituicao i, concelho c
							WHERE v.inst=i.nome AND (i.num_regiao = c.num_regiao AND i.num_concelho = c.num_concelho)
							AND data_registo = CURRENT_DATE
							GROUP BY c.nome);
-- 2:														
SELECT m.nome AS medico, r.nome AS regiao
FROM (prescricao p NATURAL JOIN consulta c NATURAL JOIN medico m) INNER JOIN (instituicao i INNER JOIN regiao r ON i.num_regiao = r.num_regiao) ON c.nome_instituicao = i.nome
WHERE data BETWEEN '2019-01-01' AND '2019-06-30'
GROUP BY m.nome, r.nome
HAVING COUNT(*) >= ALL(SELECT COUNT(*)
	               FROM (prescricao p NATURAL JOIN consulta c NATURAL JOIN medico m) INNER JOIN (instituicao i INNER JOIN regiao r2 ON i.num_regiao = r2.num_regiao) ON c.nome_instituicao = i.nome
	               WHERE r2.nome = r.nome AND data BETWEEN '2019-01-01' AND '2019-06-30'
	               GROUP BY m.nome);
-- 3:
SELECT m.nome AS medico
FROM ((prescricao_venda p INNER JOIN venda_farmacia v on p.num_venda = v.num_venda) NATURAL JOIN medico m) INNER JOIN instituicao i  ON v.inst = i.nome
WHERE EXTRACT(YEAR FROM data_registo)= EXTRACT(YEAR FROM CURRENT_DATE) AND tipo='farmacia' AND num_concelho='4' AND num_regiao='2' AND p.substancia='Aspirina'
GROUP BY m.nome
HAVING COUNT(DISTINCT i.nome) = (SELECT COUNT(DISTINCT i.nome)
                         FROM instituicao i
                         WHERE tipo='farmacia' AND num_concelho='4' AND num_regiao='2');
-- 4:                         
(SELECT num_doente
FROM analise
WHERE EXTRACT(MONTH FROM data) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM data) = EXTRACT(YEAR FROM CURRENT_DATE))
EXCEPT
(SELECT num_doente
FROM prescricao_venda
WHERE EXTRACT(MONTH FROM data) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM data)=EXTRACT(YEAR FROM CURRENT_DATE));