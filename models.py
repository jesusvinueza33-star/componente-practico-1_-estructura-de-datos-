class ModeloBase:
    def __init__(self, id_registro):
        self.id = int(id_registro)

    def a_diccionario(self):
        return {"id": self.id}

    @classmethod
    def desde_diccionario(cls, datos):
        datos = datos.copy()
        id_registro = datos.pop("id")

        if cls.__name__ == "Matricula" and "nota" in datos:
            datos["notas"] = datos.pop("nota")

        return cls(id_registro, **datos)

    def etiqueta(self):
        return f"ID: {self.id}"


class Persona(ModeloBase):
    def __init__(self, id_registro, nombre, apellido, email):
        super().__init__(id_registro)
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["apellido"] = self.apellido
        datos["email"] = self.email
        return datos

    def etiqueta(self):
        return f"{self.nombre} {self.apellido}"


class Estudiante(Persona):
    def __init__(self, id_registro, nombre, apellido, email, carnet="", carrera=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.carnet = carnet
        self.carrera = carrera

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["carnet"] = self.carnet
        datos["carrera"] = self.carrera
        return datos

    def etiqueta(self):
        return (f"{super().etiqueta()} · "
                f"{self.carnet} · {self.carrera}")


class Materia(ModeloBase):
    CUPOS_MAXIMOS = 30
    NOTA_APROBACION = 14

    def __init__(self, id_registro, nombre, codigo, creditos=0, cupos=0):
        super().__init__(id_registro)
        self.nombre = nombre
        self.codigo = codigo
        self.creditos = int(creditos)
        self.cupos = int(cupos)

    @staticmethod
    def es_nota_valida(valor):
        try:
            nota = float(valor)
            return 0 <= nota <= 20
        except (ValueError, TypeError):
            return False

    def hay_cupo(self):
        return self.cupos > 0

    def ocupar_cupo(self):
        if self.hay_cupo():
            self.cupos = self.cupos - 1
            return True
        return False

    def liberar_cupo(self):
        if self.cupos < self.CUPOS_MAXIMOS:
            self.cupos = self.cupos + 1
            return True
        return False

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["codigo"] = self.codigo
        datos["creditos"] = self.creditos
        datos["cupos"] = self.cupos
        return datos

    def etiqueta(self):
        return (f"{self.nombre} · {self.codigo} · "
                f"{self.creditos} créditos · "
                f"{self.cupos} cupos")


class Matricula(ModeloBase):
    def __init__(self, id_registro, estudiante_id, materia_id, periodo, notas=0, fecha=""):
        super().__init__(id_registro)
        self.estudiante_id = int(estudiante_id)
        self.materia_id = int(materia_id)
        self.periodo = periodo
        self.notas = float(notas) if notas is not None else 0
        self.fecha = fecha

    def esta_aprobada(self):
        return self.notas >= Materia.NOTA_APROBACION

    def estado(self):
        if self.esta_aprobada():
            return "Aprobado"
        return "Reprobado"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["estudiante_id"] = self.estudiante_id
        datos["materia_id"] = self.materia_id
        datos["periodo"] = self.periodo
        datos["notas"] = self.notas
        datos["fecha"] = self.fecha
        return datos

    def etiqueta(self):
        return (f"Matricula #{self.id} · "
                f"{self.periodo} · Nota: {self.notas} · "
                f"{self.estado()}")
