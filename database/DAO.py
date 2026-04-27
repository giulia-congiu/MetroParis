from database.DB_connect import DBConnect
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
    def hasconn(u: Fermata, v: Fermata) -> bool: #mi aspetto ogetti di tipo fermata e un bool come ritorno
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
    def getvicini(u):
        #seleziona tutti i vicini della fermata u passata
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione c where c.id_stazP = %s"
        cursor.execute(query, (u.id_fermata,))

        for row in cursor:
            result.append(Fermata(**row))
        cursor.close()
        conn.close()
        return result