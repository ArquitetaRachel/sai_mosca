import pgzrun
import random

# Configurações básicas
WIDTH = 800
HEIGHT = 600

# Estados do jogo
MENU = 0
JOGANDO = 1
GAME_OVER = 2
WIN = 3
estado = MENU
som_ativo = True

life = 3
pontuacao = 0

# Definição do jogador com classe
class Player(Actor):
    def __init__(self, imagem, posicao):
        super().__init__(imagem, posicao)
        self.velocidade = 5
        self.moving_left = False
        self.moving_right = False
        self.frame = 0  # Variável para controlar o quadro da animação
        self.movement_timer = 0  # Timer para controlar a animação de movimento
        self.vel_y = 0  # Velocidade do pulo
        self.no_chao = True  # Para verificar se o jogador está no chão

    def update(self):
        if self.moving_left and self.x > 50:
            self.x -= self.velocidade
            self.change_image_left()  # Chama a função para alterar a imagem para a esquerda
        elif self.moving_right and self.x < WIDTH - 50:
            self.x += self.velocidade
            self.change_image_right()  # Chama a função para alterar a imagem para a direita

        # A cada atualização, aumentamos o timer, e a cada 200 ms trocamos a imagem
        self.movement_timer += 1
        if self.movement_timer > 10:  # Troca a imagem a cada 10 ciclos
            self.frame += 1
            self.movement_timer = 0

        # Lógica de pulo
        if not self.no_chao:
            self.vel_y += 1  # Gravidade
            self.y += self.vel_y
        if self.y >= HEIGHT - 50:
            self.y = HEIGHT - 50  # Impede o jogador de passar do chão
            self.no_chao = True
            self.vel_y = 0

    def change_image_left(self):
        if self.frame % 2 == 0:  # Altera a imagem a cada 2 quadros
            self.image = "alien_green_walk1_left"  # Primeira imagem andando para a esquerda
        else:
            self.image = "alien_green_walk2_left"  # Segunda imagem andando para a esquerda

    def change_image_right(self):
        if self.frame % 2 == 0:  # Altera a imagem a cada 2 quadros
            self.image = "alien_green_walk1_right"  # Primeira imagem andando para a direita
        else:
            self.image = "alien_green_walk2_right"  # Segunda imagem andando para a direita

    def move_left(self):
        self.moving_left = True

    def move_right(self):
        self.moving_right = True

    def stop_left(self):
        self.moving_left = False
        self.image = "alien_green_front"  # Quando parar, mantém uma imagem fixa

    def stop_right(self):
        self.moving_right = False
        self.image = "alien_green_front"  # Quando parar, mantém uma imagem fixa

    def jump(self):
        if self.no_chao:  # Permite pular apenas se estiver no chão
            self.vel_y = -15  # Velocidade inicial do pulo
            self.no_chao = False

# Definição do inimigo com classe
class Enemy(Actor):
    def __init__(self, imagem, posicao):
        super().__init__(imagem, posicao)
        self.velocidade = 2
        self.animation_time = 0  # Tempo para alternar as imagens
        self.animation_delay = 0.5  # Delay de animação (meia segundo entre as trocas)

    def update(self, dt):  # 'dt' é passado automaticamente
        self.y += self.velocidade
        self.animation_time += dt  # Atualizando o tempo de animação

        # Alternando entre as imagens "fly" e "fly_move"
        if self.animation_time > self.animation_delay:
            self.animation_time = 0  # Resetando o contador de tempo
            if self.image == "fly":  # Se a imagem atual for "fly", muda para "fly_move"
                self.image = "fly_move"
            else:  # Se a imagem atual for "fly_move", muda para "fly"
                self.image = "fly"
        
        if self.y > HEIGHT:
            self.y = 50
            self.x = random.randint(50, WIDTH - 50)

# Criando uma lista para armazenar vários inimigos
enemies = []

# Criando múltiplos inimigos com posições aleatórias
for _ in range(5):  # Altere o número para mais ou menos inimigos
    new_enemy = Enemy("fly", (random.randint(50, WIDTH - 50), random.randint(-300, -50)))
    enemies.append(new_enemy)
# Instâncias dos objetos
player = Player("alien_green_front", (WIDTH // 2, HEIGHT - 50))
player.scale = 0.5
enemy = Enemy("fly", (random.randint(50, WIDTH - 50), 50))

# Botões do menu
botao_jogar = Rect(300, 250, 200, 50)
botao_sair = Rect(300, 320, 200, 50)
botao_som = Rect(300, 390, 200, 50)

# Função de desenho do menu
def desenhar_menu():
    screen.clear()
    screen.draw.text("Jogo Simples", center=(WIDTH // 2, 150), fontsize=50, color="white")
    screen.draw.filled_rect(botao_jogar, "blue")
    screen.draw.filled_rect(botao_sair, "red")
    screen.draw.text("Jogar", center=botao_jogar.center, fontsize=30, color="white")
    screen.draw.text("Sair", center=botao_sair.center, fontsize=30, color="white")

    # Botão para alternar o som
    screen.draw.filled_rect(botao_som, "green" if som_ativo else "gray")
    screen.draw.text("Som: " + ("ON" if som_ativo else "OFF"), center=botao_som.center, fontsize=30, color="white")

    screen.draw.text("Sound Effect by Gaston A-P from Pixabay", center=(WIDTH // 2, HEIGHT - 30), fontsize=20, color="white")


# Função para alternar o som
def alternar_som():
    global som_ativo
    if som_ativo:
        sounds.music.stop()  # Para a música
        som_ativo = False
    else:
        sounds.music.play(loops=True)
        sounds.music.set_volume(0.15)
        som_ativo = True
        
# Adicionando a imagem do coração
heart = Actor("hud_heart_full")  # Substitua "heart" pelo nome da sua imagem de coração, como "heart.png"
heart.scale = 0.1  # Ajuste o tamanho, se necessário

# Função de desenho do jogo
def desenhar_jogo():
    screen.clear()
    screen.blit("colored_shroom", (0, 0))
    player.draw()
    
    for enemy in enemies:
        enemy.draw()
    
    # Exibir vidas como corações 
    for i in range(life):  # Aqui mostramos a quantidade de corações de acordo com a vida
        heart.x = 50 + i * 50  # Ajuste a posição para os corações não se sobreporem
        heart.y = 30  # Posição vertical
        heart.draw()  # Desenha o coração

    # Exibir a pontuação
    screen.draw.text(f"Pontuação: {pontuacao}", (WIDTH - 150, 30), fontsize=30, color="black")

# Função de game over
def desenhar_game_over():
    screen.clear()
    screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="red")
    screen.draw.text("Clique para voltar ao menu", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=30, color="white")
    

# Função de vitória
def desenhar_win():
    screen.clear()
    screen.draw.text("VOCÊ VENCEU!", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="green")
    screen.draw.text("Clique para voltar ao menu", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=30, color="white")


# Atualização do jogo
def update(dt):  # Agora 'dt' é passado automaticamente para o método update de cada objeto
    global estado, life, pontuacao, som_ativo

    if estado == JOGANDO:
        player.update()

        for enemy in enemies:
            enemy.update(dt)  # Passando o 'dt' corretamente
            
            # Verifica se o inimigo colidiu com o jogador
            if player.colliderect(enemy):
                life -= 1
                enemy.y = random.randint(-300, -50)  # Reposiciona o inimigo no topo
                enemy.x = random.randint(50, WIDTH - 50)  # Nova posição aleatória
                
                if life == 0:
                    estado = GAME_OVER

            # Verifica se o inimigo chegou ao final da tela
            if enemy.y > HEIGHT-50:
                enemy.y = random.randint(-300, -50)  # Reposiciona no topo
                enemy.x = random.randint(50, WIDTH - 50)  # Nova posição aleatória

                # Se o inimigo passar pela tela, adiciona um ponto
                pontuacao += 1

        # Verifica se a pontuação chegou a 20, então vence o jogo
        if pontuacao >= 20:
            estado = WIN

def reiniciar_jogo():
    global life, estado, player, enemies, pontuacao, som_ativo

    life = 3  # Resetando a vida
    estado = JOGANDO  # Voltando ao estado inicial
    pontuacao = 0  # Resetando a pontuação

    # Resetando o jogador
    player.x = WIDTH // 2
    player.y = HEIGHT - 50
    player.vel_y = 0
    player.no_chao = True

    # Resetando os inimigos
    for enemy in enemies:
        enemy.x = random.randint(50, WIDTH - 50)
        enemy.y = random.randint(-300, -50)  # Para começarem de diferentes alturas


# Movimentação do jogador
def on_key_down(key):
    if estado == JOGANDO:
        if key == keys.LEFT or key == keys.A:
            player.move_left()
        if key == keys.RIGHT or key == keys.D:
            player.move_right()
        if key == keys.SPACE or key == keys.W:
            player.jump()

def on_key_up(key):
    if estado == JOGANDO:
        if key == keys.LEFT or key == keys.A:
            player.stop_left()
        if key == keys.RIGHT or key == keys.D:
            player.stop_right()

# Função de clique do mouse (Menu)
def on_mouse_down(pos):
    global estado, som_ativo
    if estado == MENU:
        if botao_jogar.collidepoint(pos):
            sounds.music.stop()
            if som_ativo:
                sounds.music.play(loops=True)
                sounds.music.set_volume(0.15)
            reiniciar_jogo()  # Inicia um novo jogo corretamente
        elif botao_sair.collidepoint(pos):
            exit()
        elif botao_som.collidepoint(pos):  # Verifica se o clique foi no botão de som
            sounds.music.stop()
            alternar_som()  # Alterna o som
    elif estado == GAME_OVER or estado == WIN:
        estado = MENU  # Volta para o menu
        sounds.music.stop()
        

# Função de desenho
def draw():
    if estado == MENU:
        desenhar_menu()
    elif estado == JOGANDO:
        desenhar_jogo()
    elif estado == GAME_OVER:
        desenhar_game_over()
    elif estado == WIN:
        desenhar_win()

pgzrun.go()
