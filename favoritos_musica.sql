-- DDL - Verifica se o banco favoritos
-- existe, caso exista vai removê-lo, caso contrário
-- apresenta uma advertência que indica que o banco 
-- ainda não existe
drop schema if exists favoritos;

-- DDL - Cria o BD favoritos
create schema favoritos;

-- DDL - Seleciona - habilita o BD favoritos para o uso 
use favoritos;

-- DDL - Criação de tabela de paises
create table Favoritos(
ID_musica int not null auto_increment,
Nome varchar (300) not null,
primary key (ID_musica)
);

select * from favoritos;