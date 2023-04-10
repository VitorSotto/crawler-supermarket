from abc import ABC, abstractmethod

class Mercado(ABC):
  def __init__(self, searchProducts, browser):
    self.searchProducts = searchProducts
    self.browser = browser
    
  
  @abstractmethod
  def processa(self):
    pass