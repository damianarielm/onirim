from random import shuffle

azul, verde, marron, roja = "Azul", "Verde", "Marron", "Roja"
luna, sol, llave = "☽", "☀", "⚷"
puerta, pesadilla = "Puerta", ("Pesadilla", "Negra")

mazo =  [pesadilla] * 10
mazo += [(puerta, azul)] * 2 + [(puerta, verde)] * 2
mazo += [(puerta, roja)] * 2 + [(puerta, marron)] * 2
mazo += [(sol, roja)] * 9 + [(luna, roja)] * 4 + [(llave, roja)] * 3
mazo += [(sol, azul)] * 8 + [(luna, azul)] * 4 + [(llave, roja)] * 3
mazo += [(sol, verde)] * 7 + [(luna, verde)] * 4 + [(llave, verde)] * 3
mazo += [(sol, marron)] * 6 + [(luna, marron)] * 4 + [(llave, marron)] * 3
shuffle(mazo)

def manoInicial(mazo, mano):
    for carta in mazo:
        if carta != pesadilla and carta[0] != puerta:
            mazo.remove(carta)
            mano += [carta]
        if len(mano) >= 5:
            return shuffle(mazo)

def borrarPantalla():
    for _ in range(100): print("")

def mostrarPila(nombre, pila):
    print(f"{nombre}:", end = " ")
    for tipo, color in pila:
        print(f"{tipo} {color}", end = ", ")
    print("")

def menuDeJuego(mazo, puertas, laberinto, mano):
    borrarPantalla()
    print(f"Cartas restantes: {len(mazo)}.")
    mostrarPila("Puertas", [(color, "") for _, color in  puertas])
    mostrarPila("Laberinto", laberinto)
    mostrarPila("Mano", mano)

    indice = int(input("\nElija una carta de su mano: ")) - 1
    print("1 - Jugar")
    print("2 - Descartar")
    return mano[indice], int(input("Elija una opcion: "))

def jugarCarta(laberinto, mano, mazo, carta):
    if not laberinto or carta[0] != laberinto[-1][0]:
        mano.remove(carta)
        laberinto += [carta]

def manejarProfecia(mazo, descarte):
    mostrarPila("\nMazo", mazo[-5:])
    descarte += [mazo.pop(int(input("Descarte una carta del mazo: ")) - 6)]
    mostrarPila("\nMazo", mazo[-4:])

    indices = input("Ingrese el orden de las cartas: ")
    tmp = mazo[-4:]
    for i, j in enumerate(indices):
        mazo[-i - 1] = tmp[-5 + int(j)]

def descartarCarta(carta, mazo, mano, descarte):
    mano.remove(carta)
    descarte += [carta]
    if carta[0] == llave and mazo:
        manejarProfecia(mazo, descarte)

def rellenarMano(mano, mazo, puertas, descarte):
    limbo = []
    while len(mano) < 5 and mazo:
        carta = mazo.pop()
        if carta[0] == puerta:
            limbo += manejarPuerta(mano, mazo, puertas, carta[1])
        elif carta == pesadilla:
            descarte += [carta]
            limbo += manejarPesadilla(mano, puertas, mazo, descarte)
        else:
            mano += [carta]
    if limbo:
        mazo += limbo
        shuffle(mazo)

def menuPesadilla(mano, puertas):
    print("\nHas encontrado una pesadilla!")
    mostrarPila("Mano", mano)
    print("\n1 - Descartar 5 cartas del mazo")
    print("2 - Descartar la mano")
    if llave in [tipo for tipo, _ in mano]:
        print("3 - Descartar una llave")
    if puertas:
        print("4 - Descartar una puerta")
    return int(input("Elija una opcion: "))

def manejarPesadilla(mano, puertas, mazo, descarte):
    opcion = menuPesadilla(mano, puertas)
    limbo = []
    if opcion == 1:
        mostrarPila("\nMazo", mazo[-5:])
        for carta in mazo[-5:]:
            mazo.remove(carta)
            if carta == pesadilla or carta[0] == puerta:
                limbo += [carta]
            else:
                descarte += [carta]
        input("Presione enter para cotinuar.")
    elif opcion == 2:
        descarte += mano
        mano.clear()
        manoInicial(mazo, mano)
    elif opcion == 3:
        mostrarPila("Llaves", [carta for carta in mano if carta[0] == llave])
        color = input("Ingrese un color: ")
        mano.remove((llave, color))
        descarte += [(llave, color)]
    else:
        mostrarPila("Puertas", puertas)
        color = input("Ingrese un color: ")
        puertas.remove((puerta, color))
        limbo = [(puerta, color)]

    return limbo

def manejarPuerta(mano, mazo, puertas, color):
    if (llave, color) in mano:
        print(f"Has encontrado una puerta {color}!")
        if input("Deseas usar la llave? (S/N): ") == "S":
            mano.remove((llave, color))
            puertas += [(puerta, color)]
            return []

    return [(puerta, color)]

consecutivas = 0
laberinto, puertas, mano, descarte = [], [], [], []
manoInicial(mazo, mano)
while len(puertas) != 8 and mano:
    carta, opcion = menuDeJuego(mazo, puertas, laberinto, mano)

    if opcion == 1:
        jugarCarta(laberinto, mano, mazo, carta)
        if len(laberinto) > 1 and laberinto[-1][1] != laberinto[-2][1]:
            consecutivas = 0
        if not laberinto or carta[1] == laberinto[-1][1]:
            consecutivas += 1
        if consecutivas == 3:
            consecutivas = 0
            mazo.remove((puerta, carta[1]))
            puertas += [(puerta, carta[1])]
            shuffle(mazo)
    elif opcion == 2:
        descartarCarta(carta, mazo, mano, descarte)

    rellenarMano(mano, mazo, puertas, descarte)

print("\n{'Ganaste' if len(puertas) == 8 else 'Perdiste'}!")
