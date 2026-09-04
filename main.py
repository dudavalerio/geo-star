import pyxel
class Estrela:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coletada = False
    def desenhar(self):
        if not self.coletada:
            tela_x, tela_y = self.converter_coordenada()
            pyxel.text(tela_x, tela_y, '*', 7)
    def converter_coordenada(self):
        tela_x = 250 + self.x * 20
        tela_y = 170 - self.y * 20
        return tela_x, tela_y

class Reta:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def calcular_y(self, x):
        return self.a * x + self.b
    def passa_por(self, estrela):
        y_calculado = self.calcular_y(estrela.x)
        return y_calculado == estrela.y
    #Vericar todas as estrelas quando encontrar ele coleta
    def coletar_estrelas(self, estrelas):
        for estrela in estrelas:
            if self.passa_por(estrela):
                estrela.coletada = True
    def desenhar(self):
        anterior_x = None
        anterior_y = None
        for x in range(-10, 11):
            y = self.calcular_y(x)
            tela_x = 250 + x * 20
            tela_y = 170 - y * 20
            if anterior_x is not None:
                pyxel.line(anterior_x, anterior_y, tela_x, tela_y, 8)
            anterior_x = tela_x
            anterior_y = tela_y
estrelas = [Estrela(1,-1), Estrela(3,2), Estrela(-4,3), Estrela(5,-2), Estrela(2,5)]
reta1 = Reta(2, 1)
reta1.coletar_estrelas(estrelas)

class Jogo:
    #Contador de estrelas, ele tem que mostrar números de estrelas coletados
    def contar_estrelas(self, estrelas):
        total_de_estrelas = 0
        for estrela in estrelas:
            if estrela.coletada:
                 total_de_estrelas += 1
        return total_de_estrelas
    def update(self):
        pass
    def draw(self):
        #Painel Superior
        pyxel.rect(0, 0, 100, 300, 1)
        #pyxel.text(10, 10, 'GeoStar', 7)
        total_de_estrelas = self.contar_estrelas(estrelas)
        pyxel.text(10,20,f'Estrelas: {total_de_estrelas}/ {len(estrelas)}',7)
        #Os dois for, é pra converter grade em conversão matemático pra ficar alinhados com o grade no jg.
        # Grade Vertical
        for x in range(-7, 8):
            tela_x = 250 + x * 20
            pyxel.line(tela_x, 40, tela_x, 300, 1)
        #Grade Horizontal
        for y in range(-6, 7):
            tela_y = 170 - y * 20
            pyxel.line(100, tela_y, 400, tela_y, 1)
        # Eixos
        pyxel.line(100, 170, 400, 170, 7)
        pyxel.line(250, 40, 250, 300, 7)
        #Números do eixo X
        for x in range(-7, 8):
            if x != 0:
                tela_x = 250 + x * 20#Calculamos onde ele deve aparecer na tela
                pyxel.text(tela_x, 174, str(x), 12)
        pyxel.text(245, 174, '0', 7)
        #Números do eixo y
        for y in range(-6, 7):
            if y != 0:
                tela_y = 170 - y * 20#Calculamos onde ele deve aparecer na tela
                pyxel.text(254, tela_y, str(y), 9)
        # Reta
        reta1.desenhar()
        # Estrelas
        for estrela in estrelas:
            estrela.desenhar()
print(reta1.passa_por(estrelas[0]))
jogo = Jogo()
pyxel.init(400, 300, title='GeoStar')
pyxel.run(jogo.update, jogo.draw)