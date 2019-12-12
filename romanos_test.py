import unittest
from romanos import romano_a_arabigo, arabigo_a_romano, contarParentesis, gruposDeMil
from romannumber import RomanNumber

class RomanNumberTest(unittest.TestCase):
    def test_symbols_romans(self):
        self.assertEqual(romano_a_arabigo('I'), 1)
        self.assertEqual(romano_a_arabigo('V'), 5)
        self.assertEqual(romano_a_arabigo('X'), 10)
        self.assertEqual(romano_a_arabigo('L'), 50)
        self.assertEqual(romano_a_arabigo('C'), 100)
        self.assertEqual(romano_a_arabigo('D'), 500)
        self.assertEqual(romano_a_arabigo('M'), 1000)
        self.assertEqual(romano_a_arabigo('A'), 0)
   
    def test_numeros_crecientes(self):
        self.assertEqual(romano_a_arabigo('XVI'), 16)
        self.assertEqual(romano_a_arabigo('III'), 3)
        self.assertEqual(romano_a_arabigo('VIX'), 0)

    def test_no_mas_de_tres_repeticiones(self):
        self.assertEqual(romano_a_arabigo('LXXIII'), 73)
        self.assertEqual(romano_a_arabigo('IIII'), 0)
        self.assertEqual(romano_a_arabigo('VVV'), 0)

    def test_numeros_decrecientes(self):
        self.assertEqual(romano_a_arabigo('IX'), 9)
        self.assertEqual(romano_a_arabigo('CMXCIX'), 999)

    def test_si_resta_no_suma(self):
        self.assertEqual(romano_a_arabigo('IXII'), 0)
        self.assertEqual(romano_a_arabigo('XCX'), 0)
        self.assertEqual(romano_a_arabigo('XLVIII'), 48)
 
    def test_restas_no_admiten_repeticiones(self):
        self.assertEqual(romano_a_arabigo('MIIX'), 0)

    def test_restas_no_admiten_derivados_del_5(self):
        self.assertEqual(romano_a_arabigo('VC'),0)

    def test_restas_no_admiten_mas_de_un_orden_de_diferencia(self):
        self.assertEqual(romano_a_arabigo('IC'), 0)
        self.assertEqual(romano_a_arabigo('IL'), 0)    
        self.assertEqual(romano_a_arabigo('VL'), 0)    

    def test_numeros_mayores_de_3999(self):
        self.assertEqual(romano_a_arabigo('(IV)'), 4000)
        self.assertEqual(romano_a_arabigo('(VII)CMXXIII'), 7923)
        self.assertEqual(romano_a_arabigo('((VII))(DLIII)DCXXXVII'), 7553637)

    def test_procesar_parentesis(self):
        self.assertEqual(contarParentesis('(IV)'), [(1, 'IV')])
        self.assertEqual(contarParentesis('((VII))(XL)CCCXXII'), [(2, 'VII'), (1, 'XL'), (0, 'CCCXXII')])
        self.assertEqual(contarParentesis('(VI)((VII))'), 0)
        self.assertEqual(contarParentesis('(VI)((VII)'), 0)
        self.assertEqual(contarParentesis('VI)((VII)'), 0)

class ArabicNumberTest(unittest.TestCase):
    def test_unidades(self):
        self.assertEqual(arabigo_a_romano(1), 'I')
        self.assertEqual(arabigo_a_romano(2), 'II')
        self.assertEqual(arabigo_a_romano(4), 'IV')

    def test_arabic_a_roman(self):
        self.assertEqual(arabigo_a_romano(2123), 'MMCXXIII')
        self.assertEqual(arabigo_a_romano(2444), 'MMCDXLIV')
        self.assertEqual(arabigo_a_romano(3555), 'MMMDLV')
        self.assertEqual(arabigo_a_romano(1678), 'MDCLXXVIII')
        self.assertEqual(arabigo_a_romano(2999), 'MMCMXCIX')

    def test_arabic_a_roman_gt_3999(self):
        self.assertEqual(arabigo_a_romano(4000), '(IV)')
        self.assertEqual(arabigo_a_romano(7763147686), '(((VII)))((DCCLX))(MMMCXLVII)DCLXXXVI')

    def test_gruposDe1000(self):
        self.assertEqual(gruposDeMil(7763147686), [[3, 7], [2, 760],[1, 3147], [0, 686]])
        self.assertEqual(gruposDeMil(3763142686), [[3, 0], [2, 3760],[1, 3140], [0, 2686]])

class RomanNumberClassTest(unittest.TestCase):
    def test_create_romannumber(self):
        nr = RomanNumber(23)
        self.assertEqual(str(nr), 'XXIII')

        onr = RomanNumber('XXIII')
        self.assertEqual(onr.value, 23)


if __name__ == '__main__':
    unittest.main()