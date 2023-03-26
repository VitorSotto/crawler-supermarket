from abc import ABC, abstractmethod

class Mercado(ABC):
  def __init__(self, searchProduct, browser):
    self.searchProduct = searchProduct
    self.browser = browser
    
  
  @abstractmethod
  def processa(self):
    pass