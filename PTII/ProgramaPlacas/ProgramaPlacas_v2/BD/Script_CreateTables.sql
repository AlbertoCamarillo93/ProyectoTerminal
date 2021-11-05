CREATE TABLE "Usuario" (
	"idUsuario"   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"id_camara"	  INTEGER NOT NULL,
	"nombre"	  VARCHAR(100) NOT NULL,
	"apellido_p"  VARCHAR(100) NOT NULL,
	"password"	  VARCHAR(100) NOT NULL,
	"correo"	  VARCHAR(100) NOT NULL,
	"tipoUsuario" VARCHAR(100),
	FOREIGN KEY(id_camara) REFERENCES Camara(idCamara)
);

CREATE TABLE "Camara" (
	"idCamara"	 INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"id_usuario" INTEGER NOT NULL,
	"calle"	     VARCHAR(100) NOT NULL,
	"colonia"	 VARCHAR(100) NOT NULL,
	"delegacion" VARCHAR(100) NOT NULL,
	FOREIGN KEY(id_usuario) REFERENCES Usuario(idUsuario)
);

CREATE TABLE "FotosReconocida" (
	"id_foto"   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"id_camara" INTEGER NOT NULL,
	"fecha"     TEXT NOT NULL,
	FOREIGN KEY(id_camara) REFERENCES Camara(idCamara)
);