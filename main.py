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
        tela_x = 200 + self.x * 20
        tela_y = 150 - self.y * 20
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
    def desenhar(self):
        anterior_x = None
        anterior_y = None
        for x in range(-10, 11):
            y = self.calcular_y(x)
            tela_x = 200 + x * 20
            tela_y = 150 - y * 20
            if anterior_x is not None:
                pyxel.line(anterior_x, anterior_y, tela_x, tela_y, 8)
            anterior_x = tela_x
            anterior_y = tela_y
estrelas = [Estrela(1,-1), Estrela(3,2), Estrela(-4,3), Estrela(5,-2)]
reta1 = Reta(2, 1)

class Jogo:
    def update(self):
        pass
    def draw(self):
        # Grade
        for x in range(0, 401, 20):
            pyxel.line(x, 0, x, 300, 1)

        for y in range(0, 301, 20):
            pyxel.line(0, y, 400, y, 1)
        # Eixos
        pyxel.line(0, 150, 400, 150, 7)
        pyxel.line(200, 0, 200, 300, 7)
        # Reta
        reta1.desenhar()
        # Estrelas
        for estrela in estrelas:
            estrela.desenhar()
print(reta1.passa_por(estrelas[0]))
jogo = Jogo()
pyxel.init(400, 300, title='GeoStar')
pyxel.run(jogo.update, jogo.draw)