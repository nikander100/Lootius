CREATE TABLE "Weapons" (
	"id"	INTEGER,
	"name"	TEXT UNIQUE,
	"type"	TEXT,
	"decay"	REAL DEFAULT 0,
	"ammo"	INTEGER DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE "Sights" (
	"id"	INTEGER,
	"name"	TEXT UNIQUE,
	"type"	TEXT,
	"decay"	REAL DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE "Scopes" (
	"id"	INTEGER,
	"name"	TEXT UNIQUE,
	"type"	TEXT,
	"decay"	REAL DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE "Amps" (
	"id"	INTEGER,
	"name"	TEXT UNIQUE,
	"type"	TEXT,
	"decay"	REAL DEFAULT 0,
	"ammo"	INTEGER DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE "weapon_loadouts" (
	"id"	INTEGER DEFAULT 0,
	"name"	TEXT NOT NULL DEFAULT "" UNIQUE,
	"weapon"	TEXT DEFAULT "", --do i want to add forgein keys here to the corresponding list but wth name?
	"amp"	TEXT DEFAULT "",
	"absorber"	TEXT DEFAULT "",
	"scope"	INTEGER DEFAULT "",
	"scopeSight"	TEXT DEFAULT "",
	"sight"	TEXT DEFAULT "",
	"enhancer1Name"	TEXT DEFAULT "",
	"enhancer1Amount"	INTEGER DEFAULT 0,
	"enhancer2Name"	TEXT DEFAULT "",
	"enhancer2Amount"	INTEGER DEFAULT 0,
	"enhancer3Name"	TEXT DEFAULT "",
	"enhancer3Amount"	INTEGER DEFAULT 0,
	"enhancer4Name"	TEXT DEFAULT "",
	"enhancer4Amount"	INTEGER DEFAULT 0,
	"enhancer5Name"	TEXT DEFAULT "",
	"enhancer5Amount"	INTEGER DEFAULT 0,
	"enhancer6Name"	TEXT DEFAULT "",
	"enhancer6Amount"	INTEGER DEFAULT 0,
	"enhancer7Name"	TEXT DEFAULT "",
	"enhancer7Amount"	INTEGER DEFAULT 0,
	"enhancer8Name"	TEXT DEFAULT "",
	"enhancer8Amount"	INTEGER DEFAULT 0,
	"enhancer9Name"	TEXT DEFAULT "",
	"enhancer9Amount"	INTEGER DEFAULT 0,
	"enhancer10Name"	TEXT DEFAULT "",
	"enhancer10Amount"	INTEGER DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
);