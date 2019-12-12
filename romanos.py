valores = {'I':1, 'V': 5, 'X':10, 'L': 50, 'C':100, 'D': 500, 'M': 1000}
valores5 = { 'V': 5,  'L': 50,  'D': 500 } 
simbolosOrdenados = ['I', 'V', 'X', 'L', 'C', 'D', 'M']

rangos = {
    0: {1: 'I', 5 : 'V', 'next': 'X'},
    1: {1: 'X', 5 : 'L', 'next': 'C'},
    2: {1: 'C', 5 : 'D', 'next': 'M'},
    3: {1: 'M', 'next': ''}
}



def numParentesis(cadena):
    num = 0
    for c in cadena:
        if c == '(':
            num += 1
        else:
            break
    return num


def contarParentesis(numRomano):
    res = []
    grupoParentesis = numRomano.split(')')
    ix = 0

    while ix < len(grupoParentesis):
        grupo = grupoParentesis[ix]
        numP = numParentesis(grupo)
        if numP > 0:
            for j in range(ix+1, ix+numP):
                if grupoParentesis[j] != '':
                    return 0 #Explota o Falla
            ix += numP - 1

        if len(grupo[numP:]) > 0:
            res.append((numP, grupo[numP:]))
        ix += 1
   
    #Este if sirve para tratar los casos de parentesis mal formateados
    for i in range(len(res)-1):
        if res[i][0] <= res[i+1][0]:
            return 0

    return res


def romano_individual(numRomano):
    numRepes = 1
    resta = False
    penultimoCaracter = ''
    ultimoCaracter = ''
    numArabigo = 0

    for letra in numRomano: 
        #incrementamos el valor del número arábigo con el valor numérico del símbolo romano
        if letra in valores:
            numArabigo += valores[letra]
            if ultimoCaracter == '':
                pass
            elif resta and valores[penultimoCaracter] <= valores[letra]:
                return 0
            elif penultimoCaracter != '' and valores[penultimoCaracter] < valores[letra]:
                return 0
            elif valores[ultimoCaracter] > valores[letra]:
                numRepes = 1
                resta = False
            elif valores[ultimoCaracter] == valores[letra]:
                numRepes += 1
                resta = False
                if letra in valores5:
                    return 0
                if numRepes > 3:
                    return 0
            elif valores[ultimoCaracter] < valores[letra]:
                if numRepes > 1: # No permite repeticiones en las restas
                    return 0
                if ultimoCaracter in valores5: #No permite restas de valores de 5 (5, 50, 500)
                    return 0
                distancia = simbolosOrdenados.index(letra) - simbolosOrdenados.index(ultimoCaracter) #No permite que se resten unidades de más de un orden
                if distancia > 2:
                    return 0
                numArabigo -= valores[ultimoCaracter]*2
                resta = True
                numRepes = 1
        else:  #si el simbolo romano no es permitido devolvemos error (0)
            return 0
        
        penultimoCaracter = ultimoCaracter
        ultimoCaracter = letra


    return numArabigo


def romano_a_arabigo(numRomano):
    numArabigoTotal = 0
    res = contarParentesis(numRomano)

    for elemento in res:
        romano = elemento[1]
        factor = pow(10, 3 * elemento[0])
        numArabigoTotal += romano_individual(romano) * factor

    return numArabigoTotal


def invertir(cad):
    return cad[::-1]


def gruposDeMil(num):
    cad = str(num)
    dac = invertir(cad)
    grupos = []

    rango = 0
    for i in range(0, len(dac), 3):
        grupos.append([rango, int(invertir(dac[i:i+3]))])
        rango += 1

    for i in range(len(grupos)-1):
        grupoMenor = grupos[i]
        grupoMayor = grupos[i+1]
        unidadesMayor = grupoMayor[1] % 10

        if unidadesMayor < 4:
            grupoMenor[1] = grupoMenor[1] + unidadesMayor * 1000
            grupoMayor[1] = grupoMayor[1] - unidadesMayor

    grupos.reverse()

    return grupos


def arabigo_individual(valor):
    cad = invertir(str(valor))
    res = ''

    for i in range(len(cad)-1, -1, -1):
        digit = int(cad[i])
        if digit <= 3:
            res += digit*rangos[i][1]
        elif digit == 4:
            res += (rangos[i][1]+rangos[i][5])
        elif digit == 5:
            res += rangos[i][5]
        elif digit < 9:
            res += (rangos[i][5]+rangos[i][1]*(digit-5))
        else:
            res += rangos[i][1]+rangos[i]['next']

    return res


def arabigo_a_romano(valor):
    g1000 = gruposDeMil(valor)
    romanoGlobal = ''

    for grupo in g1000:
        rango = grupo[0]
        numero = grupo[1]
        if numero > 0:
            miRomano = '(' * rango + arabigo_individual(numero) + ')'*rango
        else: 
            miRomano = ''
        romanoGlobal += miRomano

    return romanoGlobal