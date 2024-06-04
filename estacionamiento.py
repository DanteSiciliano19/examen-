import json
from datetime import datetime
from vehiculo import Vehiculo

class Estacionamiento:
    def __init__(self, nombre: str, cant_parcelas_autos: int, cant_parcelas_motos: int, coste_hora_auto: float, coste_hora_moto: float) -> None:
        self.nombre = nombre
        self.cant_parcelas_autos = cant_parcelas_autos
        self.cant_parcelas_motos = cant_parcelas_motos
        self.coste_hora_auto = coste_hora_auto
        self.coste_hora_moto = coste_hora_moto
        self.autos = []
        self.motos = []
        self.recaudacion = 0.0

    def __str__(self) -> str:
        return f"Estacionamiento {self.nombre} [Motos: {len(self.motos)}/{self.cant_parcelas_motos}] [Autos: {len(self.autos)}/{self.cant_parcelas_autos}] [Recaudación: ${self.recaudacion:.2f}]"

    def __len__(self) -> int:
        return round(self.recaudacion, 2)  # Devuelve la recaudación con formato float, con dos decimales.

    def ingresar_vehiculo(self, vehiculo: Vehiculo) -> None:
        if vehiculo.tipo == 'auto' and len(self.autos) < self.cant_parcelas_autos:
            self.autos.append(vehiculo)  # Agrega el auto a la lista de autos.
            vehiculo.tiempo_ingreso = datetime.now()  # Registra el tiempo de ingreso del vehículo.
        elif vehiculo.tipo == 'moto' and len(self.motos) < self.cant_parcelas_motos:
            self.motos.append(vehiculo)  # Agrega la moto a la lista de motos.
            vehiculo.tiempo_ingreso = datetime.now()  # Registra el tiempo de ingreso del vehículo.
        else:
            print("No hay espacio disponible para este tipo de vehículo.")  # Imprime un mensaje si no hay espacio.

    def egresar_vehiculo(self, patente: str) -> None:
        vehiculo = next((v for v in self.autos + self.motos if v.patente == patente), None)  # Busca el vehículo por patente.
        if vehiculo:
            if vehiculo.tipo == 'auto':
                self.autos.remove(vehiculo)  # Elimina el auto de la lista de autos.
            else:
                self.motos.remove(vehiculo)  # Elimina la moto de la lista de motos.
            tiempo_estacionado = (datetime.now() - vehiculo.tiempo_ingreso).total_seconds() / 3600  # Calcula el tiempo estacionado en horas.
            coste = tiempo_estacionado * (self.coste_hora_auto if vehiculo.tipo == 'auto' else self.coste_hora_moto)  # Calcula el coste del estacionamiento.
            return f"Vehículo {vehiculo.patente} egresado. Costo: ${costo:.2f}"
        else:
            return f"Vehículo con patente {patente} no encontrado en el estacionamiento."

    def modificar_costos(self, nuevo_costo_auto: float, nuevo_costo_moto: float) -> None:
        self.coste_hora_auto = nuevo_costo_auto  # Asigna el nuevo coste por hora para autos.
        self.coste_hora_moto = nuevo_costo_moto  # Asigna el nuevo coste por hora para motos.

    def listar_vehiculos_estacionados_map(self) -> list:
        return list(map(str, self.autos + self.motos))  # Retorna una lista de los vehículos estacionados convertidos a cadenas.

    def listar_vehiculos_ordenados_patente_desc(self) -> list:
        return sorted(self.autos + self.motos, key=lambda x: x.patente, reverse=True)  # Retorna una lista de vehículos ordenados por patente en orden descendente.

    def listar_vehiculos_filtrados_60_min(self) -> list:
        return list(filter(lambda v: (datetime.now() - v.tiempo_ingreso).total_seconds() / 60 > 60, self.autos + self.motos))  # Retorna una lista de vehículos que han estado estacionados por más de 60 minutos