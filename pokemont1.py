import random

class Entrenador:
    def __init__(self, nombre: str):
        self.nombre = nombre

class Pokemon:
    def __init__(self, nombre: str):
        self.nombre = nombre
        # estadísticas aleatorias según enunciado
        self.max_ataque = random.randint(20, 100)
        self.vida_max = random.randint(150, 400)
        self.vida_actual = self.vida_max

    def recuperar(self):
        self.vida_actual = self.vida_max

entrenador1 = None
pokemon1 = None
entrenador2 = None
pokemon2 = None

victorias = 0
derrotas = 0

def crearEntrenadorPokemon(tipo: int):
    """
    tipo = 1 => crea al entrenador y pokemon del jugador
    tipo = 2 => crea al entrenador y pokemon rival
    """
    global entrenador1, pokemon1, entrenador2, pokemon2
    if tipo == 1:
        nombre_ent = input("Ingrese su nombre de entrenador: ").strip()
        nombre_pok = input("Ingrese el nombre de su Pokémon: ").strip()
        entrenador1 = Entrenador(nombre_ent)
        pokemon1 = Pokemon(nombre_pok)
        print(f"\nEntrenador creado: {entrenador1.nombre}")
        print(f"Tu Pokémon: {pokemon1.nombre} | Ataque máximo: {pokemon1.max_ataque} | Vida máxima: {pokemon1.vida_max}\n")
    elif tipo == 2:
        nombre_ent = input("Ingrese el nombre del entrenador rival: ").strip()
        nombre_pok = input("Ingrese el nombre del Pokémon rival: ").strip()
        entrenador2 = Entrenador(nombre_ent)
        pokemon2 = Pokemon(nombre_pok)
        print(f"\nRival creado: {entrenador2.nombre}")
        print(f"Pokémon rival: {pokemon2.nombre} | Ataque máximo: {pokemon2.max_ataque} | Vida máxima: {pokemon2.vida_max}\n")
    else:
        print("Tipo inválido para crear entrenador/pokemon (debe ser 1 o 2).")

def valorDeAtaque(tipo: int) -> int:
    if tipo == 1:
        if pokemon1 is None:
            return 0
        return random.randint(0, pokemon1.max_ataque)
    elif tipo == 2:
        if pokemon2 is None:
            return 0
        return random.randint(0, pokemon2.max_ataque)
    else:
        return 0

def defender(receptor: int, valor_ataque: int) -> int:
    """
    receptor = 1 o 2 indica cuál pokemon recibe el ataque.
    Tira un dado (1-6). Si sale 6, el ataque se reduce a 0.
    Resta la vida correspondiente y devuelve la nueva vida actual del receptor.
    """
    global pokemon1, pokemon2
    tirada = random.randint(1, 6)
    if tirada == 6:
        valor_ataque = 0
        print("¡Tirada de dado = 6! El ataque queda anulado (0 daño).")
    if receptor == 1:
        pokemon1.vida_actual -= valor_ataque
        if pokemon1.vida_actual < 0:
            pokemon1.vida_actual = 0
        return pokemon1.vida_actual
    elif receptor == 2:
        pokemon2.vida_actual -= valor_ataque
        if pokemon2.vida_actual < 0:
            pokemon2.vida_actual = 0
        return pokemon2.vida_actual
    else:
        return 0

def recuperar():
    if pokemon1 is None:
        print("Aún no tienes un Pokémon. Primero crea tu entrenador y pokemon.")
        return
    pokemon1.recuperar()
    print(f"{pokemon1.nombre} ha recuperado a {pokemon1.vida_actual}/{pokemon1.vida_max} de vida.")

# Programa principal / menú
def main():
    global victorias, derrotas, pokemon2
    print("=== Simulación de pelea Pokémon (examen T1) ===\n")
    # Crear el entrenador y pokemon del jugador al inicio
    crearEntrenadorPokemon(1)

    while True:
        opcion = input("Seleccione: Pelear (P) o Finalizar (F): ").strip().upper()
        if opcion == 'P':
            # recuperar vida del jugador antes de la pelea
            recuperar()
            # crear rival en este momento
            crearEntrenadorPokemon(2)
            if pokemon2 is None:
                print("No se pudo crear el Pokémon rival. Volviendo al menú.")
                continue

            print("¡Comienza la pelea! Tú comienzas siempre.\n")
            turno = 1  # 1 -> jugador ataca; 2 -> rival ataca

            while pokemon1.vida_actual > 0 and pokemon2.vida_actual > 0:
                if turno == 1:
                    ataque = valorDeAtaque(1)
                    print(f"{entrenador1.nombre} con {pokemon1.nombre} ataca con {ataque} puntos de ataque.")
                    vida_restante = defender(2, ataque)
                    print(f"Resumen: {entrenador2.nombre} - {pokemon2.nombre} => {vida_restante}/{pokemon2.vida_max} vida restante.\n")
                    turno = 2
                else:
                    ataque = valorDeAtaque(2)
                    print(f"{entrenador2.nombre} con {pokemon2.nombre} ataca con {ataque} puntos de ataque.")
                    vida_restante = defender(1, ataque)
                    print(f"Resumen: {entrenador1.nombre} - {pokemon1.nombre} => {vida_restante}/{pokemon1.vida_max} vida restante.\n")
                    turno = 1

            if pokemon1.vida_actual <= 0:
                print(f"¡Ha ganado {entrenador2.nombre} con {pokemon2.nombre}!\n")
                derrotas += 1
            else:
                print(f"¡Ha ganado {entrenador1.nombre} con {pokemon1.nombre}!\n")
                victorias += 1

            pokemon2 = None

        elif opcion == 'F':
            print("\n--- Finalizando juego ---")
            if pokemon1:
                print(f"Tu Pokémon: {pokemon1.nombre} | Ataque máximo: {pokemon1.max_ataque} | Vida actual: {pokemon1.vida_actual}/{pokemon1.vida_max}")
            print(f"Encuentros ganados: {victorias} | Encuentros perdidos: {derrotas}")
            break
        else:
            print("Opción inválida. Use 'P' para pelear o 'F' para finalizar.\n")

if __name__ == '__main__':
    main()
