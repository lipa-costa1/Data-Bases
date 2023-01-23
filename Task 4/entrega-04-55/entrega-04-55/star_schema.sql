DROP TABLE IF EXISTS d_tempo CASCADE;
DROP TABLE IF EXISTS d_instituicao CASCADE;
DROP TABLE IF EXISTS f_analise CASCADE;
DROP TABLE IF EXISTS f_presc_venda CASCADE;

CREATE TABLE d_tempo(
id_tempo SERIAL, 
dia INTEGER NOT NULL, 
dia_da_semana INTEGER NOT NULL, 
semana INTEGER NOT NULL, 
mes INTEGER NOT NULL, 
trimestre INTEGER NOT NULL, 
ano INTEGER NOT NULL,
primary key(id_tempo)
);

CREATE TABLE d_instituicao(
id_inst SERIAL,
nome VARCHAR(50) NOT NULL,
tipo VARCHAR(50) NOT NULL,
num_regiao INTEGER NOT NULL,
num_concelho INTEGER NOT NULL,
primary key(id_inst),
foreign key(nome) references instituicao(nome) on delete cascade on update cascade,
foreign key(num_regiao,num_concelho) references concelho(num_regiao,num_concelho) on delete cascade on update cascade
);

CREATE TABLE f_presc_venda(
id_presc_venda INTEGER,
id_medico INTEGER NOT NULL,
num_doente INTEGER NOT NULL,
id_data_registo INTEGER NOT NULL,
id_inst INTEGER NOT NULL,
substancia VARCHAR(50) NOT NULL,
quant INTEGER NOT NULL,
primary key(id_presc_venda),
foreign key(id_presc_venda) references prescricao_venda(num_venda) on delete cascade on update cascade, --assegurando que num_venda é unique em presc_venda
foreign key(id_medico) references medico(num_cedula) on delete cascade on update cascade,
foreign key(id_data_registo) references d_tempo(id_tempo) on delete cascade on update cascade,
foreign key(id_inst) references d_instituicao(id_inst) on delete cascade on update cascade
);

CREATE TABLE f_analise(
id_analise INTEGER, 
id_medico INTEGER,
num_doente INTEGER,
id_data_registo INTEGER NOT NULL,
id_inst INTEGER NOT NULL,
nome VARCHAR(50) NOT NULL,
quant INTEGER NOT NULL,
primary key(id_analise),
foreign key(id_analise) references analise(num_analise) on delete cascade on update cascade,
foreign key(id_medico) references medico(num_cedula) on delete cascade on update cascade,
foreign key(id_data_registo) references d_tempo(id_tempo) on delete cascade on update cascade,
foreign key(id_inst) references d_instituicao(id_inst) on delete cascade on update cascade
);
