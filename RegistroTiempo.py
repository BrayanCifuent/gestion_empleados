
from prettytable import PrettyTable
import pandas as pd
import xlsxwriter
from sql import mydb

class RegistroTiempo:
    def __init__(self, id_registrar,id_empleado, fecha, horas,tareas, id_proyecto):
        self.id_registrar = id_registrar
        self.id_empleado = id_empleado
        self.fecha = fecha
        self.horas= horas
        self.tareas = tareas
        self.id_proyecto = id_proyecto

    def obtener_info_registro_tiempo():
        id_registrar = None  # Asumiendo que este se genera automáticamente en la base de datos

        # Validar ID del empleado
        while True:
            id_empleado = input("Ingrese el ID del trabajador: ")
            if RegistroTiempo.validar_id_empleado(id_empleado):
                break
            print("❌ ID de empleado no válido. Intente nuevamente.")

        # Obtener la fecha como cadena de texto
        fecha = input("Ingrese la fecha en la que trabajó (YYYY-MM-DD): ")

        # Validación de horas
        while True:
            horas = input("Ingrese las horas que trabajó: ")
            try:
                horas = float(horas)
                if horas < 0:
                    raise ValueError("Las horas no pueden ser negativas.")
                break
            except ValueError:
                print("❌ Por favor, ingrese un número válido de horas.")

        tareas = input("Ingrese las tareas realizadas: ")

        # Validar ID del proyecto
        while True:
            id_proyecto = input("Ingrese el ID del proyecto trabajado: ")
            if RegistroTiempo.validar_id_proyecto(id_proyecto):
                break
            print("❌ ID de proyecto no válido. Intente nuevamente.")

        try:
            miCursor = mydb.cursor()
            sql = "INSERT INTO registrartiempo VALUES (%s, %s, %s, %s, %s, %s)"
            val = (id_registrar, id_empleado, fecha, horas, tareas, id_proyecto)
            miCursor.execute(sql, val)
            mydb.commit()
            print("✅ Registro exitoso:")
            print(f"ID Empleado: {id_empleado}\nFecha: {fecha}\nHoras: {horas}\nTareas: {tareas}\nID Proyecto: {id_proyecto}")
            return RegistroTiempo(id_registrar, id_empleado, fecha, horas, tareas, id_proyecto)
        except Exception as e:
            print(f"❌ Ocurrió un error al registrar el tiempo: {e}")


    def validar_id_empleado(id_empleado):
        # Validar que el ID de empleado existe en la base de datos
        try:
            miCursor = mydb.cursor()
            sql = "SELECT COUNT(*) FROM empleado WHERE id_empleado = %s"
            miCursor.execute(sql, (id_empleado,))
            resultado = miCursor.fetchone()[0]
            return resultado > 0
        except Exception as e:
            print(f"❌ Ocurrió un error al validar el ID de empleado: {e}")
            return False

    def validar_id_proyecto(id_proyecto):
        # Validar que el ID de proyecto existe en la base de datos
        try:
            miCursor = mydb.cursor()
            sql = "SELECT COUNT(*) FROM proyectos WHERE id_proyecto = %s"
            miCursor.execute(sql, (id_proyecto,))
            resultado = miCursor.fetchone()[0]
            return resultado > 0
        except Exception as e:
            print(f"❌ Ocurrió un error al validar el ID de proyecto: {e}")
            return False
        
    def informe_registro_tiempos():
        try:
            with mydb.cursor() as miCursor:
                # Consulta que une registros de tiempo con empleados y proyectos
                sql = """
                SELECT rt.fecha, rt.horas, rt.tareas, rt.id_proyecto, e.id_empleado, e.nombre AS nombre_empleado
                FROM registrartiempo rt
                JOIN empleado e ON rt.id_empleado = e.id_empleado
                """
                miCursor.execute(sql)
                resultados = miCursor.fetchall()

                # Crear la tabla para el informe
                tabla = PrettyTable()
                tabla.field_names = ["ID Empleado", "Nombre Empleado", "Registros"]
                tabla.align = "l"  # Alinear a la izquierda
                tabla.padding_width = 1  # Espaciado entre columnas

                # Diccionario para almacenar registros de tiempo por empleado
                registros_dict = {}

                for fila in resultados:
                    fecha, horas, tareas, id_proyecto, id_empleado, nombre_empleado = fila

                    if id_empleado not in registros_dict:
                        registros_dict[id_empleado] = [nombre_empleado, []]

                    # Agregar el registro de tiempo
                    registros_dict[id_empleado][1].append((fecha, horas, tareas, id_proyecto))

                # Añadir filas a la tabla
                for id_empleado, (nombre_empleado, registros) in registros_dict.items():
                    registros_str = "\n".join(f"Fecha: {fecha}, Horas: {horas}, Tareas: {tareas}, ID Proyecto: {id_proyecto}"
                                              for fecha, horas, tareas, id_proyecto in registros)
                    tabla.add_row([id_empleado, nombre_empleado, registros_str])

                print(tabla)

                # Preparar datos para exportar a Excel
                datos = []
                for id_empleado, (nombre_empleado, registros) in registros_dict.items():
                    registros_str = "\n".join(f"Fecha: {fecha}, Horas: {horas}, Tareas: {tareas}, ID Proyecto: {id_proyecto}"
                                              for fecha, horas, tareas, id_proyecto in registros)
                    datos.append([id_empleado, nombre_empleado, registros_str])

                # Exportar a Excel
                df = pd.DataFrame(datos, columns=["ID Empleado", "Nombre Empleado", "Registros"])
                with pd.ExcelWriter("informe_registro_tiempos.xlsx", engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name="Informe")

                    # Formatear encabezados
                    workbook = writer.book
                    worksheet = writer.sheets["Informe"]
                    header_format = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'yellow'})
                    cell_format = workbook.add_format({'border': 1, 'align': 'left', 'valign': 'vcenter'})

                    # Escribir encabezados
                    for col_num, value in enumerate(df.columns):
                        worksheet.write(0, col_num, value, header_format)

                    # Aplicar formato a todas las celdas
                    for row in range(1, len(datos) + 1):
                        for col in range(len(df.columns)):
                            worksheet.write(row, col, datos[row - 1][col], cell_format)

                    # Ajustar el ancho de las columnas
                    worksheet.set_column('A:A', 15)  # ID Empleado
                    worksheet.set_column('B:B', 30)  # Nombre Empleado
                    worksheet.set_column('C:C', 50)  # Registros

                print("Informe exportado exitosamente a informe_registro_tiempos.xlsx.")
        except Exception as e:
            print(f"Ocurrió un error al generar el informe: {e}")