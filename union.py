import json
from estacionamiento import Estacionamiento
from vehiculo import Vehiculo

def estacionamiento_leer(path) -> list[Estacionamiento]:
    with open(path, 'r') as file:
        data = json.load(file)
        estacionamientos = []
        for estacionamiento_data in data:
            estacionamiento = Estacionamiento(estacionamiento_data['nombre'],
                                              estacionamiento_data['cant_parcelas_autos'],
                                              estacionamiento_data['cant_parcelas_motos'],
                                              estacionamiento_data['coste_hora_auto'],
                                              estacionamiento_data['coste_hora_moto'])
            estacionamiento.autos = [Vehiculo(auto['tipo'], auto['patente']) for auto in estacionamiento_data['autos']]
            estacionamiento.motos = [Vehiculo(moto['tipo'], moto['patente']) for moto in estacionamiento_data['motos']]
            estacionamiento.recaudacion = estacionamiento_data['recaudacion']
            estacionamientos.append(estacionamiento)
        return estacionamientos

def estacionamiento_guardar(path, estacionamientos) -> None:
    data = []
    for estacionamiento in estacionamientos:
        data.append({
            'nombre': estacionamiento.nombre,
            'cant_parcelas_autos': estacionamiento.cant_parcelas_autos,
            'cant_parcelas_motos': estacionamiento.cant_parcelas_motos,
            'coste_hora_auto': estacionamiento.coste_hora_auto,
            'coste_hora_moto': estacionamiento.coste_hora_moto,
            'autos': [{'tipo': auto.tipo, 'patente': auto.patente} for auto in estacionamiento.autos],
            'motos': [{'tipo': moto.tipo, 'patente': moto.patente} for moto in estacionamiento.motos],
            'recaudacion': estacionamiento.recaudacion
        })
    with open(path, 'w') as file:
        json.dump(data, file)

def alta_vehiculo() -> Vehiculo:
    tipo = input(" tipo de vehículo (auto/moto): ")
    patente = input("Ingrese patente del vehículo: ")
    return Vehiculo(tipo, patente)

def alta_estacionamiento() -> Estacionamiento:
    nombre = input("Ingrese nombre del nuevo estacionamiento: ")
    cant_parcelas_autos = int(input("Ingrese cantidad de parcelas para autos: "))
    cant_parcelas_motos = int(input("Ingrese cantidad de parcelas para motos: "))
    coste_hora_auto = float(input("Ingrese costo por hora para autos: "))
    coste_hora_moto = float(input("Ingrese costo por hora para motos: "))
    return Estacionamiento(nombre, cant_parcelas_autos, cant_parcelas_motos, coste_hora_auto, coste_hora_moto)

def grabar_log(path: str, msj: str):
    with open(path, 'a') as file:  # Abre el archivo de log en modo de añadir.
        file.write(f"{msj}\n")  # Escribe el mensaje en el archivo de log.

def punto_1() -> bool:
    estacionamiento = alta_estacionamiento()  # Crea un nuevo estacionamiento.
    # Verifica si el estacionamiento ya existe.
    if any(est.nombre == estacionamiento.nombre for est in ESTACIONAMIENTOS):
        print("El estacionamiento ya existe.")  # Imprime un mensaje si el estacionamiento ya existe.
        return False  # Retorna False indicando que no se pudo crear el estacionamiento.
    else:
        ESTACIONAMIENTOS.append(estacionamiento)  # Agrega el nuevo estacionamiento a la lista.
        estacionamiento_guardar(path_estacionamientos, ESTACIONAMIENTOS)  # Guarda los datos de los estacionamientos.
        return True  # Retorna True indicando que se creó el estacionamiento correctamente.


# Punto 2: Ingreso de vehículo.
def punto_2() -> bool:
    print("Seleccione estacionamiento:")  # Imprime un mensaje solicitando la selección de un estacionamiento.
    for i, estacionamiento in enumerate(ESTACIONAMIENTOS):  # Itera sobre los estacionamientos para mostrarlos.
        print(f"{i + 1}. {estacionamiento.nombre}")  # Imprime el número y el nombre del estacionamiento.
    seleccion = int(input("Ingrese el número de estacionamiento: ")) - 1  # Solicita la selección del estacionamiento.
    if 0 <= seleccion < len(ESTACIONAMIENTOS):  # Verifica que la selección sea válida.
        vehiculo = alta_vehiculo()  # Crea un nuevo vehículo.
        ESTACIONAMIENTOS[seleccion].ingresar_vehiculo(vehiculo)  # Ingresa el vehículo en el estacionamiento seleccionado.
        grabar_log("log.txt", vehiculo.registro_ingreso())  # Graba el registro de ingreso en el log.
        estacionamiento_guardar(path_estacionamientos, ESTACIONAMIENTOS)  # Guarda los datos de los estacionamientos.
        return True  # Retorna True indicando que el vehículo se ingresó correctamente.
    else:
        print("Selección inválida.")  # Imprime un mensaje indicando que la selección es inválida.
        return False  # Retorna False indicando que no se pudo ingresar el vehículo.

# Punto 3: Egreso de vehículo.
def punto_3() -> bool:
    print("Seleccione estacionamiento:")  # Imprime un mensaje solicitando la selección de un estacionamiento.
    for i, estacionamiento in enumerate(ESTACIONAMIENTOS):  # Itera sobre los estacionamientos para mostrarlos.
        print(f"{i + 1}. {estacionamiento.nombre}")  # Imprime el número y el nombre del estacionamiento.
    seleccion = int(input("Ingrese el número de estacionamiento: ")) - 1  # Solicita la selección del estacionamiento.
    if 0 <= seleccion < len(ESTACIONAMIENTOS):  # Verifica que la selección sea válida.
        ESTACIONAMIENTOS[seleccion].listar_vehiculos_estacionados()  # Lista los vehículos estacionados en el estacionamiento seleccionado.
        patente = input("Ingrese la patente del vehículo a egresar: ")  # Solicita la patente del vehículo a egresar.
        ESTACIONAMIENTOS[seleccion].egresar_vehiculo(patente)  # Egresar el vehículo del estacionamiento seleccionado.
        grabar_log("log.txt", ESTACIONAMIENTOS[seleccion].registro_egreso(patente))  # Graba el registro de egreso en el log.
        estacionamiento_guardar(path_estacionamientos, ESTACIONAMIENTOS)  # Guarda los datos de los estacionamientos.
        return True  # Retorna True indicando que el vehículo se egresó correctamente.
    else:
        print("Selección inválida.")  # Imprime un mensaje indicando que la selección es inválida.
        return False  # Retorna False indicando que no se pudo egresar el vehículo.

# Punto 4: Modificar costes por hora de vehículos.
def punto_4() -> bool:
    print("Modificar costes por hora de vehículos:")  # Imprime un mensaje solicitando la modificación de costes.
    print("Seleccione estacionamiento:")  # Solicita la selección de un estacionamiento.
    for i, estacionamiento in enumerate(ESTACIONAMIENTOS):  # Itera sobre los estacionamientos para mostrarlos.
        print(f"{i + 1}. {estacionamiento.nombre}")  # Imprime el número y el nombre del estacionamiento.
    seleccion = int(input("Ingrese el número de estacionamiento: ")) - 1
    if 0 <= seleccion < len(ESTACIONAMIENTOS):  # Verifica que la selección sea válida.
        nuevo_costo_auto = float(input("Ingrese el nuevo costo por hora para autos: "))  # Solicita el nuevo coste por hora para autos.
        nuevo_costo_moto = float(input("Ingrese el nuevo costo por hora para motos: "))  # Solicita el nuevo coste por hora para motos.
        ESTACIONAMIENTOS[seleccion].modificar_costos(nuevo_costo_auto, nuevo_costo_moto)  # Modifica los costes en el estacionamiento seleccionado.
        estacionamiento_guardar(path_estacionamientos, ESTACIONAMIENTOS)  # Guarda los datos de los estacionamientos.
        return True  # Retorna True indicando que los costes se modificaron correctamente.
    else:
        print("Selección inválida.")  # Imprime un mensaje indicando que la selección es inválida.
        return False  # Retorna False indicando que no se pudieron modificar los costes.

def punto_5() -> bool:
    print("Listar vehículos estacionados:")  # Imprime un mensaje solicitando listar los vehículos estacionados.
    print("Seleccione estacionamiento:")  # Solicita la selección de un estacionamiento.
    for i, estacionamiento in enumerate(ESTACIONAMIENTOS):  # Itera sobre los estacionamientos para mostrarlos.
        print(f"{i + 1}. {estacionamiento.nombre}")  # Imprime el número y el nombre del estacionamiento.
    seleccion = int(input("Ingrese el número de estacionamiento: ")) - 1  # Solicita la selección del estacionamiento.
    if 0 <= seleccion < len(ESTACIONAMIENTOS):  # Verifica que la selección sea válida.
        vehiculos = ESTACIONAMIENTOS[seleccion].listar_vehiculos_estacionados_map()  # Obtiene la lista de vehículos estacionados.
        for vehiculo in vehiculos:  # Itera sobre la lista de vehículos.
            print(vehiculo)  # Imprime la representación del vehículo.
        return True  # Retorna True indicando que los vehículos se listaron correctamente.
    else:
        print("Selección inválida.")  # Imprime un mensaje indicando que la selección es inválida.
        return False  # Retorna False indicando que no se pudieron listar los vehículos.

def punto_6() -> bool:
    print("Listar vehículos ordenados por patente (descendente):")  # Imprime un mensaje solicitando listar los vehículos por patente.
    print("Seleccione estacionamiento:")  # Solicita la selección de un estacionamiento.
    for i, estacionamiento in enumerate(ESTACIONAMIENTOS):  # Itera sobre los estacionamientos para mostrarlos.
        print(f"{i + 1}. {estacionamiento.nombre}")  # Imprime el número y el nombre del estacionamiento.
    seleccion = int(input("Ingrese el número de estacionamiento: ")) - 1  # Solicita la selección del estacionamiento.
    if 0 <= seleccion < len(ESTACIONAMIENTOS):  # Verifica que la selección sea válida.
        vehiculos_ordenados = ESTACIONAMIENTOS[seleccion].listar_vehiculos_ordenados_patente_desc()  # Obtiene la lista de vehículos ordenados por patente.
        for vehiculo in vehiculos_ordenados:  # Itera sobre la lista de vehículos.
            print(vehiculo)  # Imprime la representación del vehículo.
        return True  # Retorna True indicando que los vehículos se listaron correctamente.
    else:
        print("Selección inválida.")  # Imprime un mensaje indicando que la selección es inválida.
        return False  # Retorna False indicando que no se pudieron listar los vehículos.

# Punto 7: Recaudación total de todos los estacionamientos (reduce).
def punto_7() -> None:
    # Calcula la recaudación total sumando la recaudación de todos los estacionamientos.
    recaudacion_total = sum(estacionamiento.recaudacion for estacionamiento in ESTACIONAMIENTOS)
    print(f"Recaudación total de todos los estacionamientos: ${recaudacion_total:.2f}")  # Imprime la recaudación total.

# Punto 8: Listar vehículos filtrados por cantidad de minutos estacionados que superen los 60 min (filter).
def punto_8() -> bool:
    print("Listar vehículos filtrados por tiempo estacionado > 60 min:")  # Imprime un mensaje solicitando listar los vehículos por tiempo estacionado.
    print("Seleccione estacionamiento:")  # Solicita la selección de un estacionamiento.
    for i, estacionamiento in enumerate(ESTACIONAMIENTOS):  # Itera sobre los estacionamientos para mostrarlos.
        print(f"{i + 1}. {estacionamiento.nombre}")  # Imprime el número y el nombre del estacionamiento.
    seleccion = int(input("Ingrese el número de estacionamiento: ")) - 1  # Solicita la selección del estacionamiento.
    if 0 <= seleccion < len(ESTACIONAMIENTOS):  # Verifica que la selección sea válida.
        vehiculos_filtrados = ESTACIONAMIENTOS[seleccion].listar_vehiculos_filtrados_60_min()  # Obtiene la lista de vehículos filtrados.
        for vehiculo in vehiculos_filtrados:  # Itera sobre la lista de vehículos.
            print(vehiculo)  # Imprime la representación del vehículo.
        return True  # Retorna True indicando que los vehículos se listaron correctamente.
    else:
        print("Selección inválida.")  # Imprime un mensaje indicando que la selección es inválida.
        return False  # Retorna False indicando que no se pudieron listar los vehículos.

def punto_9() -> bool:
    print("Guardar archivo 'db_estacionamientos.json'")
    estacionamiento_guardar(path_estacionamientos, ESTACIONAMIENTOS)
    print("Archivo guardado exitosamente.")
    return True

def punto_10() -> bool:
    print("Ver log de ingresos y egresos:")
    try:
        with open("registros.txt", "r") as file:
            log_content = file.read()
            print(log_content)
    except FileNotFoundError:
        print("El archivo de log 'registros.txt' no existe o no se encontró.")
    return True