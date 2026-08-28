import pyxel
class Estrela:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def desenhar(self):
        tela_x, tela_y = self.converter_coordenada()
        pyxel.text(tela_x, tela_y, '*', 7)

    def converter_coordenada(self):
        tela_x = 200 + self.x * 20#Corrdenada matemática / 200 Centro da tela
        tela_y = 150 - self.y * 20#20 Cada um unidade matemática vale 20 pixels
        return tela_x, tela_y
    
class Jogo:
    def update(self):
        pass

    def draw(self):
        pyxel.text(100, 100,'GeoStar', 7)#Depois tenho que apagar isso
        pyxel.text(100, 110, 'Desafio das retas', 7)#Depois tenho que apagar isso
        for x in range(0, 401, 20):#Criar grade
            pyxel.line(x, 0, x, 300, 1)
        for y in range(0 , 301, 20):#Criar grade
            pyxel.line(0, y, 400, y, 1)
        pyxel.line(0, 150, 400, 150, 7)#Linha orizontal
        pyxel.line(200, 0, 200, 300, 7)#Linha vertical
        reta1.desenhar()
        for estrela in  estrelas:
            estrela.desenhar()
estrelas = [Estrela(1, -1),
        Estrela(3, 2),
        Estrela(-4, 3),
        Estrela(5, -2)]

class Reta:
    def __init__(self,a, b):
        self.a = a
        self.b = b
        
    def calcular_y(self,x):
        return self.a * x + self.b#Uma função matemática transformado em código
    def desenhar(self):
        anterior_x = None
        anterior_y = None

        for x in range(-10, 11):
            y = self.calcular_y(x)#Vai calcular o y pra cada x

            tela_x = 200 + x * 20
            tela_y = 150 - y * 20#matemático -> tela_y

            if anterior_x is not None:
                pyxel.line(anterior_x, anterior_y, tela_x, tela_y, 8)

            anterior_x = tela_x
            anterior_y = tela_y
reta1 = Reta(2,1)
print((reta1.calcular_y(3)))
jogo = Jogo()
pyxel.init(400, 300, title='GeoStar\033') #Cria a configuração de janela.
pyxel.run(jogo.update, jogo.draw)#Responsável pela lógica do jogo e responsável por desenhar na tela.


