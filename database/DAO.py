from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.fermata import Fermata


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def hasconn(u: Fermata, v: Fermata) -> bool: #mi aspetto oggetti di tipo fermata e un bool come ritorno
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione c where c.id_stazP = %s and c.id_stazA = %s"
        cursor.execute(query (u.id_fermata, v.id_fermata,)) #il confronto devo farlo con ID fermata

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return len(result) > 0 #se la len è > 0 avrò true altrimenti false

    @staticmethod
    def getvicini(u): #restituisco una connessione!
        #seleziona tutti i vicini della fermata u passata
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione c where c.id_stazP = %s"
        cursor.execute(query, (u.id_fermata,))

        for row in cursor:
            result.append(Connessione(**row)) #INVECE di caricare le cose nella fermata le carico nella connessione
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione c"
        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesPesati():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT id_stazP, id_stazA, count(*) as peso 
                   FROM connessione c
                   group by id_stazP, id_stazA
                   order by peso desc"""
        #conta le righe uguali per una coopia, ovvero quanti archi esistono da u a v
        cursor.execute(query)

        #creo semplicemente una lista di tuple (stazP, stazA, peso) invece che un oggetto che dovrei creare
        for row in cursor:
            result.append((row["id_stazP"], row["id_stazA"], row["peso"]))

        cursor.close()
        conn.close()
        return result

    '''per ogni riga mi vado a prendere la velocità massima direttamente dal dao'''
    @staticmethod
    def getAllEdgesVel():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select c.id_stazA , c.id_stazA , max(l.velocita) as v
                    from connessione c, linea l
                    where l.id_linea = c.id_linea 
                    group by c.id_stazP , c.id_stazA 
                    order by v asc"""
        cursor.execute(query)

        for row in cursor:
            result.append((row["id_stazP"], row["id_stazA"], row["v"]))

        cursor.close()
        conn.close()
        return result