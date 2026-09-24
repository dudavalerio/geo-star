import math
import pyxel
import random

class TelaInicial:
    def __init__(self):
        self.titulo_completo = "BEM VINDO AO GEO-STAR"
        self.titulo_atual = ""

    def update(self):
        if len(self.titulo_atual) < len(self.titulo_completo):
            if pyxel.frame_count % 2 == 0:
                self.titulo_atual += self.titulo_completo[len(self.titulo_atual)]
        
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_KP_ENTER):
            if len(self.titulo_atual) < len(self.titulo_completo):
                self.titulo_atual = self.titulo_completo
            else:
                pyxel.play(0, 0)  # Toca som de início/menu
                return "JOGANDO"
                
        return "TELA_INICIAL"

    def draw(self):
        pyxel.cls(0)
        pyxel.text(120, 130, self.titulo_atual, 7)
        
        if len(self.titulo_atual) == len(self.titulo_completo):
            if (pyxel.frame_count // 15) % 2 == 0:
                pyxel.text(100, 160, "Pressione ENTER para continuar", 13)

class ModalColeta:
    def __init__(self, estrela):
        self.estrela = estrela
    
    def desenhar(self):
        for y in range(0, 300, 2):
            for x in range(0, 400, 2):
                pyxel.pset(x, y, 0)
                pyxel.pset(x + 1, y + 1, 0)
        
        pyxel.rect(104, 114, 200, 50, 0)
        pyxel.rect(100, 110, 200, 50, 11)
        pyxel.rectb(100, 110, 200, 50, 7)
        
        pyxel.text(110, 122, f"Estrela em ({self.estrela.x}, {self.estrela.y}) capturada!", 0)

class ModalFimJogo:
    def desenhar(self):
        for y in range(0, 300, 2):
            for x in range(0, 400, 2):
                pyxel.pset(x, y, 0)
                pyxel.pset(x + 1, y + 1, 0)
                
        pyxel.rect(134, 124, 140, 40, 0)
        pyxel.rect(130, 120, 140, 40, 0)
        pyxel.rectb(130, 120, 140, 40, 8)

        pyxel.text(155, 132, "FIM DE JOGO!", 8)
        pyxel.text(142, 144, "Acabaram as tentativas", 7)

class ModalVitoria:
    def __init__(self, total_estrelas, tentativas_restantes):
        self.total_estrelas = total_estrelas
        self.tentativas_restantes = tentativas_restantes

    def desenhar(self):
        for y in range(0, 300, 2):
            for x in range(0, 400, 2):
                pyxel.pset(x, y, 0)
                pyxel.pset(x + 1, y + 1, 0)
                
        pyxel.rect(104, 114, 200, 60, 0)
        pyxel.rect(100, 110, 200, 60, 0)
        pyxel.rectb(100, 110, 200, 60, 11)

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
        pyxel.mouse(True)

    def desenhar(self):
        for x in range(-7, 8):
            tela_x = 250 + x * 20
            pyxel.line(tela_x, 40, tela_x, 300, 1)
            
        for y in range(-6, 7):
            tela_y = 170 - y * 20
            pyxel.line(100, tela_y, 400, tela_y, 1)
            
        pyxel.line(100, 170, 400, 170, 7)
        pyxel.line(250, 40, 250, 300, 7)
            
        for x in range(-7, 8):
            if x != 0:
                tela_x = 250 + x * 20
                pyxel.text(tela_x, 174, str(x), 12)
        
        pyxel.text(245, 174, '0', 7)
        
        for y in range(-6, 7):
            if y != 0:
                tela_y = 170 - y * 20
                pyxel.text(254, tela_y, str(y), 9)
        
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

        # Configuração dos Sons do Pyxel (Canal 0 ao 4)
        # Sintaxe: set(notas, tom, volume, efeito, velocidade)
        pyxel.sound(0).set("c3e3g3c4", "p", "7", "n", 10)  # Som 0: Início / Menu
        pyxel.sound(1).set("g4c5", "s", "7", "n", 8)        # Som 1: Estrela coletada
        pyxel.sound(2).set("c2", "n", "5", "f", 12)        # Som 2: Tentativa errada
        pyxel.sound(3).set("g3d3a2", "t", "7", "f", 20)    # Som 3: Game Over
        pyxel.sound(4).set("c4e4g4c5", "p", "7", "n", 10)  # Som 4: Vitória

        self.estado = "TELA_INICIAL"
        self.tela_inicial = TelaInicial()
        
        self.texto_1 = "1"  
        self.texto_2 = "3"  
        self.foco_input = "a"
        self.mudou_valores = False  
        
        self.modal = None
        self.mostrar_modal = False
        self.modal_timer = 0  
        
        self.plano = Plano()
        self.reta1 = Reta(1, 3)
        
        self.quant_estrelas = random.randint(4, 8)
        self.tentativas_restantes = self.quant_estrelas * 2
        
        self.modal_fim = None
        self.jogo_encerrado = False
        self.fim_timer = 0  
        
        self.modal_vitoria = None
        self.jogo_vencido = False
        self.vitoria_timer = 0  
        
        self.estrelas = []
        posicoes = []
        for i in range(self.quant_estrelas):
            x = random.randint(-7, 7)
            y = random.randint(-6, 6)
            while (x, y) in posicoes:
                x = random.randint(-7, 7)
                y = random.randint(-6, 6)
            estrela = Estrela(x, y)
            self.estrelas.append(estrela)
            posicoes.append((x, y))      

        pyxel.run(self.update, self.draw)
    
    def update(self):
        if self.estado == "TELA_INICIAL":
            proximo_estado = self.tela_inicial.update()
            if proximo_estado == "JOGANDO":
                self.estado = "JOGANDO"
            return

        if self.mostrar_modal:
            self.modal_timer -= 1    
            if self.modal_timer <= 0:
                self.mostrar_modal = False 
            return 
        
        if self.jogo_vencido:
            self.vitoria_timer -= 1
            if self.vitoria_timer <= 0:
                pyxel.quit()  
            return
        
        if self.jogo_encerrado:
            self.fim_timer -= 1      
            if self.fim_timer <= 0:
                pyxel.quit()        
            return

        caracteres_digitados = pyxel.input_text
        for caractere in caracteres_digitados:
            if caractere.isdigit() or caractere in ('-', '.', '/'):
                if self.foco_input == "a":
                    self.texto_1 += caractere
                    self.mudou_valores = True
                elif self.foco_input == "b":
                    self.texto_2 += caractere
                    self.mudou_valores = True

        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            if self.foco_input == "a":
                self.texto_1 = self.texto_1[:-1]
                self.mudou_valores = True
            elif self.foco_input == "b":
                self.texto_2 = self.texto_2[:-1]
                self.mudou_valores = True
                
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_KP_ENTER):
            if self.mudou_valores:
                try:
                    if self.texto_1 in ("", "-"): self.texto_1 = "0"
                    if self.texto_2 in ("", "-"): self.texto_2 = "0"
                    
                    self.reta1.a = int(self.texto_1)
                    self.reta1.b = int(self.texto_2)
                    
                    pegou_estrela = self.verificar_todas_colisoes()
                    
                    # Checa condição de vitória
                    if all(e.coletada for e in self.estrelas):
                        self.jogo_vencido = True
                        self.modal_vitoria = ModalVitoria(self.quant_estrelas, self.tentativas_restantes)
                        self.vitoria_timer = 180  
                        pyxel.play(0, 4)  # Toca som de vitória
                    
                    # Se submeteu e NÃO pegou estrela, desconta tentativa e toca som de erro
                    if not pegou_estrela and not self.jogo_vencido:
                        self.tentativas_restantes -= 1
                        pyxel.play(0, 2)  # Toca som de erro/tentativa perdida
                        
                        if self.tentativas_restantes <= 0:
                            self.jogo_encerrado = True
                            self.modal_fim = ModalFimJogo()  
                            self.fim_timer = 180  
                            pyxel.play(0, 3)  # Toca som de Game Over

                    self.mudou_valores = False

                except ValueError:
                    pass 
            
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if 8 <= pyxel.mouse_x <= 78 and 22 <= pyxel.mouse_y <= 42:
                self.foco_input = "a"
            elif 8 <= pyxel.mouse_x <= 78 and 62 <= pyxel.mouse_y <= 82:
                self.foco_input = "b"

    def verificar_todas_colisoes(self):
        colidiu_agora = False
        for estrela in self.estrelas:
            if not estrela.coletada:
                numerador = abs(self.reta1.a * estrela.x - estrela.y + self.reta1.b)
                denominador = math.sqrt(self.reta1.a**2 + 1)
                distancia = numerador / denominador
                
                if distancia <= 0.3:
                    estrela.coletada = True
                    self.modal = ModalColeta(estrela) 
                    self.mostrar_modal = True
                    self.modal_timer = 120  
                    colidiu_agora = True
                    pyxel.play(0, 1)  # Toca som de estrela coletada
                    print(f"⭐ Estrela na coordenada ({estrela.x}, {estrela.y}) capturada!")
                    
        return colidiu_agora

    def draw(self):
        pyxel.cls(0)
        
        if self.estado == "TELA_INICIAL":
            self.tela_inicial.draw()
            return
        
        self.plano.desenhar()
        self.reta1.desenhar()
        
        for estrela in self.estrelas:
            estrela.desenhar()
            
        pyxel.text(239, 10, 'GeoStar', 10)
        pyxel.text(10, 95, f"Tentativas Restantes: {self.tentativas_restantes}", 8 if self.tentativas_restantes <= 2 else 7)
        
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
        
        if self.mostrar_modal and self.modal is not None:
            self.modal.desenhar()
        
        if self.jogo_encerrado and self.modal_fim is not None:
            self.modal_fim.desenhar()
            
        if self.jogo_vencido and self.modal_vitoria is not None:
            self.modal_vitoria.desenhar()
         
Jogo()