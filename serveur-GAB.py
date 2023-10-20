#!/usr/bin/env python3
import socket
import sqlite3
import threading
threadsClients = []

def connexionBaseDeDonnees():
	baseDeDonnees = sqlite3.connect("banque.db")
	curseur = baseDeDonnees.cursor()
	return baseDeDonnees, curseur
def create_table():
	baseDeDonnees, curseur = connexionBaseDeDonnees()
	curseur.execute('''
    CREATE TABLE IF NOT EXISTS comptes (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        pinuser TEXT NOT NULL,
        idCompte TEXT NOT NULL, 
        solde INTEGER NOT NULL, 
        dateOperation DATE NOT NULL, 
        libelleOperation TEXT NOT NULL, 
        montant INTEGER
    )
''')
	baseDeDonnees.commit()
	baseDeDonnees.close()
def testpin(nocompte, pinuser):
	baseDeDonnees, curseur = connexionBaseDeDonnees()
	curseur.execute("SELECT codePIN FROM Comptes WHERE idCompte = ?",(nocompte,))
	pincompte = curseur.fetchone()[0]
	baseDeDonnees.close()
	if pincompte == pinuser:
		return True
	else:
		return False

def add_user(username, pinuser, solde, idCompte, dateOperation, libelleOperation, montant):
	baseDeDonnees, curseur = connexionBaseDeDonnees()
	curseur.execute("INSERT INTO comptes (username, pinuser, idCompte, solde, dateOperation, libelleOperation, montant) VALUES (?, ?, ?, ?, ?, ?, ?)", (username, pinuser, solde, idCompte, dateOperation, libelleOperation, montant))
	baseDeDonnees.commit()
	baseDeDonnees.close()

def solde(nocompte):
	baseDeDonnees, curseur = connexionBaseDeDonnees()
	curseur.execute("SELECT solde FROM Comptes WHERE idCompte = ?",(nocompte,))
	soldeCompte = curseur.fetchone()[0]
	baseDeDonnees.close()
	return soldeCompte

def retrait(nocompte, montant):
	#Le montant est négatif
	baseDeDonnees, curseur = connexionBaseDeDonnees()
	montant = float(montant)
	soldeCompte = solde(nocompte)
	if soldeCompte < montant or montant >= 0:
		baseDeDonnees.close()
		return False
	else:
		nouveauSolde = soldeCompte+montant
		curseur.execute("UPDATE Comptes SET solde = ? WHERE idCompte = ?",(nouveauSolde,nocompte))
		curseur.execute("INSERT INTO Operations (dateOperation, idCompte, libelleOperation, montant) VALUES (DATE('NOW'), ?, ?, ?)",(nocompte, "Retrait", montant))
		baseDeDonnees.commit()
		baseDeDonnees.close()
		return True

def transfert(nocompteSource, nocompteDestination, montant):
	#Le montant est positif
	baseDeDonnees, curseur = connexionBaseDeDonnees()
	montant = float(montant)
	soldeCompteSource = solde(nocompteSource)
	if soldeCompteSource < montant or montant <= 0:
		baseDeDonnees.close()
		return False
	else:
		nouveauSoldeSource = soldeCompteSource-montant
		curseur.execute("UPDATE Comptes SET solde = ? WHERE idCompte = ?",(nouveauSoldeSource,nocompteSource))
		curseur.execute("INSERT INTO Operations (dateOperation, idCompte, libelleOperation, montant) VALUES (DATE('NOW'), ?, ?, ?)",(nocompteSource, "Virement", -montant))
		soldeCompteDestination = solde(nocompteDestination)
		nouveauSoldeDestination = soldeCompteDestination+montant
		curseur.execute("UPDATE Comptes SET solde = ? WHERE idCompte = ?",(nouveauSoldeDestination,nocompteDestination))
		curseur.execute("INSERT INTO Operations (dateOperation, idCompte, libelleOperation, montant) VALUES (DATE('NOW'), ?, ?, ?)",(nocompteDestination, "Virement", montant))
		baseDeDonnees.commit()
		baseDeDonnees.close()
		return True

def depot(nocompte, montant):
	#Le montant est positif
	baseDeDonnees, curseur = connexionBaseDeDonnees()
	montant = float(montant)
	soldeCompte = solde(nocompte)
	nouveauSolde = soldeCompte+montant
	curseur.execute("UPDATE Comptes SET solde = ? WHERE idCompte = ?",(nouveauSolde,nocompte))
	curseur.execute("INSERT INTO Operations (dateOperation, idCompte, libelleOperation, montant) VALUES (DATE('NOW'), ?, ?, ?)",(nocompte, "Dépôt", montant))
	baseDeDonnees.commit()
	baseDeDonnees.close()
	return True

def historique(nocompte):
	baseDeDonnees, curseur = connexionBaseDeDonnees()
	curseur.execute("SELECT dateOperation, libelleOperation, montant FROM Operations WHERE idCompte = ? ORDER BY dateOperation DESC LIMIT 10;",(nocompte,))
	historiqueCSV = "\"dateOperation\";\"libelleOperation\";\"montant\"\n"
	for ligne in curseur.fetchall():
		historiqueCSV += "\"" + ligne[0] + "\";\"" + ligne[1] + "\";\"" + str(ligne[2]) + "\"\n"
	return historiqueCSV

def instanceServeur (client, infosClient):
	adresseIP = infosClient[0]
	port = str(infosClient[1])
	print("Instance de serveur prêt pour " + adresseIP + ":" + port)
	actif = True
	while actif:
		message = client.recv(255).decode("utf-8").upper().split(" ")
		pret = False
		if message[0] == "TESTPIN":
			if testpin(message[1], message[2]):
				client.send("TESTPIN OK".encode("utf-8"))
				message = client.recv(255).decode("utf-8").upper().split(" ")
				if message[0] == "RETRAIT":
					if retrait(message[1], message[2]):
						client.send("RETRAIT OK".encode("utf-8"))
					else:
						client.send("RETRAIT NOK".encode("utf-8"))
				elif message[0] == "DEPOT":
					depot(message[1], message[2])
					client.send("DEPOT OK".encode("utf-8"))
				elif message[0] == "SOLDE":
					soldeCompte = solde(message[1])
					client.send(("SOLDE " + str(soldeCompte)).encode("utf-8"))
				elif message[0] == "TRANSFERT":
					if transfert(message[1], message[2], message[3]):
						client.send("TRANSFERT OK".encode("utf-8"))
					else:
						client.send("TRANSFERT NOK".encode("utf-8"))
				elif message[0] == "HISTORIQUE":
					historiqueCSV = historique(message[1])
					client.send(("HISTORIQUE " + historiqueCSV).encode("utf-8"))
				else:
					client.send("ERROPERATION".encode("utf-8"))
			else:
				client.send("TESTPIN NOK".encode("utf-8"))
		else:
			client.send("ERROPERATION".encode("utf-8"))
	print("Connexion fermée avec " + adresseIP + ":" + port)
	client.close()
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(('', 50000))	# Écoute sur le port 50000
serveur.listen(5)
create_table()
add_user("test", "1310", 2500, 250, 25-10-2023, "retrait", 2500)
add_user("test3", "1412", 2500, 250, 25-10-2023, "retrait", 2500)
while True:
	client, infosClient = serveur.accept()
	threadsClients.append(threading.Thread(None, instanceServeur, None, (client, infosClient), {}))
	threadsClients[-1].start()
serveur.close()
