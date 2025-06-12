# Controla a pontuação do jogo
class Score:
    def __init__(self):
        self.score = 0

    def up_score(self):
        self.score += 1

# Lê o input das teclas de movimentação em string
class KeysPressed:
    def __init__(self, first_key):
        self.keys_pressed = [first_key]

    # Adiciona a última tecla de movimentação à lista
    def add_to_list(self, last_key):
        self.keys_pressed.append(last_key)

    # Limpa a lista, menos o último item, evitando uma lista muito grande
    def clean_list(self):
        for key in self.keys_pressed[:-1]:
            self.keys_pressed.remove(key)

    # Retorna a última tecla pressionada
    def get_last_key(self):
        return self.keys_pressed[-1]
