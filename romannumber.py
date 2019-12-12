class RomanNumber():
    __valores = {'I':1, 'V': 5, 'X':10, 'L': 50, 'C':100, 'D': 500, 'M': 1000}
    __valores5 = { 'V': 5,  'L': 50,  'D': 500 } 
    __simbolosOrdenados = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
    __rangos = {
        0: {1: 'I', 5 : 'V', 'next': 'X'},
        1: {1: 'X', 5 : 'L', 'next': 'C'},
        2: {1: 'C', 5 : 'D', 'next': 'M'},
        3: {1: 'M', 'next': ''}
    }

    def __init__(self, value):
        if isinstance(value,int):
            self.value = value
            self.__romanValue = self.__arabigo_a_romano()
        elif isinstance(value,str):
            self.__romanValue = value
            self.value = self.__romano_a_arabigo()
        else:
            raise TypeError('Argumento de RomanNumber debe ser un entero o una cadena')

    
    def __invertir(self, cad):
        return cad[::-1]

    def __gruposDeMil(self):
        cad = str(self.value)
        dac = self.__invertir(cad)
        grupos = []
        rango = 0
        for i in range(0, len(dac), 3):
            grupos.append([rango, int(self.__invertir(dac[i:i+3]))])
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
    
    def __arabigo_individual(self, valor):
        cad = self.__invertir(str(valor))
        res = ''

        for i in range(len(cad)-1, -1, -1):
            digit = int(cad[i])
            if digit <= 3:
                res += digit*self.__rangos[i][1]
            elif digit == 4:
                res += (self.__rangos[i][1]+self.__rangos[i][5])
            elif digit == 5:
                res += self.__rangos[i][5]
            elif digit < 9:
                res += (self.__rangos[i][5]+self.__rangos[i][1]*(digit-5))
            else:
                res += self.__rangos[i][1]+self.__rangos[i]['next']

        return res

    def __arabigo_a_romano(self):
        g1000 = self.__gruposDeMil()
        romanoGlobal = ''
        for grupo in g1000:
            rango = grupo[0]
            numero = grupo[1]
            if numero > 0:
                miRomano = '(' * rango + self.__arabigo_individual(numero) + ')'*rango
            else: 
                miRomano = ''
            romanoGlobal += miRomano

        return romanoGlobal

    def __numParentesis(self, cadena):
        num = 0
        for c in cadena:
            if c == '(':
                num += 1
            else:
                break
        return num

    def __contarParentesis(self):
        res = []
        grupoParentesis = self.__romanValue.split(')')
        ix = 0

        while ix < len(grupoParentesis):
            grupo = grupoParentesis[ix]
            numP = self.__numParentesis(grupo)
            if numP > 0:
                for j in range(ix+1, ix+numP):
                    if grupoParentesis[j] != '':
                        raise ValueError ('Símbolos entre paréntesis de cierre') #Explota o Falla
                ix += numP - 1

            if len(grupo[numP:]) > 0:
                res.append((numP, grupo[numP:]))
            ix += 1
    
        #Este if sirve para tratar los casos de parentesis mal formateados
        for i in range(len(res)-1):
            if res[i][0] <= res[i+1][0]:
                raise ValueError ('Número de paréntesis incorrecto')

        return res

    def __romano_individual(self, numRomano):
        numRepes = 1
        resta = False
        penultimoCaracter = ''
        ultimoCaracter = ''
        numArabigo = 0

        for letra in numRomano: 
            #incrementamos el valor del número arábigo con el valor numérico del símbolo romano
            if letra in self.__valores:
                numArabigo += self.__valores[letra]
                if ultimoCaracter == '':
                    pass
                elif resta and self.__valores[penultimoCaracter] <= self.__valores[letra]:
                    raise ValueError ('Si el romano resta luego no puede sumar')
                elif penultimoCaracter != '' and self.__valores[penultimoCaracter] < self.__valores[letra]:
                    raise ValueError ('Si los dos últimos restan el penúltimo no puede ser menor que el último')
                elif self.__valores[ultimoCaracter] > self.__valores[letra]:
                    numRepes = 1
                    resta = False
                elif self.__valores[ultimoCaracter] == self.__valores[letra]:
                    numRepes += 1
                    resta = False
                    if letra in self.__valores5:
                        raise ValueError ('Romanos de tipo cinco no se pueden repetir más de una vez')
                    if numRepes > 3:
                        raise ValueError ('Romanos de tipo uno no se pueden repetir más de tres veces')
                elif self.__valores[ultimoCaracter] < self.__valores[letra]:
                    if numRepes > 1: # No permite repeticiones en las restas
                        raise ValueError ('No se admiten repeticiones en las restas')
                    if ultimoCaracter in self.__valores5: #No permite restas de valores de 5 (5, 50, 500)
                        raise ValueError ('Romanos de tipo cinco no se pueden restar')
                    distancia = self.__simbolosOrdenados.index(letra) - self.__simbolosOrdenados.index(ultimoCaracter) #No permite que se resten unidades de más de un orden
                    if distancia > 2:
                        raise ValueError ('No se pueden restar unidades de más de un orden')
                    numArabigo -= self.__valores[ultimoCaracter]*2
                    resta = True
                    numRepes = 1
                    
            else:  #si el simbolo romano no es permitido devolvemos error (0)
                raise ValueError ('Símbolo incorrecto')
    
            penultimoCaracter = ultimoCaracter
            ultimoCaracter = letra

        return numArabigo

    def __romano_a_arabigo(self):
        numArabigoTotal = 0
        res = self.__contarParentesis()

        for elemento in res:
            romano = elemento[1]
            factor = pow(10, 3 * elemento[0])
            numArabigoTotal += self.__romano_individual(romano) * factor

        return numArabigoTotal

    def __str__(self):
        return self.__romanValue
    
    def __repr__(self):
        return self.__romanValue

    def __add__(self, value):
        resultado = self.value + int(value.value)
        resultado = RomanNumber(resultado)
        return resultado

    def __radd__(self, value):
        return self.__add__(value)

    def __sub__(self, value):
        resultado = max(0, self.value - int(value.value))
        resultado = RomanNumber(resultado)
        return resultado

    def __rsub__(self, value):
        return self.__sub__(value)

    def __mul__(self, value):
        resultado = self.value * int(value.value)
        resultado = RomanNumber(resultado)
        return resultado

    def __rmul__(self, value):
        return self.__mul__(value)

    def __truediv__(self, value):
        resultado = self.value // int(value.value)
        resultado = RomanNumber(resultado)
        return resultado

    def __rtruediv__(self, value):
        return self.__truediv__(value)

    def __div__(self, value):
        return self.__truediv__(value)

    def __rdiv__(self, value):
        return self.__div__(value)