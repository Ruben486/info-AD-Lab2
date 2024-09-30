create database productos;
show databases; 
use productos;

ALTER table productos
add SO varchar(30);

CREATE TABLE productoCelular(
	Codigo char(15) primary Key, 
	Marca varchar(30) not null,
    Modelo varchar(30) not null,
    FOREIGN KEY(Codigo) REFERENCES productos(Codigo)
);
 
 CREATE TABLE productoComputadora(
	Codigo char(15) primary Key, 
    Procesador varchar(30) not null,
    FOREIGN KEY(Codigo) REFERENCES productos(Codigo)
);
USE productos;
ALTER TABLE productos MODIFY Rubro varchar(50);