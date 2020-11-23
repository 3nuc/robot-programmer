from enum import Enum
from typing import Callable, List, Dict, Tuple
import functools
'''
PS 10 Robot Programmer

Projekt polega na stworzeniu programu, który umożliwia zaprogramowanie robota. Użytkownik może za pomocą programu wyklikać trasę przejazdu robota. Następnie po kliknięciu przycisku generate tworzony jest kod programu, który ma kontrolować robota. Program powinien odtworzyć wszystkie ruchy zaprogramowane przez użytkownika. Kod musi być wygenerowany w języku NXC (zapisany jako plik lub przedstawiony w polu tekstowym). Tak zapisany program należy skompilować za pomocą Bicx Command Center i uruchomić na robocie. W trakcie jazdy robota nie powinno być żadnej komunikacji z komputerem.
Wersja minimum: Zapamiętanie wyklikanej trasy i wygenerowanie poprawnego kodu.
Wymagania na maksymalną ocenie:

    Ustawienia robota (porty silników, kierunek jazdy, odległość jednego kroku na bazie średnicy kół robota, rozstaw kół do wykonania dowolnego skrętu).
    Aktualna pozycja robota - jest to wizualizacja pozycji podczas programowania. Jeżeli klikniemy, żeby robot jechał do przodu, na wizualizacji powinien też się przesunąć do przodu.
'''

POWER = 50
LEFT_WHEEL_ENGINE_OUT = "A"
RIGHT_WHEEL_ENGINE_OUT = "C"

class NxcGenerator:
  def __init__(self, power: int, left_out_letter: str, right_out_letter: str):
    allowed_ports = ["A", "B", "C"]
    assert left_out_letter in allowed_ports and right_out_letter in allowed_ports
    self.power = power
    self.left_out="OUT_{}".format(left_out_letter)
    self.right_out="OUT_{}".format(right_out_letter)
    self.both_out="OUT_{}{}".format(left_out_letter, right_out_letter)

  """Go forward"""
  def createForward(self, time: int):
    return self.__createFwd(time, polarity=1)

  """Go back"""
  def createReverse(self, time: int):
    return self.__createFwd(time, polarity=-1)

  def createLeft(self, degrees: int):
    return self.__createRotateEngine(self.left_out, degrees)

  """Go right"""
  def createRight(self, degrees: int):
    return self.__createRotateEngine(self.right_out, degrees)

  def __createRotateEngine(self, port_letter: str, degrees: int) -> str:
   assert port_letter == self.left_out or port_letter == self.right_out
   return "RotateMotor({port_letter}, {power}, {degrees});\n".format(port_letter=port_letter, power=self.power, degrees=degrees)

  def __createFwd(self, time: int, polarity: int) -> str:
   assert polarity == 1 or polarity == -1
   return "OnFwd({out}, {power});\nWait({time});\n".format(out=self.both_out, power=self.power*polarity, time=time)


gen = NxcGenerator(POWER, left_out_letter=LEFT_WHEEL_ENGINE_OUT, right_out_letter=RIGHT_WHEEL_ENGINE_OUT)

def test():
  print(gen.createLeft(50))
  print(gen.createRight(50))
  print(gen.createForward(50))
  print(gen.createReverse(50))


class MOVES(Enum):
  ROTATE_LEFT = 0
  ROTATE_RIGHT = 1
  MOVE_FORWARD = 2
  MOVE_REVERSE = 3
  WAIT = 4

class NxcMapper:
  def __init__(self, nxcGenerator: NxcGenerator):
    self.nxcGenerator = nxcGenerator
  
  def generate(self, commands: List[Tuple[MOVES, int]]):
    return functools.reduce(self.__reducer, commands)


  def __reducer(self, acc: str, move: Tuple[MOVES, int]) -> str:
    el_mapperino : Dict[MOVES, Callable[[int], str]] = {
      MOVES.ROTATE_LEFT: self.nxcGenerator.createLeft,
      MOVES.ROTATE_RIGHT: self.nxcGenerator.createRight,
      MOVES.MOVE_FORWARD: self.nxcGenerator.createForward,
      MOVES.MOVE_REVERSE: self.nxcGenerator.createReverse,
    }
    
    func = el_mapperino[move[0]](move[1])
    
    return acc + func