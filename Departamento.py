import os
import mysql.connector
from prettytable import PrettyTable
import pandas as pd
import xlsxwriter
from sql import mydb

class Departamento:
    def __init__(self, id_departamento, nombre, telefono):
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.telefono = telefono

    def obtener_info_departamento():
        id_departamento = input("Ingrese el ID del departamento: ")
        nombre = input("Ingrese el nombre del departamento: ")
        telefono = input("Ingrese el teléfono del departamento: ")

        # Validar que el teléfono sea un número válido
        while True:
            if telefono.isdigit():
                break
            else:
                print("El teléfono debe contener solo dígitos. Intente nuevamente.")
                telefono = input("Ingrese el teléfono del departamento: ")

        try:
            with mydb.cursor() as miCursor:
                # Omite el cuarto valor ya que se asigna automáticamente
                sql = "INSERT INTO departamentos (id_departamento, nombre_departamentos, telefono) VALUES (%s, %s, %s)"
                val = (id_departamento, nombre, telefono)
                miCursor.execute(sql, val)
                mydb.commit()
                print(miCursor.rowcount, "Registro exitoso")
                return (id_departamento, nombre, telefono)
        except Exception as e:
            print(f"Ocurrió un error al registrar el departamento: {e}")

    def mostrar_departamentos():#solo muestra los departamentos habilitados
        miCusor = mydb.cursor()
        sql = "SELECT id_departamento, nombre_departamentos, telefono FROM departamentos WHERE habilitado = 1;"
        miCusor.execute(sql)
        departamentos = miCusor.fetchall()

        # Crear la tabla
        print("Departamentos habilitados")
        tabla = PrettyTable()
        tabla.field_names = ["ID Departamento", "Nombre", "Teléfono"]

        # Añadir filas a la tabla
        for departamento in departamentos:
            tabla.add_row(departamento)

        print(tabla)
    
    def buscar_departamento(id_departamento):
        miCusor = mydb.cursor()
        sql = "SELECT * FROM departamentos WHERE id_departamento = %s"
        miCusor.execute(sql, (id_departamento,))
        departamento = miCusor.fetchone()
        
        if departamento:
            estado_habilitado = "habilitado" if departamento[3] == 1 else "deshabilitado"  # Suponiendo que habilitado es la cuarta columna
            print("ID departamento:", departamento[0])
            print("Nombre:", departamento[1])
            print("Teléfono:", departamento[2])
            print("Estado:", estado_habilitado)
        else:
            print("Departamento no encontrado.")
            

    def editar_departamento(id_departamento):
        miCusor = mydb.cursor()
        sql = "SELECT * FROM departamentos WHERE id_departamento = %s"
        miCusor.execute(sql, (id_departamento,))
        departamento = miCusor.fetchone()

        if departamento:
            print("Departamento encontrado:")
            print("ID departamento:", departamento[0], "Nombre:", departamento[1], "Teléfono:", departamento[2])

            nuevo_nombre = input("Ingrese el nuevo nombre del departamento (dejar en blanco para no cambiar): ")
            
            nuevo_telefono = ""
            while True:
                nuevo_telefono = input("Ingrese el nuevo teléfono del departamento (dejar en blanco para no cambiar): ")
                if nuevo_telefono == "" or nuevo_telefono.isdigit():
                    break
                else:
                    print("Error: El teléfono debe contener solo números. Inténtalo de nuevo.")

            if nuevo_nombre == "":
                nuevo_nombre = departamento[1]
            if nuevo_telefono == "":
                nuevo_telefono = departamento[2]

            sql_update = "UPDATE departamentos SET nombre_departamentos = %s, telefono = %s WHERE id_departamento = %s"
            miCusor.execute(sql_update, (nuevo_nombre, nuevo_telefono, id_departamento))
            mydb.commit()
            print("Departamento actualizado exitosamente.")
        else:
            print("Departamento no encontrado.")

    def reasignar_empleados(id_departamento_antiguo, id_departamento_nuevo):
        try:
            with mydb.cursor() as miCursor:
                sql = "UPDATE empleado SET id_departamento = %s WHERE id_departamento = %s"
                miCursor.execute(sql, (id_departamento_nuevo, id_departamento_antiguo))
                mydb.commit()
                print(f"Empleados reasignados del departamento {id_departamento_antiguo} al departamento {id_departamento_nuevo}.")
        except Exception as e:
            print(f"Ocurrió un error al reasignar empleados: {e}")

    def eliminar_departamento(id_departamento):
        try:
            # Verifica si hay empleados asociados a este departamento
            with mydb.cursor() as miCursor:
                sql = "SELECT COUNT(*) FROM empleado WHERE id_departamento = %s"
                miCursor.execute(sql, (id_departamento,))
                count = miCursor.fetchone()[0]

                if count > 0:
                    print("No se puede deshabilitar el departamento. Hay empleados asociados a él.")
                    
                    # Pregunta si desea reasignar empleados
                    opcion = input("¿Desea reasignar empleados a otro departamento? (s/n): ").lower()
                    if opcion == 's':
                        id_departamento_nuevo = input("Ingrese el ID del nuevo departamento: ")
                        Departamento.reasignar_empleados(id_departamento, id_departamento_nuevo)

                        # Confirmación de deshabilitación del departamento
                        confirmacion = input("¿Confirma la deshabilitación del departamento? (s/n): ").lower()
                        if confirmacion == 's':
                            sql = "UPDATE departamentos SET habilitado = 0 WHERE id_departamento = %s"
                            miCursor.execute(sql, (id_departamento,))
                            mydb.commit()
                            print("Departamento deshabilitado exitosamente.")
                        else:
                            print("Deshabilitación del departamento cancelada.")
                    return  # Termina la función
                else:
                    # Si no hay empleados, procede a deshabilitar
                    sql = "UPDATE departamentos SET habilitado = 0 WHERE id_departamento = %s"
                    miCursor.execute(sql, (id_departamento,))
                    mydb.commit()
                    print("Departamento deshabilitado exitosamente.")
        except Exception as e:
            print(f"Ocurrió un error al deshabilitar el departamento: {e}")
            
    def informe_departamentos_y_trabajadores():
        try:
            with mydb.cursor() as miCursor:
                # Consulta que une departamentos con empleados
                sql = """
                SELECT d.id_departamento, d.nombre_departamentos, d.telefono, e.id_empleado, e.nombre, e.habilitado
                FROM departamentos d
                LEFT JOIN empleado e ON d.id_departamento = e.id_departamento
                """
                miCursor.execute(sql)
                resultados = miCursor.fetchall()

                # Crear la tabla para el informe
                tabla = PrettyTable()
                tabla.field_names = ["ID Departamento", "Nombre Departamento", "Teléfono", "ID Empleado", "Nombre Empleado", "Habilitado"]
                tabla.align = "l"  # Alinear a la izquierda
                tabla.padding_width = 1  # Espaciado entre columnas

                # Añadir filas a la tabla
                for fila in resultados:
                    id_departamento, nombre_departamento, telefono, id_empleado, nombre_empleado, habilitado = fila
                    habilitado_texto = "Sí" if habilitado else "No"  # Convertir a texto

                    # Agregar a la tabla
                    tabla.add_row([id_departamento, nombre_departamento, telefono, id_empleado if id_empleado else "Sin empleado", nombre_empleado if nombre_empleado else "Sin empleado", habilitado_texto])

                print(tabla)

                # Preparar datos para exportar a Excel
                datos = []
                for fila in resultados:
                    id_departamento, nombre_departamento, telefono, id_empleado, nombre_empleado, habilitado = fila
                    habilitado_texto = "Sí" if habilitado else "No"
                    datos.append([id_departamento, nombre_departamento, telefono, id_empleado if id_empleado else "Sin empleado", nombre_empleado if nombre_empleado else "Sin empleado", habilitado_texto])

                # Exportar a Excel
                df = pd.DataFrame(datos, columns=["ID Departamento", "Nombre Departamento", "Teléfono", "ID Empleado", "Nombre Empleado", "Habilitado"])
                with pd.ExcelWriter("informe_departamentos.xlsx", engine='xlsxwriter') as writer:
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
                    worksheet.set_column('A:A', 15)  # ID Departamento
                    worksheet.set_column('B:B', 30)  # Nombre Departamento
                    worksheet.set_column('C:C', 15)  # Teléfono
                    worksheet.set_column('D:D', 15)  # ID Empleado
                    worksheet.set_column('E:E', 30)  # Nombre Empleado
                    worksheet.set_column('F:F', 10)  # Habilitado

                print("Informe exportado exitosamente a informe_departamentos.xlsx.")
        except Exception as e:
            print(f"Ocurrió un error al generar el informe: {e}")