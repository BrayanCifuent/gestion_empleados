
from sql import mydb


class ProyectoEmpleado:
    def __init__(self, id_asociacion, id_proyecto, id_empleado):
        self.id_asociacion = id_asociacion
        self.id_proyecto = id_proyecto
        self.id_empleado = id_empleado
    
    def asignar_Proyecto_A_Empleado():
        miCursor = mydb.cursor()

        while True:
            id_proyecto = input("Ingrese el ID del proyecto: ")
            id_empleado = input("Ingrese el ID del empleado: ")

            # Verificar si el proyecto existe y si está habilitado
            verifica_proyecto_sql = "SELECT habilitado FROM proyectos WHERE id_proyecto = %s"
            miCursor.execute(verifica_proyecto_sql, (id_proyecto,))
            resultado = miCursor.fetchone()

            if resultado is None:
                print("❌ El proyecto no existe. Por favor, intente de nuevo.")
                continue  # Pide el ID nuevamente

            habilitado = resultado[0]
            if not habilitado:
                print("❌ El proyecto está deshabilitado. No se puede asignar.")
                continue  # Pide el ID nuevamente

            # Verificar si el empleado ya está asignado al proyecto
            verifica_empleado_sql = "SELECT COUNT(*) FROM proyectoempleado WHERE id_proyecto = %s AND id_empleado = %s"
            miCursor.execute(verifica_empleado_sql, (id_proyecto, id_empleado))
            empleado_asignado = miCursor.fetchone()[0]

            if empleado_asignado > 0:
                print("❌ El empleado ya está asignado a este proyecto. Por favor, intente de nuevo.")
                continue  # Pide el ID nuevamente

            # Si pasa todas las verificaciones, insertar el registro
            sql = "INSERT INTO proyectoempleado (id_proyecto, id_empleado) VALUES (%s, %s)"
            val = (id_proyecto, id_empleado)
            miCursor.execute(sql, val)
            mydb.commit()
            print("✅ Registro exitoso.")
            print(f"Proyecto ID: {id_proyecto}, Empleado ID: {id_empleado}")
            break  # Sale del bucle si todo fue exitoso

        miCursor.close()  # Cierra el cursor