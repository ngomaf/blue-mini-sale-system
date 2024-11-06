import locale

locale.setlocale(locale.LC_ALL, '')

class NotDecimal:

    ''' Notacao 1,234.56 (USA) -> 1.123,56 (PT) '''

    def mspp(self, valor): # milhar_sepado_por_ponto
        '''
        -> A presente funcao rescreve um dado valor
        da notaçao 1234.20 para 1.234,20, ou seja separa as casas de milhares
        por ponto "." e decimal por virgula ","
        :param valor: num (notacao 1234.20)
        :return valor: na notacao 1.234,20

        :by ngoma m fortuna
        '''

        # mspp - milhar_sepado_por_ponto
        # Função que recebe um valor na forma 0.5 e retrona 0,5
        # ou 1,000 e retorna 1.000

        valor = '{:.2f}'.format(valor)
        valor = float(valor)
        valor = locale.currency(valor, grouping=True)

        valor_milhar_pt = valor

        return valor_milhar_pt[:-2]

    def mspp_reverse(self, valor): # inverso de milhar_sepado_por_ponto
        """
        -> A presente funcao rescreve um dado valor
        na notaçao 1.234,20 para 1,234.20, ou seja separa as casas de milhares
        por virgula "," e decimal por ponto "."
        :param valor: num (notacao 1.234,20)
        :return valor: na notacao 1,234,20

        :by ngoma m fortuna
        """

        valor = valor

        valor_milhar_us = ('{}'.format(valor).replace('.',''))
        valor_milhar_us = ('{}'.format(valor_milhar_us).replace(',','.'))

        return valor_milhar_us
