import mysql.connector
from prettytable import PrettyTable
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from sql import mydb


class Proyecto:
    def __init__(self, id_proyecto, nombre, descripcion, fecha_inicio):
        self.id_proyecto = id_proyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
    def obtener_info_proyecto():
        id_proyecto = input("Ingrese el ID del proyecto: ")
        nombre = input("Ingrese el nombre del proyecto: ")
        descripcion = input("Ingrese la descripción del proyecto: ")
        fecha_inicio = input("Ingrese la fecha de inicio del proyecto (YYYY-MM-DD): ")
        
        miCursor = mydb.cursor()
        
        # no inclute la columna 'habilitado' ya que se asigna automaticamente
        sql = "INSERT INTO proyectos (id_proyecto, nombre_proyecto, descripcion, fecha_inicio) VALUES (%s, %s, %s, %s)"
        val = (id_proyecto, nombre, descripcion, fecha_inicio)
        
        miCursor.execute(sql, val)
        mydb.commit()
        
        print(miCursor.rowcount, "Registro exitoso")
        print(f"ID: {id_proyecto}, Nombre: {nombre}, Detalle: {descripcion}, Fecha Inicio: {fecha_inicio}")
        
        return Proyecto(id_proyecto, nombre, descripcion, fecha_inicio)
        
    def buscar_proyecto(id_proyecto):
        try:
            miCursor = mydb.cursor()
            sql = "SELECT * FROM proyectos WHERE id_proyecto = %s"
            miCursor.execute(sql, (id_proyecto,))
            proyecto = miCursor.fetchone()

            if proyecto:
                habilitado = "Sí" if proyecto[4] else "No"  # Asumiendo que 'habilitado' es el quinto atributo
                print(f"Proyecto encontrado: ID: {proyecto[0]}, Nombre: {proyecto[1]}, Descripción: {proyecto[2]}, Fecha de Inicio: {proyecto[3]}, Habilitado: {habilitado}")
            else:
                print("Proyecto no encontrado.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")
        finally:
            miCursor.close()


    def mostrar_proyectos(): #solo muestra los departamentos habilitados
        try:
            miCusor = mydb.cursor()
            sql = "SELECT * FROM proyectos WHERE habilitado = 1"  # Filtrar proyectos habilitados
            miCusor.execute(sql)
            proyectos = miCusor.fetchall()

            # Crear una tabla con PrettyTable
            tabla = PrettyTable()
            tabla.field_names = ["ID", "Nombre", "Descripción", "Fecha de Inicio"]

            for proyecto in proyectos:
                tabla.add_row([proyecto[0], proyecto[1], proyecto[2], proyecto[3]])

            print("\nProyectos habilitados:")
            print(tabla)

        except Exception as e:
            print(f"Ocurrió un error al mostrar proyectos: {e}")
        
        finally:
            miCusor.close()  # Asegúrate de cerrar el cursor
    
    def editar_proyecto(id_proyecto):
        miCursor = mydb.cursor()
        # Buscar el proyecto
        sql = "SELECT * FROM proyectos WHERE id_proyecto = %s"
        miCursor.execute(sql, (id_proyecto,))
        proyecto = miCursor.fetchone()

        if proyecto:
            # Convertir la tupla a una lista para poder modificarla
            proyecto_lista = list(proyecto)
            print(f"Proyecto actual: ID: {proyecto_lista[0]}, Nombre: {proyecto_lista[1]}, Descripción: {proyecto_lista[2]}, Fecha de Inicio: {proyecto_lista[3]}")

            # Solicitar nuevos datos
            nuevo_nombre = input("Nuevo nombre (dejar vacío para no cambiar): ")
            nuevo_descripcion = input("Nueva descripción (dejar vacío para no cambiar): ")
            nueva_fecha_inicio = input("Nueva fecha de inicio (YYYY-MM-DD, dejar vacío para no cambiar): ")

            # Actualizar solo si se proporciona un nuevo valor
            if nuevo_nombre:
                proyecto_lista[1] = nuevo_nombre
            if nuevo_descripcion:
                proyecto_lista[2] = nuevo_descripcion
            if nueva_fecha_inicio:
                proyecto_lista[3] = nueva_fecha_inicio

            # Preparar y ejecutar la actualización
            sql = "UPDATE proyectos SET nombre_proyecto = %s, descripcion = %s, fecha_inicio = %s WHERE id_proyecto = %s"
            miCursor.execute(sql, (proyecto_lista[1], proyecto_lista[2], proyecto_lista[3], id_proyecto))
            mydb.commit()
            print("Proyecto actualizado con éxito.")
        else:
            print("Proyecto no encontrado.")

    def eliminar_proyecto(id_proyecto):
        miCursor = mydb.cursor()
        try:
            # Intentar deshabilitar el proyecto
            sql = "UPDATE proyectos SET habilitado = 0 WHERE id_proyecto = %s"
            miCursor.execute(sql, (id_proyecto,))
            mydb.commit()
            
            if miCursor.rowcount > 0:  # Verificar si se deshabilitó algún registro
                print(f"Proyecto con ID {id_proyecto} deshabilitado con éxito.")
            else:
                print(f"No se encontró un proyecto con ID {id_proyecto}.")
        
        except mysql.connector.IntegrityError:
            print("No se pudo deshabilitar el proyecto debido a referencias en registrartiempo.")
        
        except Exception as e:
            print(f"Ocurrió un error al deshabilitar el proyecto: {e}")
        
        finally:
            miCursor.close()
    def informe_proyectos_y_empleados():
        try:
            with mydb.cursor() as miCursor:
                # Consulta que une proyectos con empleados
                sql = """
                SELECT p.id_proyecto, p.nombre_proyecto, p.descripcion, e.id_empleado, e.nombre AS nombre_empleado
                FROM proyectos p
                LEFT JOIN proyectoempleado pe ON p.id_proyecto = pe.id_proyecto
                LEFT JOIN empleado e ON pe.id_empleado = e.id_empleado
                """
                miCursor.execute(sql)
                resultados = miCursor.fetchall()

                # Crear la tabla para el informe
                tabla = PrettyTable()
                tabla.field_names = ["ID Proyecto", "Nombre Proyecto", "Descripción", "Empleados"]
                tabla.align = "l"  # Alinear a la izquierda
                tabla.padding_width = 1  # Espaciado entre columnas

                # Diccionario para almacenar proyectos y sus empleados
                proyectos_dict = {}

                for fila in resultados:
                    id_proyecto = fila[0]
                    nombre_proyecto = fila[1]
                    descripcion = fila[2]
                    id_empleado = fila[3]
                    nombre_empleado = fila[4]

                    if id_proyecto not in proyectos_dict:
                        proyectos_dict[id_proyecto] = [nombre_proyecto, descripcion, []]
                    
                    if id_empleado:  # Solo si hay un empleado
                        proyectos_dict[id_proyecto][2].append((id_empleado, nombre_empleado))

                # Añadir filas a la tabla
                for id_proyecto, (nombre_proyecto, descripcion, empleados) in proyectos_dict.items():
                    if empleados:
                        empleados_list = "\n".join(f"ID: {id_emp} - Nombre: {nom_emp}" for id_emp, nom_emp in empleados)
                    else:
                        empleados_list = "Sin empleados"
                        
                    tabla.add_row([id_proyecto, nombre_proyecto, descripcion, empleados_list])

                print(tabla)

                # Preparar datos para exportar a Excel
                datos = []
                for id_proyecto, (nombre_proyecto, descripcion, empleados) in proyectos_dict.items():
                    empleados_list = "\n".join(f"ID: {id_emp} - Nombre: {nom_emp}" for id_emp, nom_emp in empleados) if empleados else "Sin empleados"
                    datos.append([id_proyecto, nombre_proyecto, descripcion, empleados_list])
                    
                # Exportar a Excel
                df = pd.DataFrame(datos, columns=["ID Proyecto", "Nombre Proyecto", "Descripción", "Empleados"])
                with pd.ExcelWriter("informe_proyectos.xlsx", engine='xlsxwriter') as writer:
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
                    worksheet.set_column('A:A', 15)  # ID Proyecto
                    worksheet.set_column('B:B', 30)  # Nombre Proyecto
                    worksheet.set_column('C:C', 40)  # Descripción
                    worksheet.set_column('D:D', 40)  # Empleados

                print("Informe exportado exitosamente a informe_proyectos.xlsx.")
        except Exception as e:
            print(f"Ocurrió un error al generar el informe: {e}")