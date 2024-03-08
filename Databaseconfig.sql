DROP SCHEMA IF EXISTS bioaccess;

CREATE SCHEMA IF NOT EXISTS bioaccess;

USE bioaccess;

CREATE TABLE Ansatt
( 
AnsattID CHAR(20) NOT NULL,
Ansettelsesdato DATE NOT NULL,
Fornavn CHAR(20) NOT NULL,
Etternavn CHAR(20) NOT NULL,
Fødselsnummer CHAR(6) NOT NULL,
Adresse CHAR(20) NOT NULL,
Telefon CHAR(15) NOT NULL,
Epost CHAR(30) NOT NULL,

CONSTRAINT AnsattPK PRIMARY KEY(AnsattID)
);

CREATE TABLE Arbeidsregistrering
(
AnsattID CHAR(20) NOT NULL,
RegID CHAR(20) NOT NULL,
Dato DATE NOT NULL,
Starttid TIMESTAMP NOT NULL,
Slutttid TIMESTAMP NULL DEFAULT NULL,
AntallTimer CHAR(6),
CONSTRAINT ArbeidslistePK PRIMARY KEY(RegID),
CONSTRAINT ArbeidslisteFK FOREIGN KEY (AnsattID) 
REFERENCES Ansatt (AnsattID)
);


CREATE TABLE Statusen
(
AnsattID CHAR(20) NOT NULL,
Statusen ENUM('Jobber', 'Jobber ikke'),
RegID CHAR(20),
CONSTRAINT StatusPK PRIMARY KEY(AnsattID,Statusen),
CONSTRAINT StatusFK FOREIGN KEY (AnsattID) 
REFERENCES Ansatt (AnsattID)
);
CREATE TABLE Stilling
(
AnsattID CHAR(20) NOT NULL,
Stilling CHAR(30) NOT NULL,
Timelonn CHAR(30) NOT NULL,
Stillingstype ENUM('Heltid', 'Deltid 80%','Deltid 60%','Deltid 40%','Deltid 20%'),

CONSTRAINT StillingPK PRIMARY KEY(AnsattID,Stilling),
CONSTRAINT StillingFK FOREIGN KEY (AnsattID) 
REFERENCES Ansatt (AnsattID)
);

CREATE TABLE Lønnsdokument
(
DokumentID CHAR(20) NOT NULL,
Opprettelsesdato timestamp NOT NULL,
Utbetalingsstatus CHAR(20) NOT NULL,
AnsattID CHAR(20) NOT NULL,
Dokument_Navn CHAR(30) NOT NULL,
Dokument_Sti CHAR(50) NOT NULL,

CONSTRAINT LønnsdokumentPK PRIMARY KEY(DokumentID),
CONSTRAINT LønnsdokumentFK FOREIGN KEY (AnsattID) 
REFERENCES Ansatt (AnsattID)
);
INSERT INTO Ansatt (AnsattID,Ansettelsesdato,Fornavn,Etternavn,Fødselsnummer,Adresse,Telefon,Epost) Values
('1','2024-02-16','Luqman','Khokhar','181199','Kongens gate 1','+4712345678','example@test.no');

INSERT INTO Stilling (AnsattID,Stilling,Timelonn,Stillingstype) Values
('1','Medarbeider','190','Heltid');
INSERT INTO Statusen (AnsattID,Statusen) Values
('1','Jobber');

INSERT INTO Arbeidsregistrering (AnsattID,regid,Dato,Starttid,slutttid,antalltimer) Values
('1',13,'2024-02-20','2024-02-20 16:30:00','2024-02-20 23:30:00','7');
