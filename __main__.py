from union import *
from estacionamiento import Estacionamiento
from vehiculo import Vehiculo

path_estacionamientos = "estacionamientos.json"  # Ruta del archivo JSON para los datos de los estacionamientos.
ESTACIONAMIENTOS = estacionamiento_leer(path_estacionamientos)  # Carga los datos de los estacionamientos desde el archivo JSON.

def mostrar_menu() -> None:
    while True:
        print("[1] Nuevo estacionamiento")
        print("[2] Ingreso de vehículo")
        print("[3] Egreso de vehículo")
        print("[4] Modificar costes por hora de vehiculos")
        print("[5] Listar vehículos estacionados (map)")
        print("[6] Listar vehículos ordenados por patente (descendente)")
        print("[7] Recaudación total de todos los estacionamientos (reduce)")
        print("[8] Listar vehiculos filtrados por cantidad de minutos estacionados que superen los 60 min (filter)")
        print("[9] Guardar archivo 'db_estacionamientos.csv'")
        print("[10] Ver log de ingresos y egresos")
        print("[0] Salir")

        match opcion:
            case "1":
                punto_1()
            case "2":
                punto_2()
            case "3":
                punto_3()
            case "4":
                punto_4()
            case "5":
                punto_5()
            case "6":
                punto_6()
            case "7":
                punto_7()
            case "8":
                punto_8()
            case "9":
                punto_9()
            case "10":
                punto_10()
            case "0":
                print("SALIENDO...")
                return
            case _:
                print("Opción inválida. Por favor, seleccione una opción válida.")


#mostrar_menu()
#preguntar al profe 
def main() -> None:
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "0":
            break
        ejecutar_opcion(opcion)

if __name__ == "__main__":
    main()