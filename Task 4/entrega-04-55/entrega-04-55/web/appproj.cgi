#!/usr/bin/python3
# -*- coding: utf-8 -*-

from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template, request
import datetime as d

## Libs postgres
import psycopg2
import psycopg2.extras

app = Flask(__name__)

## SGBD configs
DB_HOST="db.tecnico.ulisboa.pt"
DB_USER="ist192648" 
DB_DATABASE=DB_USER
DB_PASSWORD="yxvz9390"
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)

@app.route("/")
def home():
    return '''<h1>Aplicação Bases de Dados:</h1> <br>
              <h2> <a href="instituicao">Instituições</a> </h2> <br> 
              <h2> <a href="medico">Médicos</a> </h2> <br>
              <h2> <a href="prescricao">Prescrições</a> </h2> <br>
              <h2> <a href="analise">Análises</a> </h2> <br>
              <h2> <a href="venda_farmacia">Venda Farmácia</a> </h2> <br> 
              <h2> <a href="substancias">Substâncias Prescritas</a> </h2> <br>
              <h2> <a href="glicemia">Glicémia</a> </h2> <br> '''
              

#===============================================================================================================================================
@app.route("/venda_farmacia")
def redirectfarmacia():
    return """<h1>Registo de Venda em Farmácia</h1> <br>
              <h2> <a href="venda_farmacia/s_presc">Sem prescrição</a> </h2> <br> 
              <h2> <a href="venda_farmacia/c_presc">Com prescrição</a> </h2>""" + '<br> <a href="./">Voltar</a>'

@app.route("/venda_farmacia/s_presc")
def alter_sale_wout_presc():
    dbConn=None 
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute("SELECT nome from instituicao;")
        insts = cursor.fetchall()
        cursor.execute("SELECT * from prescricao;")
        prescs = cursor.fetchall()
        prescs = map(lambda x: [x, str(x[0])+', '+str(x[1])+', '+x[2].strftime("%Y-%m-%d")+', '+x[3]+', '+str(x[4]) ], prescs) 
        return render_template("s_presc.html", insts=insts, prescs=prescs)
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        dbConn.close()
    
@app.route("/venda_farmacia/s_presc/add", methods=["POST"])
def add_sale_wout_presc():
    dbConn=None 
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = "SELECT MAX(num_venda) FROM venda_farmacia;"
        cursor.execute(query)
        num_venda = str(cursor.fetchone()[0] + 1)
        data_registo = d.date.today().strftime("%Y-%m-%d")
        substancia = request.form["substancia"]
        quant = request.form["quant"]
        preco = request.form["preco"]
        inst = request.form["inst"]
        
        query = "INSERT INTO venda_farmacia VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (num_venda, data_registo, substancia, quant, preco, inst) )
        return '<h3>Venda sem prescrição registada!</h3> <br> <a href="../../venda_farmacia">Voltar</a>'
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()
        
@app.route("/venda_farmacia/c_presc")
def alter_sale_w_presc():
    dbConn=None 
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute("SELECT nome from instituicao;")
        insts = cursor.fetchall()
        cursor.execute("SELECT * from prescricao;")
        prescs = cursor.fetchall()
        prescs = map(lambda x:  str(x[0])+', '+str(x[1])+', '+x[2].strftime("%Y-%m-%d")+', '+x[3]+', '+str(x[4]) , prescs)
        return render_template("c_presc.html", insts=insts, prescs=prescs)
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        dbConn.close()
        
        
@app.route("/venda_farmacia/c_presc/add", methods=["POST"])
def add_sale_w_presc():
    dbConn=None 
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute("SELECT MAX(num_venda) FROM venda_farmacia;")
        num_venda = str(cursor.fetchone()[0] + 1)
        presc = request.form["presc"].split(', ')
        num_cedula = presc[0]
        num_doente = presc[1]
        data = presc[2]
        substancia = presc[3]
        quant = presc[4] 
        data_registo = d.date.today().strftime("%Y-%m-%d")
        preco = request.form["preco"]
        inst = request.form["inst"]
        
        query1 = "INSERT INTO venda_farmacia VALUES (%s, %s, %s, %s, %s, %s)"
        query2 = "INSERT INTO prescricao_venda VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query1, (num_venda, data_registo, substancia, quant, preco, inst) )
        cursor.execute(query2, (num_cedula, num_doente, data, substancia, num_venda) )
        return  '<h3>Venda com prescrição registada!</h3><br> <a href="../../venda_farmacia">Voltar</a>'
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

#===============================================================================================================================================
@app.route("/glicemia")
def list_glicemia():
    dbConn=None 
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = """SELECT c.nome, quant, num_doente 
                   FROM analise a join instituicao i ON i.nome = a.inst 
                   JOIN concelho c ON (i.num_concelho = c.num_concelho AND i.num_regiao = c.num_regiao)
                   WHERE a.nome = 'glicémia'
                   AND (c.num_concelho, c.num_regiao, quant) IN (SELECT c.num_concelho, c.num_regiao, %s(quant)
											  FROM analise a join instituicao i ON i.nome = a.inst 
											  JOIN concelho c ON (i.num_concelho = c.num_concelho AND i.num_regiao = c.num_regiao)
											  WHERE a.nome = 'glicémia'
											  GROUP BY c.num_concelho, c.num_regiao)
                   ORDER BY c.nome;"""
        cursor.execute(query % "max")
        max_glic = cursor.fetchall()
        cursor.execute(query % "min")
        min_glic = cursor.fetchall()
        return render_template("glicemia.html", max_glic=max_glic, min_glic=min_glic) + '<br> <a href="./">Voltar</a>'
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        dbConn.close()
#===============================================================================================================================================    
@app.route('/instituicao')
def list_instituicao_edit():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "SELECT i.nome, tipo, r.nome, c.nome FROM (regiao r JOIN concelho c ON r.num_regiao=c.num_regiao) JOIN instituicao i ON i.num_regiao=r.num_regiao AND i.num_concelho=c.num_concelho;"
    cursor.execute(query)
    return render_template("edit_instituicao.html", cursor=cursor, params=request.args)+ '<br> <a href="./">Voltar</a>'
  except Exception as e:
    return str(e) 
  finally:
    cursor.close()
    dbConn.close()

@app.route('/instituicao/insert')
def alter_instituicao_insert():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "SELECT c.num_regiao, c.num_concelho, r.nome, c.nome FROM concelho c JOIN regiao r ON c.num_regiao=r.num_regiao;"
    cursor.execute(query)
    return render_template("insert_instituicao.html", cursor=cursor)
  except Exception as e:
    return str(e)

@app.route('/instituicao/update')
def alter_instituicao_update():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "SELECT c.num_regiao, c.num_concelho, r.nome, c.nome FROM concelho c JOIN regiao r ON c.num_regiao=r.num_regiao;"
    cursor.execute(query)
    return render_template("update_instituicao.html", cursor=cursor, params=request.args)
  except Exception as e:
    return str(e)

@app.route('/instituicao/insert/confirm', methods=["POST"])
def insert_instituicao():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = 'INSERT INTO instituicao VALUES (%s,%s,%s,%s);'
    num_regiao, num_concelho = request.form["regiao_concelho"].split(",")
    data = (request.form["nome"],request.form["tipo"],num_regiao , num_concelho)
    cursor.execute(query,data)
    return '<h3>Instituição inserida!</h3><br> <a href="../../instituicao">Voltar</a>'
  except Exception as e:
    return str(e) 
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

@app.route('/instituicao/update/confirm', methods=["POST"])
def update_instituicao():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    data = (request.form["new_name"], request.form["old_name"])
    query = 'UPDATE instituicao SET nome=%s WHERE nome=%s;'
    cursor.execute(query,data)
    return '<h3>Instituição atualizada!</h3><br> <a href="../../instituicao">Voltar</a>'
  except psycopg2.errors.UniqueViolation:
      return "<h3>ERRO: Esse nome de instituição já existe.<h3>"
  except Exception as e:
    return str(e)
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()
        
@app.route('/instituicao/delete/confirm', methods=["GET"])
def delete_instituicao():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "DELETE FROM instituicao WHERE nome = %s;"
    cursor.execute(query, [request.args.get("nome")] )
    return '<h3>Instituição removida!</h3><br> <a href="../../instituicao">Voltar</a>'
  except Exception as e:
    return str(e) 
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

#===============================================================================================================================================
@app.route('/medico')
def list_medico_edit():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "SELECT num_cedula, nome, especialidade FROM medico;"
    cursor.execute(query)
    return render_template("edit_medico.html", cursor=cursor, params=request.args) + '<br> <a href="./">Voltar</a>'
  except Exception as e:
    return str(e) 
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

@app.route('/medico/insert')
def alter_medico_insert():
  try:
    return render_template("insert_medico.html", params=request.args)
  except Exception as e:
    return str(e)
    
@app.route('/medico/update')
def alter_medico_update():
  try:
    return render_template("update_medico.html", params=request.args)
  except Exception as e:
    return str(e)

@app.route('/medico/insert/confirm', methods=["POST"])
def insert_medico():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "INSERT INTO medico VALUES (%s,%s,%s);"
    data = (request.form["num_cedula"],request.form["nome"],request.form["especialidade"])
    cursor.execute(query,data)
    return '<h3>Médico inserido!</h3><br> <a href="../../medico">Voltar</a>'
  except Exception as e:
    return str(e) 
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()


@app.route('/medico/update/confirm', methods=["POST"])
def update_medico():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    if request.form["nome"]=="":
        if request.form["especialidade"]=="":
            return "<h3>ERRO: Preencha pelo menos um dos campos.<h3>"
        else:
            query = "UPDATE medico SET especialidade=%s WHERE num_cedula=%s;"
            data = (request.form["especialidade"],request.form["num_cedula"])
            cursor.execute(query,data)
    else:
       if request.form["especialidade"]=="":
           query = "UPDATE medico SET nome=%s WHERE num_cedula=%s;"
           data = (request.form["nome"],request.form["num_cedula"])
           cursor.execute(query,data)
       else:
           query = "UPDATE medico SET nome=%s, especialidade=%s WHERE num_cedula=%s;"
           data = (request.form["nome"],request.form["especialidade"],request.form["num_cedula"])
           cursor.execute(query,data)
    
    return '<h3>Médico atualizado!</h3><br> <a href="../../medico">Voltar</a>'
  except Exception as e:
    return str(e) 
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

@app.route('/medico/delete/confirm', methods=["GET"])
def delete_medico():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "DELETE FROM medico WHERE num_cedula=%s;"
    cursor.execute(query,[request.args.get("num_cedula")])
    return '<h3>Médico removido!</h3><br> <a href="../../medico">Voltar</a>'
  except Exception as e:
    return str(e) 
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

#===============================================================================================================================================
@app.route('/prescricao')
def list_prescricao_edit():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "SELECT num_cedula, nome, num_doente, data, substancia, quant FROM prescricao NATURAL JOIN medico;"
    cursor.execute(query)
    return render_template("edit_prescricao.html", cursor=cursor, params=request.args) + '<br> <a href="./">Voltar</a>'
  except Exception as e:
    return str(e) 
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

@app.route('/prescricao/insert')
def alter_prescricao_insert():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    
    cursor.execute("SELECT c.num_cedula, m.nome, c.num_doente, c.data FROM consulta c JOIN medico m ON c.num_cedula=m.num_cedula ;")

    return render_template("insert_prescricao.html", consultas=cursor)
  except Exception as e:
    return str(e)
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()
    
@app.route('/prescricao/update')
def alter_prescricao_update():
  try:
    return render_template("update_prescricao.html", params=request.args)
  except Exception as e:
    return str(e)

@app.route('/prescricao/insert/confirm', methods=["POST"])
def insert_prescricao():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    
    query = "INSERT INTO prescricao VALUES (%s,%s,%s,%s,%s);"
    num_cedula, num_doente, data = request.form["consulta"].split(",") 

    data = (num_cedula,num_doente, data, request.form["substancia"], request.form["quant"])
    cursor.execute(query,data)
    return '<h3>Prescrição inserida!</h3><br> <a href="../../prescricao">Voltar</a>'
  except Exception as e:
    return str(e) 
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

@app.route('/prescricao/update/confirm', methods=["POST"])
def update_prescricao():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "UPDATE prescricao SET quant=%s WHERE num_cedula=%s AND num_doente=%s AND data=%s AND substancia=%s;"
    data = (request.form["quant"],request.form["num_cedula"],request.form["num_doente"],request.form["data"],request.form["substancia"])
    cursor.execute(query,data)
    return '<h3>Prescrição atualizada!</h3><br> <a href="../../prescricao">Voltar</a>'
  except Exception as e:
    return str(e) 
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

@app.route('/prescricao/delete/confirm', methods=["GET"])
def delete_prescricao():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "DELETE FROM prescricao WHERE num_cedula=%s AND num_doente=%s AND data=%s AND substancia=%s;"
    data = (request.args.get("num_cedula"),request.args.get("num_doente"),request.args.get("data"),request.args.get("substancia"))
    cursor.execute(query,data)  
    return '<h3>Prescrição removida!</h3><br> <a href="../../prescricao">Voltar</a>'
  except Exception as e:
    return str(e) 
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()


#===============================================================================================================================================
@app.route('/analise')
def list_analise_edit():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "SELECT a.num_analise, a.especialidade, a.num_cedula, m.nome, a.num_doente, a.data, \
    a.data_registo, a.nome, a.quant, a.inst FROM analise a LEFT JOIN medico m ON a.num_cedula = m.num_cedula;"
    cursor.execute(query)
    return render_template("edit_analise.html", cursor=cursor, params=request.args) + '<br> <a href="./">Voltar</a>'
  except Exception as e:
    return str(e) 
  finally:
    cursor.close()
    dbConn.close()

@app.route('/analise/insert')
def alter_analise_insert():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cursor.execute("SELECT nome FROM instituicao;")
    insts = cursor.fetchall()
    cursor.execute("SELECT c.num_cedula, m.nome, c.num_doente, c.data FROM consulta c JOIN medico m ON c.num_cedula=m.num_cedula ;")
    consultas = cursor.fetchall()
    return render_template("insert_analise.html", insts=insts, consultas=consultas)
  except Exception as e:
    return str(e)
  finally:
    dbConn.commit()
    cursor.close()
    
@app.route('/analise/update', methods=["GET"])
def alter_analise_update():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cursor.execute("SELECT nome FROM instituicao;")
    insts = cursor.fetchall()
    cursor.execute("SELECT c.num_cedula, m.nome, c.num_doente, c.data FROM consulta c JOIN medico m ON c.num_cedula=m.num_cedula ;")
    consultas = cursor.fetchall()
    return render_template("update_analise.html", insts=insts, consultas=consultas, num_analise=request.args.get("num_analise"))
  except Exception as e:
    return str(e)
  finally:
    dbConn.commit()
    cursor.close()


@app.route('/analise/insert/confirm', methods=["POST"])
def insert_analise():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cursor.execute("SELECT MAX(num_analise) FROM analise;")
    num_analise = cursor.fetchone()[0] + 1
    num_cedula, num_doente, data = request.form["consulta"].split(",") if 'NULL' not in request.form["consulta"].split(",") else [None, None, None]
    query = "INSERT INTO analise VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    data = (num_analise, request.form["especialidade"], num_cedula, num_doente, data, \
            d.date.today().strftime("%Y-%m-%d"), request.form["nome"], request.form["quant"], request.form["inst"])
    cursor.execute(query,data)
    return'<h3>Análise inserida!</h3><br> <a href="../../analise">Voltar</a>'
  except Exception as e:
    return str(e)
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

@app.route('/analise/update/confirm', methods=["POST"])
def update_analise():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    num_analise = request.form["num_analise"]
    especialidade = request.form["especialidade"] 
    num_cedula, num_doente, data = request.form["consulta"].split(",") if 'NULL' not in request.form["consulta"].split(",") else [None, None, None]
    data_registo = request.form["data_registo"] 
    nome = request.form["nome"] 
    quant = request.form["quant"] 
    inst = request.form["inst"] 

    query = ("UPDATE analise SET " +
    ("especialidade=%s, " if especialidade != "" else "") +
    ("num_cedula=%s, " if num_cedula != "" else "") +
    ("num_doente=%s, " if num_doente != "" else "") +
    ("data=%s, " if data != "" else "") +
    ("data_registo=%s, " if data_registo != "" else "") +
    ("nome=%s, " if nome != "" else "") +
    ("quant=%s, " if quant != "" else "") +
    ("inst=%s, " if inst != "" else "") )[:-2] + \
    " WHERE num_analise=%s;"
    
    data = tuple(x for x in (especialidade, num_cedula, num_doente, data, data_registo, nome, quant, inst, num_analise) if x != "")

    cursor.execute(query,data)
    return '<h3>Análise atualizada!</h3><br> <a href="../../analise">Voltar</a>'
  except psycopg2.errors.SyntaxError:
    return "<h3>ERRO: Mude o valor de pelo menos um dos parâmetros.</h3>"

  except Exception as e:
    return str(e) 
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close() 

@app.route('/analise/delete/confirm', methods=["GET"])
def delete_analise():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "DELETE FROM analise WHERE num_analise=%s;"
    cursor.execute(query, [request.args.get("num_analise")] )
    return '<h3>Análise removida!</h3><br> <a href="../../analise">Voltar</a>'
  except Exception as e:
    return str(e) 
  finally:
    dbConn.commit()
    cursor.close()

#===============================================================================================================================================
    
@app.route('/substancias')
def alter_instituicao_delete():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "SELECT DISTINCT p.num_cedula, m.nome FROM prescricao p NATURAL JOIN medico m ;"
    cursor.execute(query)
    return render_template("choose_prescricao.html", cursor=cursor) + '<br> <a href="./">Voltar</a>'
  except Exception as e:
    return str(e)
  finally:
    cursor.close()
    dbConn.close()

@app.route('/substancias/list', methods=["POST"])
def list_prescricao():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    print()
    query = "SELECT DISTINCT substancia FROM prescricao p WHERE num_cedula=%s AND EXTRACT(MONTH FROM data)=%s AND EXTRACT(YEAR FROM data)=%s;"
    num_cedula, nome = request.form["medico"].split(",")
    month,year = request.form["mes"][5:7],request.form["mes"][0:4]
    data = (num_cedula,month,year)
    cursor.execute(query,data)
    return render_template("list_prescricao.html",  cursor=cursor, nome=nome, month=month, year=year) + '<br> <a href="../substancias">Voltar</a>'
  except Exception as e:
    return str(e) 
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

CGIHandler().run(app)

