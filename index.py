import math
import pyxel

class Estrela:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coletada = False  # Nova flag para saber se o jogador já pegou esta estrela

    def desenhar(self):
        if not self.coletada:  # Só desenha se não tiver sido coletada
            tela_x, tela_y = self.converter_coordenada()
            # Ajuste leve (-2) para centralizar o caractere '*' visualmente na linha
            pyxel.text(tela_x - 2, tela_y - 2, '*', 10) # Cor 10 (Amarelo) fica ótimo!

    def converter_coordenada(self):
        tela_x = 200 + self.x * 20  # Centro x em 200
        tela_y = 150 - self.y * 20  # Centro y em 150
        return tela_x, tela_y
    
class Reta:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def calcular_y(self, x):
        return self.a * x + self.b

    def desenhar(self):
        anterior_x = None
        anterior_y = None

        for x in range(-10, 11):
            y = self.calcular_y(x)

            tela_x = 200 + x * 20
            tela_y = 150 - y * 20

            if anterior_x is not None:
                # Desenha a linha conectando os pontos da reta (cor vermelha 8)
                pyxel.line(anterior_x, anterior_y, tela_x, tela_y, 8)

            anterior_x = tela_x
            anterior_y = tela_y

class Jogo:
    def __init__(self):
        pyxel.init(400, 300, title="GeoStar - Desafio das Retas")
        
        self.texto_1 = ""  # Guarda o input de 'a'
        self.texto_2 = ""  # Guarda o input de 'b'
        self.foco_input = "a"  # Controla em qual caixa o jogador está digitando ("a" ou "b")
        
        # Criamos a nossa reta inicial padrão (a=1, b=3)
        self.reta1 = Reta(1, 3)
        
        # Lista de estrelas guardada dentro do jogo
        self.estrelas = [
            Estrela(1, -1),
            Estrela(3, 2),
            Estrela(-4, 3),
            Estrela(5, -2)
        ]
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        # Captura os caracteres digitados no teclado
        caracteres_digitados = pyxel.input_text
        
        for caractere in caracteres_digitados:
            # Aceita números e também o sinal de menos '-' para valores negativos
            if caractere.isdigit() or caractere in ('-', '.', '/'):
                if self.foco_input == "a":
                    self.texto_1 += caractere
                elif self.foco_input == "b":
                    self.texto_2 += caractere

        # Apagar caractere com Backspace
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            if self.foco_input == "a":
                self.texto_1 = self.texto_1[:-1]
            elif self.foco_input == "b":
                self.texto_2 = self.texto_2[:-1]
                
        # Quando pressionar ENTER/RETURN
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_KP_ENTER):
            # Tenta converter os textos para número de forma segura
            try:
                if self.texto_1 in ("", "-"): self.texto_1 = "0"
                if self.texto_2 in ("", "-"): self.texto_2 = "0"
                
                self.reta1.a = int(self.texto_1)
                self.reta1.b = int(self.texto_2)
                
                # CHAMA A VERIFICAÇÃO DE COLISÃO APÓS MUDAR A RETA!
                self.verificar_todas_colisoes()
            except ValueError:
                pass # Ignora se houver erro de digitação inválido
            
        # Alternar entre caixas usando o MOUSE (clicando nelas)
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # Se clicou na caixa do 'a'
            if 8 <= pyxel.mouse_x <= 78 and 22 <= pyxel.mouse_y <= 42:
                self.foco_input = "a"
            # Se clicou na caixa do 'b'
            elif 8 <= pyxel.mouse_x <= 78 and 62 <= pyxel.mouse_y <= 82:
                self.foco_input = "b"

    def verificar_todas_colisoes(self):
        # Passa por cada estrela da lista para testar colisão com a reta atual
        for estrela in self.estrelas:
            if not estrela.coletada:
                # 1. Fórmula matemática ponto-reta usando os valores da reta1
                numerador = abs(self.reta1.a * estrela.x - estrela.y + self.reta1.b)
                denominador = math.sqrt(self.reta1.a**2 + 1)
                distancia = numerador / denominador
                
                # 2. Tolerância do raio (0.3 deixa o jogo mais justo e divertido)
                if distancia <= 0.3:
                    estrela.coletada = True
                    print(f"⭐ Estrela na coordenada ({estrela.x}, {estrela.y}) capturada!")

    def draw(self):
        pyxel.cls(0)
        
        # Desenha a Grade Azul (1)
        for x in range(0, 401, 20):
            pyxel.line(x, 0, x, 300, 1)
        for y in range(0, 301, 20):
            pyxel.line(0, y, 400, y, 1)
            
        # Desenha os Eixos Principais Brancos (7)
        pyxel.line(0, 150, 400, 150, 7) # Eixo X
        pyxel.line(200, 0, 200, 300, 7) # Eixo Y
        
        # Desenha a Reta e as Estrelas
        self.reta1.desenhar()
        for estrela in self.estrelas:
            estrela.desenhar()
            
        # Interface de Texto por cima
        pyxel.text(340, 10, 'GeoStar', 10)
        
        # Caixa de Input do 'a'
        pyxel.text(10, 10, "Valor de 'a' (inclinacao):", 7)
        cor_borda_a = 11 if self.foco_input == "a" else 5  # Fica verde (11) se estiver ativa
        pyxel.rectb(8, 22, 70, 20, cor_borda_a)
        
        # Caixa de Input do 'b'
        pyxel.text(10, 52, "Valor de 'b' (intercepto Y):", 7)
        cor_borda_b = 11 if self.foco_input == "b" else 5  # Fica verde (11) se estiver ativa
        pyxel.rectb(8, 62, 70, 20, cor_borda_b)
        
        # Efeito do cursor piscando
        cursor = "_" if pyxel.frame_count % 30 < 15 else ""
        
        # Renderiza os textos separados nas suas respectivas caixas
        pyxel.text(14, 29, self.texto_1 + (cursor if self.foco_input == "a" else ""), 7)
        pyxel.text(14, 69, self.texto_2 + (cursor if self.foco_input == "b" else ""), 7)
        
        # Mostra o status da equação atual na tela
        pyxel.text(250, 280, f"Equacao: y = {self.reta1.a}x + {self.reta1.b}", 12)
        
        pyxel.mouse(True) #habilita o mouse em cima da janela

# Inicializa o jogo diretamente
Jogo()
