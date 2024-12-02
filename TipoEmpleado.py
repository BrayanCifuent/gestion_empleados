from sql import mydb

class TipoEmpleado:
    def __init__(self, id_tipo, tipo, detalle):
        self.id_tipo = id_tipo
        self.tipo = tipo
        self.detalle = detalle


    def obtener_info_tipo_empleado():
        id_tipo = input("Ingrese el ID del tipo de empleado: ")
        tipo = input("Ingrese el tipo de empleado: ")
        detalle = input("Ingrese el detalle del tipo de empleado: ")

        # Validar entradas (opcional)
        if not id_tipo or not tipo or not detalle:
            print("Todos los campos son obligatorios.")
            return None

        try:
            with mydb.cursor() as miCursor:
                sql = "INSERT INTO tipo_empleados VALUES (%s, %s, %s)"
                val = (id_tipo, tipo, detalle)
                miCursor.execute(sql, val)
                mydb.commit()
                print(miCursor.rowcount, "Registro exitoso")
                print(f"ID: {id_tipo}, Tipo: {tipo}, Detalle: {detalle}")
                return (id_tipo, tipo, detalle)
        except Exception as e:
            print(f"Ocurrió un error al registrar el tipo de empleado: {e}")

    def mostrar_tipos_empleados():
        miCusor = mydb.cursor()
        sql = "SELECT *FROM tipo_empleados "
        miCusor.execute(sql)
        tipos_de_empleados= miCusor.fetchall()
        print("Tipos de empleados")
        print (tipos_de_empleados)
    
    def buscar_tipo_empleado():
        id_tipo = input("Ingrese el ID del tipo de empleado que desea buscar: ")
        miCursor = mydb.cursor()
        sql = "SELECT * FROM tipo_empleados WHERE id_tipo_empleado = %s"
        miCursor.execute(sql, (id_tipo,))
        resultado = miCursor.fetchone()
        if resultado:
            print(f"Empleado encontrado: ID: {resultado[0]}, Tipo: {resultado[1]}, Detalle: {resultado[2]}")
        else:
            print("No se encontró el tipo de empleado.")