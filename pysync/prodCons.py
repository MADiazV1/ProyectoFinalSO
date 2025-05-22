import threading

class GenProdCons:
  def __init__(self, size=10):
    if size <= 0:
      raise ValueError("El tamaño debe ser mayor que 0")
    self.size = size
    self.buffer = [None] * size
    self.entrada = 0
    self.salida = 0
    self.count = 0

    self.mutex = threading.Lock()
    self.vacio = threading.Semaphore(size)
    self.full = threading.Semaphore(0)

  def put(self, item):
    self.vacio.acquire()
    with self.mutex:
      self.buffer[self.entrada] = item
      self.entrada = (self.entrada + 1) % self.size
      self.count += 1
    self.full.release()

  def get(self):
    self.full.acquire()
    with self.mutex:
      item = self.buffer[self.salida]
      self.salida = (self.salida + 1) % self.size
      self.count -= 1
    self.vacio.release()
    return item

  def __len__(self):
    with self.mutex:
      return self.count
