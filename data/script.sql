CREATE TABLE "WeaponTypes" (
	"id"	INTEGER,
	"type" TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE "Weapons" (
	"id"	INTEGER,
	"name"	TEXT,
	"damage"	INTEGER DEFAULT 0,
	"firerate"	INTEGER DEFAULT 0,
	"decay"	REAL DEFAULT 0,
	"ammoBurn"	INTEGER DEFAULT 0,
	"weaponTypeID"	INTEGER,
	FOREIGN KEY("weaponTypeID") REFERENCES "WeaponTypes"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE "Sights" (
	"id"	INTEGER,
	"name"	TEXT,
	"decay"	REAL DEFAULT 0,
	"weaponTypeID"	INTEGER,
	FOREIGN KEY("weaponTypeID") REFERENCES "WeaponTypes"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE "Scopes" (
	"id"	INTEGER,
	"name"	TEXT,
	"decay"	REAL DEFAULT 0,
	"weaponTypeID"	INTEGER,
	FOREIGN KEY("weaponTypeID") REFERENCES "WeaponTypes"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE "WeaponAmps" (
	"id"	INTEGER,
	"name"	TEXT,
	"decay"	REAL DEFAULT 0,
	"ammoBurn"	INTEGER DEFAULT 0,
	"weaponTypeID"	INTEGER,
	FOREIGN KEY("weaponTypeID") REFERENCES "WeaponTypes"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE "WeaponAbsorbers" (
	"id"	INTEGER,
	"name"	TEXT,
	"decay"	REAL,
	"absorbPercent"	REAL,
	"weaponTypeID"	INTEGER,
	FOREIGN KEY("weaponTypeID") REFERENCES "WeaponTypes"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE "ScopeLoadout" (
	"id"	INTEGER,
	"scopeID"	INTEGER,
	"sightID"	INTEGER,
	FOREIGN KEY("scopeID") REFERENCES "Scopes"("id"),
	FOREIGN KEY("sightID") REFERENCES "Sights"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE "WeaponLoadout" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL DEFAULT "" UNIQUE,
	"weaponID"	INTEGER,
	"socketsID"	INTEGER,
	"weaponAmpID"	INTEGER,
	"scopeLoadoutID"	INTEGER,
	"sightID"	INTEGER,
	"absorberID"	INTEGER,
	FOREIGN KEY("weaponID") REFERENCES "Weapons"("id"),
	FOREIGN KEY("socketsID") REFERENCES "Sockets"("id"),
	FOREIGN KEY("weaponAmpID") REFERENCES "WeaponAmps"("id"),
	FOREIGN KEY("scopeLoadoutID") REFERENCES "ScopeLoadout"("id"),
	FOREIGN KEY("sightID") REFERENCES "Sights"("id"),
	FOREIGN KEY("absorberID") REFERENCES "WeaponAbsorbers"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);