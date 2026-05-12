from django.conf import settings
import psycopg2
import psycopg2.extras

class ConexionDB:
    def conectar(self):
        return psycopg2.connect(
            host=settings.DB_CONFIG['HOST'],
            user=settings.DB_CONFIG['USER'],
            password=settings.DB_CONFIG['PASSWORD'],
            dbname=settings.DB_CONFIG['NAME'],
            port=settings.DB_CONFIG['PORT']
        )
    
    def ejecutar(self, sql, params=None):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute(sql, params)
        conexion.commit()
        cursor.close()
        conexion.close()

    def verificar(self, sql, params=None):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute(sql, params)
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado is not None

    def consultar(self, sql, params=None):
        conexion = self.conectar()
        # Usamos RealDictCursor para simular el DictCursor de pymysql
        cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql, params)
        resultado = cursor.fetchall()
        cursor.close()
        conexion.close()
        return resultado