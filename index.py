import pyxel

class Reta:
  def __init__(self, a, b, c):
    self.a = a
    self.b = b
    self.c = c
  def draw(self):
    pyxel.react(self.a, self.b, self.c)

class GeoStart:
  def __init__(self):
    a=int(input("Digite valor em x"))
    b=int(input("Digite valor em y"))
    c=int(input("Digite valor em "))

    reta = Reta(a, b, c)

    #𝑎𝑥+𝑏𝑦+𝑐
    
    eq_reta = ((reta.self.a) * x) + ((reta.self.b) * y) + reta.self.c
    
    pyxel.run(self.draw)
