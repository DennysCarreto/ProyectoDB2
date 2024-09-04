import mysql.connector


class CConexion:
    def conexionDB(self):
        conexion = None
        try:
            # user = usuario que colocaron al instalar workbench o al crear la conexion
            # paswword = es la que colocaron al instalar mysql o workbench
            # host = puede ser localhost(para local) o una ip de otro equipo
            # database = nombre de la base de datos
            # port = puerto de conexion que aparece en workbench
            conexion = mysql.connector.connect(user='Denys', password='admin',
                                               host='192.168.204.253', database='hotel_perza',
                                               port='3306')
            print('Conexion Correcta')
        except mysql.connector.Error as error:
            print('Error al conectar a la DB {}'.format(error))
        return conexion


conectar = CConexion()
conectar.conexionDB()

