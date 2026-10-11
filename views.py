from models import Estudiante, Materia, Matricula
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido


gestor_estudiantes = GestorJSON("data/estudiantes.json")
gestor_materias = GestorJSON("data/materias.json")
gestor_matriculas = GestorJSON("data/matriculas.json")


# FUNCIONES GENERALES

def leer_objetos(gestor, clase):
    datos = gestor.leer()
    objetos = []

    for dato in datos:
        objetos.append(clase.desde_diccionario(dato))

    return objetos


def siguiente_id(gestor):
    # El conjunto permite comprobar los ID registrados.
    ids = {dato["id"] for dato in gestor.leer()}

    if len(ids) == 0:
        return 1

    return max(ids) + 1


def guardar_nuevo(gestor, objeto):
    datos = gestor.leer()
    datos.append(objeto.a_diccionario())
    gestor.guardar(datos)


def reemplazar(gestor, objeto):
    datos = gestor.leer()

    for i in range(len(datos)):
        if datos[i]["id"] == objeto.id:
            datos[i] = objeto.a_diccionario()
            gestor.guardar(datos)
            return True

    return False


def eliminar(gestor, id_registro):
    datos = gestor.leer()
    nuevos = []

    for dato in datos:
        if dato["id"] != id_registro:
            nuevos.append(dato)

    if len(datos) == len(nuevos):
        return False

    gestor.guardar(nuevos)
    return True


def obtener_por_id(gestor, clase, id_registro):
    objetos = leer_objetos(gestor, clase)

    for objeto in objetos:
        if objeto.id == int(id_registro):
            return objeto

    return None


def buscar(gestor, clase, termino, campos):
    # La tupla indica los campos en los que se puede buscar.
    objetos = leer_objetos(gestor, clase)
    resultados = []

    for objeto in objetos:
        datos = objeto.a_diccionario()

        for campo in campos:
            if termino.lower() in str(datos[campo]).lower():
                resultados.append(objeto)
                break

    return resultados


# ESTUDIANTES

def carnets_registrados(excepto_id=None):
    # El conjunto evita repetir carnets.
    carnets = set()

    for dato in gestor_estudiantes.leer():
        if dato["id"] != excepto_id:
            carnets.add(dato["carnet"].upper())

    return carnets


def validar_estudiante(datos, id_actual=None):
    campos = ("nombre", "apellido", "email", "carnet")

    for campo in campos:
        if campo not in datos or str(datos[campo]).strip() == "":
            return f"El campo {campo} es obligatorio."

    if not es_email_valido(datos["email"]):
        return "El email no es válido."

    for estudiante in leer_objetos(gestor_estudiantes, Estudiante):
        if estudiante.id != id_actual:
            if estudiante.email.lower() == datos["email"].lower():
                return "Ese email ya está registrado."

    carnet = datos["carnet"].strip().upper()

    if carnet in carnets_registrados(id_actual):
        return "Ese carnet ya está registrado."

    return None


def crear_estudiante(datos):
    datos["nombre"] = datos["nombre"].strip()
    datos["apellido"] = datos["apellido"].strip()
    datos["email"] = datos["email"].strip()
    datos["carnet"] = datos["carnet"].strip().upper()
    datos["carrera"] = datos.get("carrera", "").strip()

    error = validar_estudiante(datos)

    if error:
        return False, error

    estudiante = Estudiante(
        siguiente_id(gestor_estudiantes),
        datos["nombre"],
        datos["apellido"],
        datos["email"],
        datos["carnet"],
        datos["carrera"]
    )

    guardar_nuevo(gestor_estudiantes, estudiante)
    return True, "Estudiante registrado correctamente."


def obtener_estudiantes():
    return leer_objetos(gestor_estudiantes, Estudiante)


def obtener_estudiante(id_registro):
    return obtener_por_id(
        gestor_estudiantes, Estudiante, id_registro
    )


def buscar_estudiantes(termino):
    campos = ("nombre", "apellido", "email", "carnet", "carrera")
    return buscar(gestor_estudiantes, Estudiante, termino, campos)


def actualizar_estudiante(id_registro, cambios):
    estudiante = obtener_estudiante(id_registro)

    if estudiante is None:
        return False, "Estudiante no encontrado."

    datos = estudiante.a_diccionario()
    datos.update(cambios)

    datos["nombre"] = datos["nombre"].strip()
    datos["apellido"] = datos["apellido"].strip()
    datos["email"] = datos["email"].strip()
    datos["carnet"] = datos["carnet"].strip().upper()
    datos["carrera"] = datos["carrera"].strip()

    error = validar_estudiante(datos, estudiante.id)

    if error:
        return False, error

    nuevo = Estudiante.desde_diccionario(datos)
    reemplazar(gestor_estudiantes, nuevo)

    return True, "Estudiante actualizado correctamente."


def eliminar_estudiante(id_registro):
    # No se elimina si tiene matrículas registradas.
    for matricula in obtener_matriculas():
        if matricula.estudiante_id == int(id_registro):
            return False, "El estudiante tiene matrículas registradas."

    if eliminar(gestor_estudiantes, int(id_registro)):
        return True, "Estudiante eliminado correctamente."

    return False, "Estudiante no encontrado."


# MATERIAS

def codigos_registrados(excepto_id=None):
    # El conjunto evita repetir códigos.
    codigos = set()

    for dato in gestor_materias.leer():
        if dato["id"] != excepto_id:
            codigos.add(dato["codigo"].upper())

    return codigos


def crear_materia(datos):
    nombre = datos["nombre"].strip()
    codigo = datos["codigo"].strip().upper()

    try:
        creditos = int(datos["creditos"])
        cupos = int(datos["cupos"])
    except (ValueError, TypeError):
        return False, "Créditos y cupos deben ser números enteros."

    if nombre == "" or codigo == "":
        return False, "El nombre y el código son obligatorios."

    if codigo in codigos_registrados():
        return False, "Ese código ya está registrado."

    if creditos < 1 or creditos > 10:
        return False, "Los créditos deben estar entre 1 y 10."

    if cupos < 0 or cupos > Materia.CUPOS_MAXIMOS:
        return False, "Los cupos deben estar entre 0 y 30."

    materia = Materia(
        siguiente_id(gestor_materias),
        nombre, codigo, creditos, cupos
    )

    guardar_nuevo(gestor_materias, materia)
    return True, "Materia registrada correctamente."


def obtener_materias():
    return leer_objetos(gestor_materias, Materia)


def obtener_materia(id_registro):
    return obtener_por_id(gestor_materias, Materia, id_registro)


def buscar_materias(termino):
    campos = ("nombre", "codigo")
    return buscar(gestor_materias, Materia, termino, campos)


def actualizar_materia(id_registro, cambios):
    materia = obtener_materia(id_registro)

    if materia is None:
        return False, "Materia no encontrada."

    datos = materia.a_diccionario()
    datos.update(cambios)

    nombre = datos["nombre"].strip()
    codigo = datos["codigo"].strip().upper()

    try:
        creditos = int(datos["creditos"])
        cupos = int(datos["cupos"])
    except (ValueError, TypeError):
        return False, "Créditos y cupos deben ser números enteros."

    if nombre == "" or codigo == "":
        return False, "El nombre y el código son obligatorios."

    if codigo in codigos_registrados(materia.id):
        return False, "Ese código ya está registrado."

    if creditos < 1 or creditos > 10:
        return False, "Los créditos deben estar entre 1 y 10."

    if cupos < 0 or cupos > Materia.CUPOS_MAXIMOS:
        return False, "Los cupos deben estar entre 0 y 30."

    # No se permiten cupos inferiores a los ya ocupados.
    ocupados = Materia.CUPOS_MAXIMOS - materia.cupos
    if cupos < ocupados:
        return False, "Los nuevos cupos no cubren las matrículas existentes."

    nuevo = Materia(
        materia.id, nombre, codigo, creditos, cupos
    )

    reemplazar(gestor_materias, nuevo)
    return True, "Materia actualizada correctamente."


def eliminar_materia(id_registro):
    for matricula in obtener_matriculas():
        if matricula.materia_id == int(id_registro):
            return False, "La materia tiene matrículas registradas."

    if eliminar(gestor_materias, int(id_registro)):
        return True, "Materia eliminada correctamente."

    return False, "Materia no encontrada."


def materias_sin_cupo():
    resultado = []

    for materia in obtener_materias():
        if not materia.hay_cupo():
            resultado.append(materia)

    return resultado


# MATRÍCULAS

def obtener_matriculas():
    return leer_objetos(gestor_matriculas, Matricula)


def obtener_matricula(id_registro):
    return obtener_por_id(gestor_matriculas, Matricula, id_registro)


def crear_matricula(datos):
    try:
        estudiante_id = int(datos["estudiante_id"])
        materia_id = int(datos["materia_id"])
    except (ValueError, TypeError, KeyError):
        return False, "Los ID del estudiante y la materia son obligatorios."

    estudiante = obtener_estudiante(estudiante_id)
    materia = obtener_materia(materia_id)

    if estudiante is None:
        return False, "El estudiante no existe."

    if materia is None:
        return False, "La materia no existe."

    if not materia.hay_cupo():
        return False, "La materia no tiene cupos disponibles."

    periodo = datos["periodo"].strip()

    if periodo == "":
        return False, "El período es obligatorio."

    for matricula in obtener_matriculas():
        if (matricula.estudiante_id == estudiante_id
                and matricula.materia_id == materia_id
                and matricula.periodo == periodo):
            return False, "El estudiante ya está matriculado en ese período."

    matricula = Matricula(
        siguiente_id(gestor_matriculas),
        estudiante_id,
        materia_id,
        periodo,
        0,
        datos["fecha"]
    )

    guardar_nuevo(gestor_matriculas, matricula)

    materia.ocupar_cupo()
    reemplazar(gestor_materias, materia)

    return True, "Matrícula registrada correctamente."


def registrar_nota(id_registro, nota):
    matricula = obtener_matricula(id_registro)

    if matricula is None:
        return False, "Matrícula no encontrada."

    if not Materia.es_nota_valida(nota):
        return False, "La nota debe estar entre 0 y 20."

    matricula.notas = float(nota)
    reemplazar(gestor_matriculas, matricula)

    return True, "Nota registrada correctamente."

def retirar_matricula(id_registro):
    matricula = obtener_matricula(id_registro)

    if matricula is None:
        return False, "Matrícula no encontrada."

    materia = obtener_materia(matricula.materia_id)

    if materia is not None:
        materia.liberar_cupo()
        reemplazar(gestor_materias, materia)

    eliminar(gestor_matriculas, int(id_registro))

    return True, "Matrícula retirada correctamente."


def certificado(id_registro):
    matricula = obtener_matricula(id_registro)

    if matricula is None:
        return None

    # Los diccionarios índice permiten encontrar datos por ID.
    estudiantes = {
        e.id: e for e in obtener_estudiantes()
    }

    materias = {
        m.id: m for m in obtener_materias()
    }

    estudiante = estudiantes.get(matricula.estudiante_id)
    materia = materias.get(matricula.materia_id)

    if estudiante is None or materia is None:
        return None

    return {
        "matricula": matricula,
        "estudiante": estudiante,
        "materia": materia
    }


def matriculas_por_estudiante():
    # El diccionario de listas agrupa las matrículas por estudiante.
    agrupadas = {}

    for matricula in obtener_matriculas():
        agrupadas.setdefault(
            matricula.estudiante_id, []
        ).append(matricula)

    return agrupadas


def promedio_de_estudiante(id_registro):
    notas = []

    for matricula in obtener_matriculas():
        if matricula.estudiante_id == int(id_registro):
            notas.append(matricula.notas)  

    if len(notas) == 0:
        return None
    resultado = sum(notas) / len(notas)
    return resultado