DROP TABLE IF EXISTS prescricao_venda CASCADE;
DROP TABLE IF EXISTS venda_farmacia CASCADE;
DROP TABLE IF EXISTS analise CASCADE;
DROP TABLE IF EXISTS prescricao CASCADE;
DROP TABLE IF EXISTS consulta CASCADE;
DROP TABLE IF EXISTS medico CASCADE;
DROP TABLE IF EXISTS instituicao CASCADE;
DROP TABLE IF EXISTS concelho CASCADE;
DROP TABLE IF EXISTS regiao CASCADE;

CREATE TABLE regiao(
num_regiao INTEGER,
nome VARCHAR(8) NOT NULL,
num_habitantes INTEGER NOT NULL,
primary key(num_regiao),
unique(nome),
CHECK(num_regiao>0),
CHECK(nome in ('Norte', 'Centro', 'Lisboa', 'Alentejo', 'Algarve')),
CHECK(num_habitantes>=0)
);

CREATE TABLE concelho(
num_concelho INTEGER,
num_regiao INTEGER,
nome VARCHAR(50) NOT NULL,
num_habitantes INTEGER NOT NULL,
primary key(num_concelho,num_regiao),
foreign key(num_regiao) references regiao(num_regiao) on delete cascade on update cascade,
unique(nome),
CHECK(num_concelho>0),
CHECK(num_habitantes>=0)
);

CREATE TABLE instituicao(
nome VARCHAR(50),
tipo VARCHAR(11) NOT NULL,
num_regiao INTEGER NOT NULL,
num_concelho INTEGER NOT NULL,
primary key(nome),
foreign key(num_regiao,num_concelho) references concelho(num_regiao,num_concelho) on delete cascade on update cascade,
CHECK(tipo in ('farmacia', 'laboratorio', 'clinica', 'hospital'))
);

CREATE TABLE medico(
num_cedula INTEGER,
nome VARCHAR(50) NOT NULL,
especialidade VARCHAR(50) NOT NULL,
primary key(num_cedula),
CHECK(num_cedula>0)
);

CREATE TABLE consulta(
num_cedula INTEGER,
num_doente INTEGER,
data DATE,
nome_instituicao VARCHAR(50) NOT NULL,
primary key(num_cedula,num_doente,data),
foreign key(num_cedula) references medico(num_cedula) on delete cascade on update cascade,
foreign key(nome_instituicao) references instituicao(nome) on delete cascade on update cascade,
unique(num_doente,data,nome_instituicao),
CHECK(num_doente>0),
CHECK(EXTRACT(DOW FROM data) in ('1', '2','3', '4', '5'))
);

CREATE TABLE prescricao(
num_cedula INTEGER, 
num_doente INTEGER, 
data DATE,
substancia VARCHAR(50),
quant INTEGER NOT NULL,
primary key(num_cedula,num_doente,data,substancia),
foreign key(num_cedula,num_doente,data) references consulta(num_cedula,num_doente,data) on delete cascade on update cascade,
CHECK(quant>=0)
);

CREATE TABLE analise(
num_analise INTEGER, 
especialidade VARCHAR(50) NOT NULL,
num_cedula INTEGER, 
num_doente INTEGER, 
data DATE,
data_registo DATE NOT NULL,
nome VARCHAR(50) NOT NULL,
quant INTEGER NOT NULL,
inst VARCHAR(50) NOT NULL,
primary key(num_analise),
foreign key(num_cedula,num_doente,data) references consulta(num_cedula,num_doente,data) on delete cascade on update cascade,
foreign key(inst) references instituicao(nome) on delete cascade on update cascade,
CHECK(quant>=0),
CHECK(data <= data_registo)
);

CREATE TABLE venda_farmacia(
num_venda INTEGER,
data_registo DATE NOT NULL,
substancia VARCHAR(50) NOT NULL,
quant INTEGER NOT NULL,
preco NUMERIC(6,2) NOT NULL,
inst VARCHAR(50) NOT NULL,
primary key(num_venda),
foreign key(inst) references instituicao(nome) on delete cascade on update cascade,
CHECK(num_venda>0),
CHECK(quant>=0),
CHECK(preco>=0)
);

CREATE TABLE prescricao_venda(
num_cedula INTEGER, 
num_doente INTEGER, 
data DATE,
substancia VARCHAR(50),
num_venda INTEGER,
unique(num_venda), --necessario para o star_schema.sql
primary key(num_cedula, num_doente, data, substancia, num_venda),
foreign key(num_venda) references venda_farmacia(num_venda) on delete cascade on update cascade,
foreign key(num_cedula, num_doente, data, substancia) references prescricao(num_cedula, num_doente, data, substancia) on delete cascade on update cascade
);