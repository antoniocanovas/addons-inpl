import xmlrpc.client
import pyodbc
import time

# ==========================================
# Configuración de conexión a Odoo
# ==========================================
ODOO_URL = "https://odoo-dev.inplast.es/"
ODOO_DB = "DEV"
ODOO_USERNAME = "usuario"       # Reemplazar con el usuario real
ODOO_PASSWORD = "contraseña"    # Reemplazar con la contraseña real

# ==========================================
# Configuración de conexión a SQL Server
# ==========================================
SQL_SERVER = "SERVERCLASS"
SQL_DATABASE = "ODOO_SQL"
SQL_USERNAME = "punt"
SQL_PASSWORD = "odoo2025"
SQL_TABLE = "ExportarEntradasOdoo"

def get_odoo_connection():

    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
    if not uid:
        raise Exception("Error en la autenticación en Odoo. Verifique sus credenciales.")
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    return uid, models

def read_sql_data():

    connection_string = (
        "Driver={SQL Server};"
        f"Server={SQL_SERVER};"
        f"Database={SQL_DATABASE};"
        f"UID={SQL_USERNAME};"
        f"PWD={SQL_PASSWORD};"
    )
    entradas = []
    try:
        with pyodbc.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                select_query = f"SELECT * FROM {SQL_TABLE}"
                cursor.execute(select_query)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                for row in rows:
                    row_dict = dict(zip(columns, row))
                    entradas.append(row_dict)
    except Exception as e:
        print("Ocurrió un error al leer la tabla SQL:", str(e))
    return entradas

def delete_sql_record(record_pk):

    connection_string = (
        "Driver={SQL Server};"
        f"Server={SQL_SERVER};"
        f"Database={SQL_DATABASE};"
        f"UID={SQL_USERNAME};"
        f"PWD={SQL_PASSWORD};"
    )
    try:
        with pyodbc.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                delete_query = f"DELETE FROM {SQL_TABLE} WHERE ID = ?"
                cursor.execute(delete_query, (record_pk,))
                conn.commit()
                print(f"Registro con ID {record_pk} borrado de SQL.")
    except Exception as e:
        print("Ocurrió un error al borrar el registro en SQL:", str(e))

def verify_odoo_record(odoo_id, uid, models):

    try:
        result = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'mig.inventario', 'search_read',
            [[['id', '=', odoo_id]]],
            {'limit': 1}
        )
        if result and isinstance(result, list) and len(result) > 0:
            return True
    except Exception as e:
        print("Error al verificar registro en Odoo:", str(e))
    return False


import datetime


def enviar_a_odoo_y_procesar(entrada, uid, models):
    # Obtener y convertir la fecha de fabricación
    fecha_fabricacion = entrada.get("FechaFabricacion")
    if fecha_fabricacion and isinstance(fecha_fabricacion, datetime.datetime):
        fecha_fabricacion = fecha_fabricacion.strftime("%Y-%m-%d")

    data = {
        "name": entrada.get("NewArticulo"),
        "qty": entrada.get("Unidades"),
        "ubicacion": entrada.get("CodigoUbicacion"),
        "ubicacion_old": entrada.get("New_hueco"),
        "lote": entrada.get("NLote"),
        "palet": entrada.get("Palet"),
        "sscc1": entrada.get("SSCC"),
        "sscc2": entrada.get("SSCC_2"),
        "boxsn": entrada.get("Cajas"),
        "mig_fechafabricacion": fecha_fabricacion,
    }
    try:
        # Crear el registro en Odoo
        odoo_record_id = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'mig.inventario', 'create', [data]
        )
        print(f"Registro creado en Odoo con ID: {odoo_record_id} para: {data}")

        time.sleep(0.5)

        if verify_odoo_record(odoo_record_id, uid, models):
            return True
        else:
            print(f"El registro con ID {odoo_record_id} no se verificó en Odoo.")
            return False
    except Exception as e:
        print("Error al crear registro en Odoo:", str(e))
        return False


def main():
    # 1. Leer todos los registros de la tabla SQL
    entradas = read_sql_data()
    if not entradas:
        print("No se encontraron entradas en la tabla SQL.")
        return
    print(f"Se encontraron {len(entradas)} entradas en la tabla SQL.")

    # 2. Conectar a Odoo
    try:
        uid, models = get_odoo_connection()
        print("Autenticación en Odoo exitosa. UID:", uid)
    except Exception as e:
        print(str(e))
        return

    # 3. Procesar cada registro de SQL
    for entrada in entradas:
        # Se asume que cada registro posee un campo 'id' que lo identifica en SQL
        sql_record_id = entrada.get("ID")
        if sql_record_id is None:
            print("El registro no posee campo 'id'. Se omite.")
            continue

        print(f"\nProcesando registro SQL con ID: {sql_record_id}")
        # Enviar a Odoo y verificar su creación
        if enviar_a_odoo_y_procesar(entrada, uid, models):
            # Si la verificación es exitosa, borrar el registro de SQL
            delete_sql_record(sql_record_id)
        else:
            print(f"No se pudo procesar correctamente el registro con ID {sql_record_id}. Se mantiene en SQL.")

if __name__ == '__main__':
    main()