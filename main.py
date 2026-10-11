from views import *
from shared.herramientas import (
    imprimir_titulo,
    imprimir_exito,
    imprimir_error,
    imprimir_info
)


def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_lista(objetos):
    if len(objetos) == 0:
        imprimir_info("No hay registros.")
    else:
        for objeto in objetos:
            print(objeto.etiqueta())


def mostrar_detalle(objeto):
    if objeto is None:
        imprimir_error("Registro no encontrado.")
    else:
        for campo, valor in objeto.a_diccionario().items():
            print(f"{campo}: {valor}")


def menu_estudiantes():
    while True:
        imprimir_titulo("MENÚ DE ESTUDIANTES")
        print("1. Crear estudiante")
        print("2. Ver todos")
        print("3. Buscar estudiante")
        print("4. Ver por ID")
        print("5. Actualizar estudiante")
        print("6. Eliminar estudiante")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            datos = {
                "nombre": input("Nombre: "),
                "apellido": input("Apellido: "),
                "email": input("Email: "),
                "carnet": input("Carnet: "),
                "carrera": input("Carrera: ")
            }

            exito, mensaje = crear_estudiante(datos)

            if exito:
                imprimir_exito(mensaje)
            else:
                imprimir_error(mensaje)

        elif opcion == "2":
            mostrar_lista(obtener_estudiantes())

        elif opcion == "3":
            termino = input("Ingrese el nombre o carnet: ")
            mostrar_lista(buscar_estudiantes(termino))

        elif opcion == "4":
            try:
                id_registro = int(input("ID del estudiante: "))
                mostrar_detalle(obtener_estudiante(id_registro))
            except ValueError:
                imprimir_error("Ingrese un ID numérico.")

        elif opcion == "5":
            try:
                id_registro = int(input("ID del estudiante: "))
                estudiante = obtener_estudiante(id_registro)

                if estudiante is None:
                    imprimir_error("Estudiante no encontrado.")
                else:
                    datos = {
                        "nombre": input("Nombre: "),
                        "apellido": input("Apellido: "),
                        "email": input("Email: "),
                        "carnet": input("Carnet: "),
                        "carrera": input("Carrera: ")
                    }

                    exito, mensaje = actualizar_estudiante(
                        id_registro, datos
                    )

                    if exito:
                        imprimir_exito(mensaje)
                    else:
                        imprimir_error(mensaje)

            except ValueError:
                imprimir_error("Ingrese un ID numérico.")

        elif opcion == "6":
            try:
                id_registro = int(input("ID del estudiante: "))
                exito, mensaje = eliminar_estudiante(id_registro)

                if exito:
                    imprimir_exito(mensaje)
                else:
                    imprimir_error(mensaje)

            except ValueError:
                imprimir_error("Ingrese un ID numérico.")

        elif opcion == "0":
            break

        else:
            imprimir_error("Opción incorrecta.")

        pausa()


def menu_materias():
    while True:
        imprimir_titulo("MENÚ DE MATERIAS")
        print("1. Crear materia")
        print("2. Ver todas")
        print("3. Buscar materia")
        print("4. Ver por ID")
        print("5. Actualizar materia")
        print("6. Eliminar materia")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            datos = {
                "nombre": input("Nombre: "),
                "codigo": input("Código: "),
                "creditos": input("Créditos: "),
                "cupos": input("Cupos disponibles: ")
            }

            exito, mensaje = crear_materia(datos)

            if exito:
                imprimir_exito(mensaje)
            else:
                imprimir_error(mensaje)

        elif opcion == "2":
            mostrar_lista(obtener_materias())

        elif opcion == "3":
            termino = input("Nombre o código: ")
            mostrar_lista(buscar_materias(termino))

        elif opcion == "4":
            try:
                id_registro = int(input("ID de la materia: "))
                mostrar_detalle(obtener_materia(id_registro))
            except ValueError:
                imprimir_error("Ingrese un ID numérico.")

        elif opcion == "5":
            try:
                id_registro = int(input("ID de la materia: "))
                materia = obtener_materia(id_registro)

                if materia is None:
                    imprimir_error("Materia no encontrada.")
                else:
                    datos = {
                        "nombre": input("Nombre: "),
                        "codigo": input("Código: "),
                        "creditos": input("Créditos: "),
                        "cupos": input("Cupos disponibles: ")
                    }

                    exito, mensaje = actualizar_materia(
                        id_registro, datos
                    )

                    if exito:
                        imprimir_exito(mensaje)
                    else:
                        imprimir_error(mensaje)

            except ValueError:
                imprimir_error("Ingrese un ID numérico.")

        elif opcion == "6":
            try:
                id_registro = int(input("ID de la materia: "))
                exito, mensaje = eliminar_materia(id_registro)

                if exito:
                    imprimir_exito(mensaje)
                else:
                    imprimir_error(mensaje)

            except ValueError:
                imprimir_error("Ingrese un ID numérico.")

        elif opcion == "0":
            break

        else:
            imprimir_error("Opción incorrecta.")

        pausa()


def menu_matriculas():
    while True:
        imprimir_titulo("MENÚ DE MATRÍCULAS")
        print("1. Matricular estudiante")
        print("2. Ver todas")
        print("3. Registrar nota")
        print("4. Ver certificado")
        print("5. Retirar matrícula")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                datos = {
                    "estudiante_id": int(input("ID del estudiante: ")),
                    "materia_id": int(input("ID de la materia: ")),
                    "periodo": input("Período: "),
                    "fecha": input("Fecha (AAAA-MM-DD): ")
                }

                exito, mensaje = crear_matricula(datos)

                if exito:
                    imprimir_exito(mensaje)
                else:
                    imprimir_error(mensaje)

            except ValueError:
                imprimir_error("Los ID deben ser números.")

        elif opcion == "2":
            mostrar_lista(obtener_matriculas())

        elif opcion == "3":
            try:
                id_registro = int(input("ID de la matrícula: "))
                nota = float(input("Nota (0 a 20): "))

                exito, mensaje = registrar_nota(id_registro, nota)

                if exito:
                    imprimir_exito(mensaje)
                else:
                    imprimir_error(mensaje)

            except ValueError:
                imprimir_error("Ingrese números válidos.")

        elif opcion == "4":
            try:
                id_registro = int(input("ID de la matrícula: "))
                datos = certificado(id_registro)

                if datos is None:
                    imprimir_error("No se pudo generar el certificado.")
                else:
                    matricula = datos["matricula"]
                    estudiante = datos["estudiante"]
                    materia = datos["materia"]

                    imprimir_titulo(
                        f"CERTIFICADO #{matricula.id}"
                    )
                    print(f"Período: {matricula.periodo}")
                    print(
                        f"Estudiante: {estudiante.nombre} "
                        f"{estudiante.apellido}"
                    )
                    print(f"Carnet: {estudiante.carnet}")
                    print(
                        f"Materia: {materia.nombre} "
                        f"({materia.codigo})"
                    )
                    print(f"Créditos: {materia.creditos}")
                    print(f"Nota: {matricula.notas}")
                    print(f"Estado: {matricula.estado()}")

            except ValueError:
                imprimir_error("Ingrese un ID numérico.")

        elif opcion == "5":
            try:
                id_registro = int(input("ID de la matrícula: "))
                exito, mensaje = retirar_matricula(id_registro)

                if exito:
                    imprimir_exito(mensaje)
                else:
                    imprimir_error(mensaje)

            except ValueError:
                imprimir_error("Ingrese un ID numérico.")

        elif opcion == "0":
            break

        else:
            imprimir_error("Opción incorrecta.")

        pausa()


def mostrar_resumen():
    imprimir_titulo("RESUMEN ACADÉMICO")

    estudiantes = obtener_estudiantes()
    materias = obtener_materias()
    matriculas = obtener_matriculas()

    # El conjunto evita repetir carreras.
    carreras = set()

    for estudiante in estudiantes:
        if estudiante.carrera != "":
            carreras.add(estudiante.carrera)

    print(f"Total de estudiantes: {len(estudiantes)}")
    print("Carreras registradas:")

    for carrera in sorted(carreras):
        print(f"- {carrera}")

    print(f"Materias sin cupo: {len(materias_sin_cupo())}")

    aprobadas = 0

    for matricula in matriculas:
        if matricula.esta_aprobada():
            aprobadas += 1

    print(f"Matrículas aprobadas: {aprobadas}")


def main():
    while True:
        imprimir_titulo("SISTEMA ACADÉMICO")
        print("1. Estudiantes")
        print("2. Materias")
        print("3. Matrículas")
        print("4. Resumen")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_estudiantes()

        elif opcion == "2":
            menu_materias()

        elif opcion == "3":
            menu_matriculas()

        elif opcion == "4":
            mostrar_resumen()
            pausa()

        elif opcion == "0":
            imprimir_exito("Hasta pronto.")
            break

        else:
            imprimir_error("Opción incorrecta.")
            pausa()


if __name__ == "__main__":
    main()