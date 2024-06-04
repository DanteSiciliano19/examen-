from datetime import datetime

class Vehiculo:
    def __init__(self, tipo: str, patente: str):
        self.tipo = tipo  # Asigna el tipo del vehículo (auto o moto).
        self.patente = patente  # Asigna la patente del vehículo.
        self.tiempo_ingreso = datatime.now()  # Inicializa el tiempo de ingreso del vehículo 

    def __str__(self):
        return f"{self.tipo} - {self.patente}"  # Retorna una representación en cadena del vehículo.

    def __len__(self) -> int:
        ahora = datetime.now()
        delta = ahora - self.hora_ingreso
        return int(delta.total_seconds() // 60)  # Retorna la diferencia en minutos

    def registro_ingreso(self) -> str:
            return f"[Patente: {self.patente}] [Hora ingreso: {self.hora_ingreso.strftime('%d-%m-%Y %H:%M')}]"