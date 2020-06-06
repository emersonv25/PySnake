'''

@author emersonv25
github.com/emersonv25

'''


from random import randint
import pygame

# ------------ Váriaveis Globais ------------
width = 400
height = 400
size = (width, height)
# cores
branco = (255, 255, 255)
azul = (0, 200, 255)
verde = (0, 255, 0)
preto = (0, 0, 0)
vermelho = (255, 0, 0)

# Inicializando o PYGAME
pygame.init()

# Configurações GLOBAIS de tela
tela = pygame.display.set_mode(size)
pygame.display.set_caption('Snake by emersonv25')
frames = pygame.time.Clock()
pontos = 0
GameOver = False


# ----------- Funções --------------
def game_menu():
    global pontos, GameOver
    # Loop de execução do menu
    while True:
        # recebe todos os eventos do pygame na tela
        for event in pygame.event.get():

            # ---------- IF's de Verificação de Eventos ---------------

            # Evento de fechar a tela
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()

        if GameOver:
            fonte = pygame.font.Font(None, 25)
            fonte2 = pygame.font.Font(None, 35)
            text = fonte.render('Pressione ENTER para Jogar Novamente', True, preto, branco)
            text2 = fonte2.render('GAME OVER', True, preto, branco)
            textRect = text.get_rect()
            textRect2 = text2.get_rect()
            textRect2.center = (width // 2, height // 2 - 100)
            textRect.center = (width // 2, height // 2)
            tela.blit(text, textRect)
            tela.blit(text2, textRect2)



        else:
            tela.fill(branco)
            fonte = pygame.font.Font(None, 25)
            text = fonte.render('Pressione ENTER para Jogar', True, preto, branco)
            textRect = text.get_rect()
            textRect.center = (width // 2, height // 2)
            tela.blit(text, textRect)

        pygame.display.update()
        frames.tick(10)


def pos_aleatoria():
    x = randint(10, width-10)
    y = randint(10, height-10)
    return x // 10 * 10, y // 10 * 10


def colisao(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])


def main():

    global pontos, GameOver
    pontos = 0

    # Variáveis de movimento
    UP = 'cima'
    DOWN = 'baixo'
    LEFT = 'esquerda'
    RIGHT = 'direita'

    # Cria a cobre e maça
    snake = [(150, 150), (160, 150), (170, 150), (180, 150)]
    snake_corpo = pygame.Surface((10, 10))
    snake_corpo.fill(verde)
    apple_pos = pos_aleatoria()
    apple = pygame.Surface((10, 10))
    apple.fill(vermelho)

    # Bordas da tela
    bordaTamanho = 10
    bordaCima = pygame.Surface((width, bordaTamanho))
    bordaBaixo = pygame.Surface((width, bordaTamanho))
    bordaEsquerda = pygame.Surface((bordaTamanho, height))
    bordaDireita = pygame.Surface((bordaTamanho, height))
    bordaCima.fill(azul)
    bordaBaixo.fill(azul)
    bordaEsquerda.fill(azul)
    bordaDireita.fill(azul)


    # Cria uma direção inicial para a cobra
    snake_direcao = RIGHT

    # Textos
    pygame.font.init()
    fonte = pygame.font.Font(None, 25)
    text = fonte.render('Pontuação: ' + str(pontos), True, preto)
    textRect = text.get_rect()
    textRect.center = (width // 2, 20)

    # Loop de execução do game
    while True:
        # recebe todos os eventos do pygame na tela
        for event in pygame.event.get():

            # ---------- IF's de Verificação de Eventos ---------------

            # Evento de fechar a tela
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Controles
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and RIGHT != snake_direcao:
                    snake_direcao = LEFT
                if event.key == pygame.K_RIGHT and LEFT != snake_direcao:
                    snake_direcao = RIGHT
                if event.key == pygame.K_UP and DOWN != snake_direcao:
                    snake_direcao = UP
                if event.key == pygame.K_DOWN and UP != snake_direcao:
                    snake_direcao = DOWN

        # Colisão com a Maça
        if colisao(snake[0], apple_pos):
            apple_pos = pos_aleatoria()
            snake.append((0, 0))
            pontos += 1
            text = fonte.render('Pontuação: ' + str(pontos), True, preto, branco)

        # Colisão com o rabo
        for i in range(3, len(snake)):
            if colisao(snake[0], snake[i]):
                GameOver = True
                game_menu()

        # colisão com a borda
        if snake[0][0] == 0 or snake[0][0] == width-bordaTamanho or snake[0][1] == height-bordaTamanho \
                or snake[0][1] == 0:
            GameOver = True
            game_menu()


        # Puxa o resto do corpo da cobra junto com a cabeça
        for posicao in range(len(snake) - 1, 0, -1):
            snake[posicao] = (snake[posicao - 1][0], snake[posicao - 1][1])

        # Direção da snake
        if snake_direcao == UP:
            snake[0] = (snake[0][0], snake[0][1] - 10)
        if snake_direcao == DOWN:
            snake[0] = (snake[0][0], snake[0][1] + 10)
        if snake_direcao == RIGHT:
            snake[0] = (snake[0][0] + 10, snake[0][1])
        if snake_direcao == LEFT:
            snake[0] = (snake[0][0] - 10, snake[0][1])

        # Taxa de Atualização da Tela
        frames.tick(10+(pontos/10))

        # Definição de Cores da superficie e tela
        tela.fill(branco)

        #  Inserindo/Desenhando Objetos na tela [Posição]
        tela.blit(text, textRect)
        # desenha o corpo da snake na tela
        for posicao in snake:
            tela.blit(snake_corpo, posicao)

        # desenha a maça na tela
        tela.blit(apple, apple_pos)

        # Desenha a borda da tela

        tela.blit(bordaCima, (0, 0))
        tela.blit(bordaBaixo, (0, height-10))
        tela.blit(bordaEsquerda, (0, 0))
        tela.blit(bordaDireita, (width-10, 0))

        pygame.display.update()

    pygame.quit()


game_menu()
