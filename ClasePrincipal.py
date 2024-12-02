import os
import mysql.connector
from Departamento import Departamento
from Empleado import Empleado
import informe
from Proyecto import Proyecto
from ProyectoEmpleado import ProyectoEmpleado
from RegistroTiempo import RegistroTiempo
from TipoEmpleado import TipoEmpleado
from prettytable import PrettyTable
import pandas as pd
import xlsxwriter
from Usuario import Usuario

def menu_usuario():
    """Menú principal donde el usuario puede elegir entre iniciar sesión """
    print("\n--- Menú ---")
    print("1. Iniciar sesión")
    print("2. Salir")

def mostrar_sub_menu_agregar():
    """Muestra el submenú para agregar nuevos registros."""
    print("=== Submenú de Agregar ===")
    print("1) Agregar departamento")
    print("2) Agregar Tipo de empleado")
    print("3) Agregar empleado")
    print("4) Agregar Proyecto")
    print("5) Agregar Usuario")
    print("6) Asignar trabajador a proyecto")
    print("===========================")

def buscar_datos_de():
    """Muestra las opciones de búsqueda disponibles."""
    print("=== Submenú de Búsqueda ===")
    print("1) Buscar departamento")
    print("2) Buscar empleado")
    print("3) Buscar Proyecto")
    print("============================")

def mostrar_sub_menu_editar():
    """Muestra las opciones para editar registros existentes."""
    print("=== Submenú de Edición ===")
    print("1) Editar departamento")
    print("2) Editar empleado")
    print("3) Editar Proyecto")
    print("4) Reasignar departamento")
    print("5) Reasignar proyecto")
    print("===========================")

def mostrar_sub_menu_eliminar():
    """Muestra las opciones para eliminar registros."""
    print("=== Submenú de Eliminación ===")
    print("1) Eliminar departamento")
    print("2) Eliminar empleado")
    print("3) Eliminar Proyecto")
    print("===============================")

def mostrar_sub_menu_informe():
    """Muestra las opciones para informes."""
    print("=== Submenú de Informes ===")
    print("1) Departamentos y sus trabajadores")
    print("2) Empleados de la empresa")
    print("3) Proyectos y sus trabajadores")
    print("4) Registro de tiempos de cada empleado")
    print("===============================")

# Crear directorio para almacenamiento si no existe
CARPETA = "sistema/"

def crear_directorio():
    """Crea un directorio para almacenamiento si no existe."""
    if not os.path.exists(CARPETA):
        os.makedirs(CARPETA)

def obtener_input_usuario(mensaje):
    """Obtiene y valida la entrada del usuario."""
    try:
        return int(input(mensaje))
    except ValueError:
        print("❌ Por favor, ingrese un número válido.")
        return None

def manejar_opcion_agregar(opcion):
    """Maneja la opción de agregar registros."""
    if opcion == 1:
        Departamento.obtener_info_departamento()
    elif opcion == 2:
        TipoEmpleado.obtener_info_tipo_empleado()
    elif opcion == 3:
        Empleado.obtener_info_empleado()
    elif opcion == 4:
        Proyecto.obtener_info_proyecto()
    elif opcion==5:
        usuario = Usuario()  # Crear una instancia de la clase Usuario
        usuario.agregar_usuario()  # Llamar al método de la instancia
        return
    elif opcion == 6:
        Proyecto.mostrar_proyectos()
        Empleado.mostrar_empleados()
        ProyectoEmpleado.asignar_Proyecto_A_Empleado()
        return
    else:
        print("❌ Opción no válida.")

def manejar_opcion_buscar(opcion):
    """Maneja la opción de búsqueda."""
    if opcion == 1:
        id_a_buscar = input("Ingrese el ID del departamento a buscar: ")
        Departamento.buscar_departamento(id_a_buscar)
        return
    elif opcion == 2:
        id_a_buscar = input("Ingrese el ID del empleado a buscar: ")
        Empleado.buscar_empleado(id_a_buscar)
        return
    elif opcion == 3:
        id_a_buscar = input("Ingrese el ID del proyecto a buscar: ")
        Proyecto.buscar_proyecto(id_a_buscar)
        return
    else:
        print("❌ Opción no válida.")

def manejar_opcion_editar(opcion):
    """Maneja la opción de editar registros."""
    if opcion == 1:
        Departamento.mostrar_departamentos()
        Departamento.editar_departamento(input("Ingrese el ID del departamento a editar: ")) 
    elif opcion == 2:
        Empleado.mostrar_empleados()
        Empleado.editar_empleado(input("Ingrese el ID del empleado a editar: "))         
    elif opcion == 3:
        Proyecto.mostrar_proyectos()
        Proyecto.editar_proyecto(input("Ingrese el ID del proyecto a editar: "))
    elif opcion == 4:
        Empleado.mostrar_resumen_empleados()
        print("Departamentos:")
        Departamento.mostrar_departamentos()
        id_empleado = input("Ingrese el ID del empleado que desea reasignar: ")
        nuevo_id_departamento = input("Ingrese el nuevo ID del departamento: ")
        Empleado.reasignar_departamento(id_empleado, nuevo_id_departamento)

    elif opcion == 5:
        Proyecto.mostrar_proyectos()
        print("Empleados:")
        Empleado.mostrar_empleados()
        id_proyecto = input("Ingrese el ID del proyecto al que desea reasignar al empleado: ")
        id_empleado = input("Ingrese el ID del empleado a reasignar: ")
        ProyectoEmpleado.asignar_Proyecto_A_Empleado(id_empleado, id_proyecto)
    else:
        print("❌ Opción no válida.")

def manejar_opcion_eliminar(opcion):
    """Maneja la opción de eliminar registros."""
    if opcion == 1:
        Departamento.mostrar_departamentos()
        id_departamento_a_eliminar = input("Ingrese el ID del departamento a eliminar: ")
        Departamento.eliminar_departamento(id_departamento_a_eliminar)
        
    elif opcion == 2:
        Empleado.mostrar_empleados()
        id_empleado_a_eliminar = input("Ingrese el ID del empleado a eliminar: ")
        Empleado.eliminar_empleado(id_empleado_a_eliminar)
        
    elif opcion == 3:
        Proyecto.mostrar_proyectos()
        id_proyecto_a_eliminar = input("Ingrese el ID del proyecto a eliminar: ")
        Proyecto.eliminar_proyecto(id_proyecto_a_eliminar)
        
    else:
        print("❌ Opción no válida.")

def manejar_opcion_informe(opcion):
    """Maneja la opción de informes."""
    if opcion == 1:
        Departamento.informe_departamentos_y_trabajadores()
    elif opcion == 2:
        Empleado.mostrar_empleados()
        Empleado.informe_empleados()
    elif opcion == 3:
        Proyecto.informe_proyectos_y_empleados()
    elif opcion == 4:
        RegistroTiempo.informe_registro_tiempos()
    else:
        print("❌ Opción no válida.")

def mostrar_menu_usuario(rol_id):
    """Muestra el menú basado en el rol del usuario."""
    print("\n--- Menú ---")
    
    # Administrador General
    if rol_id == 1:
        print("1. Agregar")
        print("2. Buscar")
        print("3. Editar")
        print("4. Eliminar")
        print("5. Registrar tiempo")
        print("6. Informe")
        print("7. Agregar Usuario")
        print("8. Salir")
        eleccion = obtener_input_usuario("Seleccione una opción: ")
        while True:
            if eleccion is None:
                continue  
            if eleccion == 1:  # Agregar
                    mostrar_sub_menu_agregar()
                    opcion = obtener_input_usuario("Seleccione una opción: ")
                    if opcion is not None:
                        manejar_opcion_agregar(opcion)

            elif eleccion == 2:  # Buscar
                    buscar_datos_de()
                    opcion = obtener_input_usuario("Ingrese una opción: ")
                    if opcion is not None:
                        manejar_opcion_buscar(opcion)

            elif eleccion == 3:  # Editar
                mostrar_sub_menu_editar()
                opcion = obtener_input_usuario("Ingrese una opción: ")
                if opcion is not None:
                    manejar_opcion_editar(opcion)

            elif eleccion == 4:  # Eliminar
                    mostrar_sub_menu_eliminar()
                    opcion = obtener_input_usuario("Ingrese una opción: ")
                    if opcion is not None:
                        manejar_opcion_eliminar(opcion)
                        return

            elif eleccion == 5:  # Registrar tiempo
                RegistroTiempo.obtener_info_registro_tiempo()

            elif eleccion == 6:  # Informe
                mostrar_sub_menu_informe()
                opcion = obtener_input_usuario("Seleccione una opción: ")
                if opcion is not None:
                    manejar_opcion_informe(opcion)

            elif eleccion == 7:  # Agregar Usuario
                        Empleado.mostrar_empleados()
                        nuevo_usuario = Usuario()  # Crear una instancia de Usuario para agregar un nuevo usuario
                        nuevo_usuario.agregar_usuario()  # Llamamos al método para agregar el usuario
                    
            elif eleccion == 8:  # Salir
                print("👋 Saliendo del sistema...")
                break

            else:
                print("❌ Opción no válida.")

    
    # Administrador Comercial
    elif rol_id == 2:
        print("1. Buscar")
        print("2. Editar")
        print("3. Registrar tiempo")
        print("4. Informe")
        print("5. Salir")

        eleccion = obtener_input_usuario("Seleccione una opción: ")
        while True:
            if eleccion is None:
                continue  

            elif eleccion == 1:  # Buscar
                    buscar_datos_de()
                    opcion = obtener_input_usuario("Ingrese una opción: ")
                    if opcion is not None:
                        manejar_opcion_buscar(opcion)

            elif eleccion == 2:  # Editar
                mostrar_sub_menu_editar()
                opcion = obtener_input_usuario("Ingrese una opción: ")
                if opcion is not None:
                    manejar_opcion_editar(opcion)


            elif eleccion == 3:  # Registrar tiempo
                RegistroTiempo.obtener_info_registro_tiempo()

            elif eleccion == 4:  # Informe
                mostrar_sub_menu_informe()
                opcion = obtener_input_usuario("Seleccione una opción: ")
                if opcion is not None:
                    manejar_opcion_informe(opcion)
                    
            elif eleccion == 5:  # Salir
                print("👋 Saliendo del sistema...")
                break

            else:
                print("❌ Opción no válida.")
    
    # Gerente de Área
    elif rol_id == 3:
        print("1. Buscar")
        print("2. Editar")
        print("3. Registrar tiempo")
        print("4. Salir")
        eleccion = obtener_input_usuario("Seleccione una opción: ")
        while True:
            if eleccion is None:
                continue  

            elif eleccion == 1:  # Buscar
                    buscar_datos_de()
                    opcion = obtener_input_usuario("Ingrese una opción: ")
                    if opcion is not None:
                        manejar_opcion_buscar(opcion)

            elif eleccion == 2:  # Editar
                mostrar_sub_menu_editar()
                opcion = obtener_input_usuario("Ingrese una opción: ")
                if opcion is not None:
                    manejar_opcion_editar(opcion)


            elif eleccion == 3:  # Registrar tiempo
                RegistroTiempo.obtener_info_registro_tiempo()

                    
            elif eleccion == 4:  # Salir
                print("👋 Saliendo del sistema...")
                break

            else:
                print("❌ Opción no válida.")
    
    
    # Técnico
    elif rol_id == 4:
        print("1. Registrar tiempo")
        print("2. Salir")
        eleccion = obtener_input_usuario("Seleccione una opción: ")
        while True:
            if eleccion is None:
                continue  

            elif eleccion == 3:  # Registrar tiempo
                RegistroTiempo.obtener_info_registro_tiempo()

                    
            elif eleccion == 2:  # Salir
                print("👋 Saliendo del sistema...")
                break

            else:
                print("❌ Opción no válida.")

    
    # Operario
    elif rol_id == 5:
        print("1. Registrar tiempo")
        print("2. Salir")
        eleccion = obtener_input_usuario("Seleccione una opción: ")
        while True:
            if eleccion is None:
                continue  

            elif eleccion == 3:  # Registrar tiempo
                RegistroTiempo.obtener_info_registro_tiempo()

                    
            elif eleccion == 4:  # Salir
                print("👋 Saliendo del sistema...")
                return

            else:
                print("❌ Opción no válida.")
    
    else:
        print("❌ Rol no reconocido.")




def app():
    """Función principal de la aplicación."""

    # Mostrar el menú de usuario
    menu_usuario()
    eleccion = obtener_input_usuario("Seleccione una opción: ")
    while True:

        if eleccion is None:
            continue
        if eleccion == 1:
            usuario = Usuario()  # Crear un objeto Usuario para iniciar sesión
            if usuario.iniciar_sesion():
                print("¡Inicio de sesión exitoso!")

            crear_directorio()
            mostrar_menu_usuario(usuario.rol_id)  # Mostrar el menú basado en el rol
            return
        elif eleccion == 2:
            print("👋 Saliendo del sistema...")
            return
        else:
            print("❌ Opción inválida. Intente de nuevo.")

# Ejecuta la aplicación si es el módulo principal
if __name__ == "__main__":
    app()
