import math
import pyxel
import random


class ModalColeta:
    def __init__(self, estrela):
        self.estrela = estrela
    
    def desenhar(self):
        # Efeito de sombra/overlay, varre a tela pulando pixels para criar uma cortina semitransparente escura
        for y in range(0, 300, 2):
            for x in range(0, 400, 2):
                pyxel.pset(x, y, 0)       # Pixels pretos intercalados
                pyxel.pset(x + 1, y + 1, 0)
        
        # Retãngulo sobreposto a tela, simulando uma modal
        pyxel.rect(104, 114, 200, 50, 0)  # Retângulo preto ao fundo para dar profundidade
        pyxel.rect(100, 110, 200, 50, 11)   # Caixa verde
        pyxel.rectb(100, 110, 200, 50, 7)   # Borda branca da caixa
        
        # Texto da modal
        pyxel.text(110, 122, f"Estrela em ({self.estrela.x}, {self.estrela.y}) capturada!", 0)
        
class ModalFimJogo:
    def desenhar(self):
       # Efeito de sombra/overlay, varre a tela pulando pixels para criar uma cortina semitransparente escura
        for y in range(0, 300, 2):
            for x in range(0, 400, 2):
                pyxel.pset(x, y, 0)       # Pixels pretos intercalados
                pyxel.pset(x + 1, y + 1, 0)
                
        # Retãngulo sobreposto a tela, simulando uma modal
        pyxel.rect(134, 124, 140, 40, 0)
        pyxel.rect(130, 120, 140, 40, 0)    # Fundo preto 
        pyxel.rectb(130, 120, 140, 40, 8)   # Borda vermelha

        # Texto da modal
        pyxel.text(155, 132, "FIM DE JOGO!", 8)
        pyxel.text(142, 144, "Acabaram as tentativas", 7)

class ModalVitoria:
    # Recebe o total de estrelas e as tentativas que sobraram para mostrar no status
    def __init__(self, total_estrelas, tentativas_restantes):
        self.total_estrelas = total_estrelas
        self.tentativas_restantes = tentativas_restantes

    def desenhar(self):
        # Efeito de sombra/overlay, varre a tela pulando pixels para criar uma cortina semitransparente escura
        for y in range(0, 300, 2):
            for x in range(0, 400, 2):
                pyxel.pset(x, y, 0)       # Pixels pretos intercalados
                pyxel.pset(x + 1, y + 1, 0)
                
        # Retãngulo sobreposto a tela, simulando uma modal
        pyxel.rect(104, 114, 200, 60, 0)    # Sombra
        pyxel.rect(100, 110, 200, 60, 0)    # Fundo preto 
        pyxel.rectb(100, 110, 200, 60, 11)  # Borda verde

        # Textos da modal
        pyxel.text(110, 118, "VOCÊ VENCEU!", 11)
        pyxel.text(110, 130, "Todas as estrelas foram coletadas!", 7)
        pyxel.text(110, 145, f"Estrelas capturadas: {self.total_estrelas}", 7)
        pyxel.text(110, 155, f"Tentativas restantes: {self.tentativas_restantes}", 7)



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

class Plano:
    def __init__(self):
        
        # Habilita a visibilidade do cursor do mouse
        pyxel.mouse(True)

    def desenhar(self):
        # Grade Vertical
        for x in range(-7, 8):
            tela_x = 250 + x * 20
            pyxel.line(tela_x, 40, tela_x, 300, 1)
            
        # Grade Horizontal
        for y in range(-6, 7):
            tela_y = 170 - y * 20
            pyxel.line(100, tela_y, 400, tela_y, 1)
            
        # Eixos principais destacados por cima da grade
        pyxel.line(100, 170, 400, 170, 7)
        pyxel.line(250, 40, 250, 300, 7)
            
        # Números do eixo X
        for x in range(-7, 8):
            if x != 0:
                tela_x = 250 + x * 20
                pyxel.text(tela_x, 174, str(x), 12)
        
        pyxel.text(245, 174, '0', 7)
        
        # Números do eixo Y
        for y in range(-6, 7):
            if y != 0:
                tela_y = 170 - y * 20
                pyxel.text(254, tela_y, str(y), 9)
        
        # Coordenadas no cursor
        mouse_tela_x = pyxel.mouse_x
        mouse_tela_y = pyxel.mouse_y
        
        centro_grade_x = 250
        centro_grade_y = 170
        
        cartesian_x = round((mouse_tela_x - centro_grade_x) / 20)
        cartesian_y = round((centro_grade_y - mouse_tela_y) / 20)
        
        texto_coordenadas = f"X: {cartesian_x}, Y: {cartesian_y}"
        pyxel.text(mouse_tela_x + 10, mouse_tela_y + 10, texto_coordenadas, 7)


class Jogo:
    def __init__(self):
        pyxel.init(400, 300, title="GeoStar - Desafio das Retas")
        
        self.texto_1 = ""  
        self.texto_2 = ""  
        self.foco_input = "a"
        
        # Inicialização das flags de controle da Modal
        self.modal = None
        self.mostrar_modal = False
        self.modal_timer = 0  # variável para contar o tempo da modal
        
        self.reta1 = Reta(1, 3)
        
        quant = random.randint(4, 8)
        self.tentativas_restantes = quant * 2
        
        self.modal_fim = None
        self.jogo_encerrado = False
        self.fim_timer = 0  # variável para contar o tempo da modal de fim do jogo
        
        self.modal_vitoria = None
        self.jogo_vencido = False
        self.vitoria_timer = 0  # fechar o jogo após a vitória
        
        # Criamos o Plano cartesiano
        self.plano = Plano()
        
        # Criamos a nossa reta inicial padrão (a=1, b=3)
        self.reta1 = Reta(1, 3)
        
        #Quantidade de estrelas aleatória
        quant = random.randint(4,8)
        #Lista de estrelas do jogo
        self.estrelas = []
        posições = []
        for i in range(quant):
            x = random.randint(-7, 7)
            y = random.randint(-6, 6)
            while (x, y) in posições:
                x = random.randint(-7, 7)
                y = random.randint(-6, 6)
            estrela = Estrela(x, y)
            self.estrelas.append(estrela)
            posições.append((x, y))       
        pyxel.run(self.update, self.draw)
    
    def update(self):
        # Lógica da modal temporizada
        if self.mostrar_modal:
            self.modal_timer -= 1     # Diminui o timer a cada frame
            if self.modal_timer <= 0:
                self.mostrar_modal = False # Esconde a modal quando o tempo acaba
            return # Mantém o jogo pausado enquanto a modal estiver sumindo
        
        # Lógica da modal de vitória temporizada (fecha após 3 segundos)
        if self.jogo_vencido:
            self.vitoria_timer -= 1
            if self.vitoria_timer <= 0:
                pyxel.quit()  # Fecha o jogo automaticamente
            return
        
        
        if self.jogo_encerrado:
            self.fim_timer -= 1      # Diminui o timer a cada frame
            if self.fim_timer <= 0:
                pyxel.quit()         # Fecha o jogo automaticamente após o temporizador
                #Tela Inicial?
            return # Impede que qualquer outra lógica rode após o fim do jogo

        caracteres_digitados = pyxel.input_text
        
        for caractere in caracteres_digitados:
            if caractere.isdigit() or caractere in ('-', '.', '/'):
                if self.foco_input == "a":
                    self.texto_1 += caractere
                elif self.foco_input == "b":
                    self.texto_2 += caractere

        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            if self.foco_input == "a":
                self.texto_1 = self.texto_1[:-1]
            elif self.foco_input == "b":
                self.texto_2 = self.texto_2[:-1]
                
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_KP_ENTER):
            try:
                if self.texto_1 in ("", "-"): self.texto_1 = "0"
                if self.texto_2 in ("", "-"): self.texto_2 = "0"
                
                self.reta1.a = int(self.texto_1)
                self.reta1.b = int(self.texto_2)
                
                coletadas_antes = sum(1 for e in self.estrelas if e.coletada)
                self.verificar_todas_colisoes()
                coletadas_depois = sum(1 for e in self.estrelas if e.coletada)
                
                if coletadas_depois == coletadas_antes:
                    self.tentativas_restantes -= 1
                    
                if self.tentativas_restantes <= 0:
                    self.jogo_encerrado = True
                    self.modal_fim = ModalFimJogo()  # Instancia a modal
                    self.fim_timer = 90  # 3 segundos

            except ValueError:
                pass 
            
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if 8 <= pyxel.mouse_x <= 78 and 22 <= pyxel.mouse_y <= 42:
                self.foco_input = "a"
            elif 8 <= pyxel.mouse_x <= 78 and 62 <= pyxel.mouse_y <= 82:
                self.foco_input = "b"

    def verificar_todas_colisoes(self):
        for estrela in self.estrelas:
            if not estrela.coletada:
                numerador = abs(self.reta1.a * estrela.x - estrela.y + self.reta1.b)
                denominador = math.sqrt(self.reta1.a**2 + 1)
                distancia = numerador / denominador
                
                if distancia <= 0.3:
                    estrela.coletada = True
                    self.modal = ModalColeta(estrela) 
                    self.mostrar_modal = True
                    self.modal_timer = 120  # Define que a modal vai durar 120 frames (4 segundos)
                    print(f"⭐ Estrela na coordenada ({estrela.x}, {estrela.y}) capturada!")

    def draw(self):
        pyxel.cls(0)
        
        #Desenha o Plano de fundo primeiro
        self.plano.desenhar()
        
        # Desenha a Reta e as Estrelas
        self.reta1.desenhar()
        
        for estrela in self.estrelas:
            estrela.desenhar()
            
        pyxel.text(239, 10, 'GeoStar', 10)
        pyxel.text(10, 95, f"Tentativas Restantes: {self.tentativas_restantes}", 8 if self.tentativas_restantes <= 2 else 7)
        # Interface de Texto por cima
        pyxel.text(239, 10, 'GeoStar', 10)
        
        pyxel.text(10, 10, "Valor de 'a' (inclinacao):", 7)
        cor_borda_a = 11 if self.foco_input == "a" else 5  
        pyxel.rectb(8, 22, 70, 20, cor_borda_a)
        
        pyxel.text(10, 52, "Valor de 'b' (intercepto Y):", 7)
        cor_borda_b = 11 if self.foco_input == "b" else 5  
        pyxel.rectb(8, 62, 70, 20, cor_borda_b)
        
        cursor = "_" if pyxel.frame_count % 30 < 15 else ""
        
        pyxel.text(14, 29, self.texto_1 + (cursor if self.foco_input == "a" else ""), 7)
        pyxel.text(14, 69, self.texto_2 + (cursor if self.foco_input == "b" else ""), 7)
        
        pyxel.mouse(True)
        
        # Telas de sobreposição (coleta e Fim de jogo)
        if self.mostrar_modal and self.modal is not None:
            self.modal.desenhar()
        
        if self.jogo_encerrado:
            self.modal_fim.desenhar()
            
        if self.jogo_vencido:
            self.modal_vitoria.desenhar()
        
Jogo()

