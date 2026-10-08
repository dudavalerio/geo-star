import math
import pyxel
import random
from fractions import Fraction

class Tipografia:
    """Gerencia estilos de texto padronizados para o jogo."""
    
    @staticmethod
    def titulo(x, y, texto):
        pyxel.text(x + 1, y + 1, texto, 1)
        pyxel.text(x, y, texto, 10)

    @staticmethod
    def subtitulo(x, y, texto):
        pyxel.text(x, y, texto, 7)

    @staticmethod
    def aviso(x, y, texto, alerta=False):
        cor = 8 if alerta else 7
        pyxel.text(x, y, texto, cor)

    @staticmethod
    def rotulo(x, y, texto):
        pyxel.text(x, y, texto, 13)


class TelaInicial:
    def __init__(self):
        self.titulo_completo = "BEM VINDO AO GEO-STAR"
        self.titulo_atual = ""
        self.som_tocado = False
        
        # Gera estrelas de fundo fixas para a tela inicial
        self.estrelas_fundo = []
        for _ in range(50):
            self.estrelas_fundo.append({
                'x': random.randint(0, 400),
                'y': random.randint(0, 300),
                'cor': random.choice([7, 10, 6, 13]),
                'tamanho': random.choice([1, 1, 2])
            })
        self.instrucoes = """Instrucoes do Jogo:

O jogo tem como objetivo capturar estrelas no plano atraves da equacao da reta y= ax+b.

Para iniciar o jogo digite um valor para “a“ (coeficiente angular) e um valor para “b“ ( coeficiente 

linear ) afim de coletar uma das estrelas no plano, com base nesses valores a reta será projeta 

sobre o plano para realizar a coleta."""

    def update(self):
        if not self.som_tocado:
            pyxel.play(0, 0)
            self.som_tocado = True

        if len(self.titulo_atual) < len(self.titulo_completo):
            if pyxel.frame_count % 3 == 0:
                self.titulo_atual += self.titulo_completo[len(self.titulo_atual)]
        
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_KP_ENTER):
            if len(self.titulo_atual) < len(self.titulo_completo):
                self.titulo_atual = self.titulo_completo
            else:
                return "JOGANDO"
                
        return "TELA_INICIAL"

    def draw(self):
        pyxel.cls(0)
        
        
        # Desenha o céu estrelado de fundo (apenas pequenas)
        for est in self.estrelas_fundo:
            if est['tamanho'] == 2:
                pyxel.pset(est['x'], est['y'], est['cor'])
                if pyxel.frame_count % 30 < 15:
                    pyxel.pset(est['x'] + 1, est['y'], est['cor'])
            else:
                pyxel.pset(est['x'], est['y'], est['cor'])

        # Título centralizado com efeito de digitação (calculando X para centralizar com base no tamanho da fonte do Pyxel)
        x_titulo = 200 - (len(self.titulo_completo) * 2)
        Tipografia.titulo(x_titulo, 135, self.titulo_atual)
        
        
        # Aviso centralizado
        texto_aviso = "Pressione ENTER para iniciar"
        x_aviso = 200 - (len(texto_aviso) * 2)
        if len(self.titulo_atual) == len(self.titulo_completo):
            if (pyxel.frame_count // 10) % 2 == 0:
                Tipografia.aviso(x_aviso, 220, texto_aviso, False)
            pyxel.text(10, 150, self.instrucoes, 7)

            

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
        
        Tipografia.subtitulo(110, 122, f"Estrela em ({self.estrela.x}, {self.estrela.y}) capturada!")


class ModalFimJogo:
    def desenhar(self):
        for y in range(0, 300, 2):
            for x in range(0, 400, 2):
                pyxel.pset(x, y, 0)
                pyxel.pset(x + 1, y + 1, 0)
                
        pyxel.rect(134, 124, 140, 40, 0)
        pyxel.rect(130, 120, 140, 40, 0)
        pyxel.rectb(130, 120, 140, 40, 8)

        Tipografia.titulo(155, 132, "      FIM DE JOGO!")
        Tipografia.subtitulo(142, 144, "   Acabaram as tentativas")


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
        pyxel.recb(100, 110, 200, 60, 11)

        Tipografia.titulo(110, 118, "VOCÊ VENCEU!")
        Tipografia.subtitulo(110, 130, "Todas as estrelas foram coletadas!")
        Tipografia.subtitulo(110, 145, f"Estrelas capturadas: {self.total_estrelas}")
        Tipografia.subtitulo(110, 155, f"Tentativas restantes: {self.tentativas_restantes}")


class Estrela:
    def __init__(self, x, y, largura, altura, cor, sprite_x, sprite_y):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura

        self.sprite_x = sprite_x
        self.sprite_y = sprite_y

        self.cor = cor
        self.coletada = False

    def desenhar(self):
        if not self.coletada:
            tela_x, tela_y = self.converter_coordenada()
            pyxel.tri(tela_x, tela_y - 9,
                      tela_x + 5, tela_y + 2,
                      tela_x - 5, tela_y + 2, 10)

            pyxel.tri(tela_x + 9, tela_y,
                      tela_x - 2, tela_y + 5,
                      tela_x - 2, tela_y - 5, 10)

            pyxel.tri(tela_x, tela_y + 9,
                      tela_x + 5, tela_y - 2,
                      tela_x - 5, tela_y - 2, 10)

            pyxel.tri(tela_x - 9, tela_y,
                      tela_x + 2, tela_y + 5,
                      tela_x + 2, tela_y - 5, 10)

            pyxel.circ(tela_x, tela_y, 4, 7)

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
    #Verificar tds as estrelas quando encontrar ele coleta.
    def coletar_estrelas(self, estrelas):
        for estrela in estrelas:
            if self.pass_por(estrela):
                estrela.coletada = True

    def desenhar(self):
        anterior_x = None
        anterior_y = None

        for x in range(-10, 11):
            y = self.calcular_y(x)

            tela_x = 250 + (x) * 20
            tela_y = 170 - (y) * 20

            if anterior_x is not None:
                pyxel.line(anterior_x, anterior_y, tela_x, tela_y, 8)

            anterior_x = tela_x
            anterior_y = tela_y


class Plano:
    def __init__(self):
        pyxel.mouse(True)

    def desenhar(self):
        pyxel.rect(0, 0, 100, 300, 3)
        pyxel.line(100, 0, 100, 300, 1)
        #Linhas verticais que cortam o plano
        for x in range(-7, 8):
            tela_x = 250 + x * 20
            #Desenha a linha somente dentro da área do plano
            if tela_x >= 100:
                pyxel.line(tela_x, 40, tela_x, 300, 1)
        #Linhas horizontais que cortam o plano
        for y in range(-6, 7):
            tela_y = 170 - y * 20
            #Linha que atravessa toda a área do plano
            pyxel.line(100, tela_y, 400, tela_y, 1)
            
        pyxel.line(100, 170, 400, 170, 7)
        pyxel.line(250, 40, 250, 300, 7)
            
        for x in range(-7, 8):
            if x != 0:
                tela_x = 250 + x * 20
                Tipografia.rotulo(tela_x, 174, str(x))
        
        Tipografia.subtitulo(245, 174, '0')
        
        for y in range(-6, 7):
            if y != 0:
                tela_y = 170 - y * 20
                Tipografia.aviso(254, tela_y, str(y))
        
        mouse_tela_x = pyxel.mouse_x
        mouse_tela_y = pyxel.mouse_y
        
        centro_grade_x = 250
        centro_grade_y = 170
        
        cartesian_x = round((mouse_tela_x - centro_grade_x) / 20)
        cartesian_y = round((centro_grade_y - mouse_tela_y) / 20)
        
        texto_coordenadas = f"X: {cartesian_x}, Y: {cartesian_y}"
        
        if mouse_tela_x > 80 and mouse_tela_y > 20:
            Tipografia.subtitulo(mouse_tela_x + 10, mouse_tela_y + 10, texto_coordenadas)


class Jogo:
    def __init__(self):
        pyxel.init(400, 300, title="GeoStar - Desafio das Retas")

        self.estado = "TELA_INICIAL"
        self.tela_inicial = TelaInicial()
        
        pyxel.sounds[0].set("c3c3c3c3c3c4c2c3", "s", "5", "f", 15)
        pyxel.sounds[1].set("c2", "p", "7", "n", 3)        
        pyxel.sounds[2].set("c3", "s", "5", "f", 12)
        pyxel.sounds[3].set("g3f3d3c3a2", "t", "7", "f", 12)    
        pyxel.sounds[4].set("c3g3c4e4g4c4", "p", "7", "n", 6)

        self.som_inicio_tocado = False  
        
        self.texto_1 = ""  
        self.texto_2 = ""  
        self.foco_input = "a"
        self.mudou_valores = False
        
        self.modal = None
        self.mostrar_modal = False
        self.modal_timer = 0  
        
        self.plano = Plano()
        self.reta1 = None 
        
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
            sprite_x = random.choice([0, 16, 32, 48, 64])
            sprite_y = 0
            estrela = Estrela(x, y, 14, 18, 7, sprite_x, sprite_y)
            self.estrelas.append(estrela)
            posicoes.append((x, y))

        pyxel.run(self.update, self.draw)

    def iniciar_jogo(self): # Inicia o jogo com todas as variáveis resetadas
        self.estado = "JOGANDO"

        self.jogo_encerrado = False
        self.jogo_vencido = False

        self.modal_fim = None
        self.modal_vitoria = None
        self.modal = None
        self.mostrar_modal = False

        self.fim_timer = 0
        self.vitoria_timer = 0
        self.modal_timer = 0

        self.texto_1 = ""
        self.texto_2 = ""
        self.foco_input = "a"
        self.mudou_valores = False

        self.reta1 = None

        self.quant_estrelas = random.randint(4, 8)
        self.tentativas_restantes = self.quant_estrelas * 2

        self.estrelas = []
        posicoes = []

        for i in range(self.quant_estrelas):
            x = random.randint(-7, 7)
            y = random.randint(-6, 6)

            while (x, y) in posicoes:
                x = random.randint(-7, 7)
                y = random.randint(-6, 6)

            sprite_x = random.choice([0, 16, 32, 48, 64])
            sprite_y = 0

            estrela = Estrela(x, y, 14, 18, 7, sprite_x, sprite_y)

            self.estrelas.append(estrela)
            posicoes.append((x, y))
    def converter_numero(self, texto):
        texto = texto.strip()

        if "/" in texto:
            partes = texto.split("/") 

            if len(partes) != 2:
                raise ValueError

            numerador = float(partes[0])
            denominador = float(partes[1])

            if denominador == 0:
                raise ValueError

            return numerador / denominador

        return float(texto)
    
    def update(self):
        if self.estado == "TELA_INICIAL":
            proximo_estado = self.tela_inicial.update()
            if proximo_estado == "JOGANDO":
                self.iniciar_jogo()

        if self.estado == "JOGANDO" and not self.som_inicio_tocado:
            pyxel.play(0, 1)  
            self.som_inicio_tocado = True

        if self.mostrar_modal:
            self.modal_timer -= 1    
            if self.modal_timer <= 0:
                self.mostrar_modal = False 
            return 
        
        if self.jogo_vencido:
            self.vitoria_timer -= 1

            if self.vitoria_timer <= 0:
                self.estado = "TELA_INICIAL"
                self.jogo_vencido = False
                self.modal_vitoria = None
                self.tela_inicial = TelaInicial()

            return
        
        if self.jogo_encerrado:
            self.fim_timer -= 1

            if self.fim_timer <= 0:
                self.estado = "TELA_INICIAL"
                self.jogo_encerrado = False
                self.modal_fim = None
                self.tela_inicial = TelaInicial()

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

        
        # Troca de input usando as setas do teclado
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_DOWN):
            if self.foco_input == "a":
                self.foco_input = "b"
            else:
                self.foco_input = "a"
                
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_KP_ENTER):
            if self.mudou_valores:
                try:
                    if self.texto_1 in ("", "-"): self.texto_1 = "0"
                    if self.texto_2 in ("", "-"): self.texto_2 = "0"
                    
                    a = self.converter_numero(self.texto_1)
                    b = self.converter_numero(self.texto_2)
                    self.reta1 = Reta(a, b)
                    
                    pegou_estrela = self.verificar_todas_colisoes()
                    
                    if all(e.coletada for e in self.estrelas):
                        self.jogo_vencido = True
                        self.modal_vitoria = ModalVitoria(self.quant_estrelas, self.tentativas_restantes)
                        self.vitoria_timer = 180  
                        pyxel.play(0, 4)  
                    
                    if not pegou_estrela and not self.jogo_vencido:
                        self.tentativas_restantes -= 1
                        pyxel.play(0, 3)  
                        
                        if self.tentativas_restantes <= 0:
                            self.jogo_encerrado = True
                            self.modal_fim = ModalFimJogo()  
                            self.fim_timer = 180  
                            pyxel.play(0, 3)  

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
                    pyxel.play(0, 2)  
                    print(f"⭐ Estrela na coordenada ({estrela.x}, {estrela.y}) capturada!")
                    
        return colidiu_agora

    def draw(self):
        pyxel.cls(0)
        
        if self.estado == "TELA_INICIAL":
            self.tela_inicial.draw()
            return
        
        self.plano.desenhar()
        if self.reta1 is not None: 
            self.reta1.desenhar()
        
        for estrela in self.estrelas:
            estrela.desenhar()

        pyxel.text(34, 20, 'GEOSTAR', 7)
        pyxel.text(221, 20, 'PLANO CARTESIANO', 7)
        pyxel.text(13, 40, 'Desafio das Retas', 7)
        
        alerta_tentativas = self.tentativas_restantes <= 2
        Tipografia.aviso(10, 150, f"Tentativas: {self.tentativas_restantes}", alerta_tentativas)
        
        Tipografia.subtitulo(10, 70, "Valor de 'a':")
        cor_borda_a = 11 if self.foco_input == "a" else 5  
        pyxel.rectb(8, 81, 70, 20, cor_borda_a)
        
        Tipografia.subtitulo(10, 110, "Valor de 'b':")
        cor_borda_b = 11 if self.foco_input == "b" else 5  
        pyxel.rectb(8, 120, 70, 20, cor_borda_a)
        
        cursor = "_" if pyxel.frame_count % 30 < 15 else ""
        
        Tipografia.subtitulo(14, 89, self.texto_1 + (cursor if self.foco_input == "a" else ""))
        Tipografia.subtitulo(14, 129, self.texto_2 + (cursor if self.foco_input == "b" else ""))
        
        pyxel.mouse(True)
        
        if self.mostrar_modal and self.modal is not None:
            self.modal.desenhar()
        
        if self.jogo_encerrado and self.modal_fim is not None:
            self.modal_fim.desenhar()
            
        if self.jogo_vencido and self.modal_vitoria is not None:
            self.modal_vitoria.desenhar()
         
Jogo()
