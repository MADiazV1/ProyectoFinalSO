import threading

class RendezvousDEchange:
    def __init__(self):
        self.condition = threading.Condition()
        self.waiting = False
        self.first_value = None
        self.second_value = None

    def echanger(self, value):
        with self.condition:
            if not self.waiting:
                # Primer hilo llega y espera al segundo
                self.first_value = value
                self.waiting = True
                self.condition.wait()
                result = self.second_value
                self.condition.notify()
                return result
            else:
                # Segundo hilo llega
                self.second_value = value
                self.condition.notify()  # Despierta al primer hilo
                self.condition.wait()   # Espera que el primer hilo lea second_value
                result = self.first_value
                self.first_value = None
                self.second_value = None
                self.waiting = False
                return result