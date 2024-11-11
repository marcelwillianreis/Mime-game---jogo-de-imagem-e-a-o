import random 
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown  # Import para DropDown

# Configurar a janela em modo de tela cheia
Window.fullscreen = False

# Função para carregar as palavras do arquivo palavras.txt
def carregar_palavras():
    with open("palavras.txt", "r") as file:
        palavras = [linha.strip() for linha in file.readlines()]
    return palavras

# Tela de início
class InicioScreen(Screen):
    def __init__(self, **kwargs):
        super(InicioScreen, self).__init__(**kwargs)
        
        # Usando FloatLayout para colocar a imagem de fundo e os elementos por cima
        layout = FloatLayout()
        
        # Adiciona a imagem de fundo da tela inicial
        imagem_fundo = Image(source='imagens/imagem-tela-inicial.jfif', allow_stretch=True, keep_ratio=False)
        layout.add_widget(imagem_fundo)

        # Título do jogo
        label = Label(text='Palavra e Mímica', font_size='32sp', color=(0, 0, 0, 1), 
              size_hint=(0.8, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.7})

        # Botão para iniciar o jogo (mantendo o background_color)
        botao_iniciar = Button(text='Iniciar Jogo', on_press=self.iniciar_jogo, 
                        background_color=(1.0, 0.7, 1, 1), size_hint=(0.2, 0.1), 
                        pos_hint={'center_x': 0.5, 'center_y': 0.3})

        # Botão para selecionar o tempo do contador
        self.tempo_selecionado = 60  # Tempo padrão de 1 minuto
        self.botao_tempo = Button(text='Selecionar Tempo', size_hint=(0.2, 0.1), 
                                  pos_hint={'center_x': 0.5, 'center_y': 0.2})
        self.botao_tempo.bind(on_release=self.abrir_dropdown_tempo)

        # Criar o DropDown para seleção de tempo
        self.dropdown = DropDown()
        for tempo in [10, 20, 30, 40, 50, 60, 90, 120]:  # Opções de 10s até 2min
            btn = Button(text=f"{tempo} segundos", size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.selecionar_tempo(btn.text))
            self.dropdown.add_widget(btn)

        # Adiciona os widgets ao layout
        layout.add_widget(label)
        layout.add_widget(botao_iniciar)
        layout.add_widget(self.botao_tempo)
        
        self.add_widget(layout)

    def abrir_dropdown_tempo(self, instance):
        self.dropdown.open(instance)

    def selecionar_tempo(self, tempo_texto):
        # Converte a seleção para um número inteiro e atualiza o tempo selecionado
        self.tempo_selecionado = int(tempo_texto.split()[0])
        self.botao_tempo.text = f"Tempo: {self.tempo_selecionado}s"
        self.dropdown.dismiss()

    def iniciar_jogo(self, instance):
        # Passa o tempo selecionado para a tela do jogo
        self.manager.get_screen('jogo').set_tempo(self.tempo_selecionado)
        self.manager.current = 'jogo'

# Tela do jogo
class JogoScreen(Screen):
    def __init__(self, **kwargs):
        super(JogoScreen, self).__init__(**kwargs)
        self.equipe_a_pontos = 0
        self.equipe_b_pontos = 0
        self.palavras = carregar_palavras()
        self.temporizador = 60 # Tempo padrão de 1 minuto
        self.contagem = None
        self.palavra_gerada = False

        self.layout = FloatLayout()  # Usar FloatLayout como layout principal

        # Adiciona a imagem de fundo da tela de jogo
        imagem_fundo_jogo = Image(source='imagens/imagem-tela-jogo.jfif', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(imagem_fundo_jogo)

        # Área de Pontuação
        pontuacao_layout = GridLayout(cols=2, size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'top': 0.95})
        self.pontuacao_label_a = Label(text="Equipe A: 0", font_size='24sp', halign='center')
        self.pontuacao_label_b = Label(text="Equipe B: 0", font_size='24sp', halign='center')
        
        pontuacao_layout.add_widget(self.pontuacao_label_a)
        pontuacao_layout.add_widget(self.pontuacao_label_b)

        # Área de Botões de Pontuação
        botoes_pontuacao_layout = GridLayout(cols=2, size_hint=(0.8, 0.2), pos_hint={'center_x': 0.5, 'top': 0.85})
        self.botao_add_equipe_a = Button(text="Adicionar Ponto Equipe A", on_press=self.adicionar_ponto_equipe_a, background_color=(0, 0, 1, 1))
        self.botao_sub_equipe_a = Button(text="Retirar Ponto Equipe A", on_press=self.retirar_ponto_equipe_a, background_color=(1, 0, 0, 1))
        self.botao_sub_equipe_b = Button(text="Retirar Ponto Equipe B", on_press=self.retirar_ponto_equipe_b , background_color=(1, 0, 0, 1))
        self.botao_add_equipe_b = Button(text="Adicionar Ponto Equipe B", on_press=self.adicionar_ponto_equipe_b , background_color=(0, 0, 1, 1))

        botoes_pontuacao_layout.add_widget(self.botao_add_equipe_a)
        botoes_pontuacao_layout.add_widget(self.botao_add_equipe_b)
        botoes_pontuacao_layout.add_widget(self.botao_sub_equipe_a)
        botoes_pontuacao_layout.add_widget(self.botao_sub_equipe_b)

        # Área da parte de trás do parte de Palavra e Contador
        self.botao_fundo_auxiliar_palavra = Button(text="", background_color=(1, 1, 1, 2.5), disabled=True, size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'top': 0.6})
        self.layout.add_widget(self.botao_fundo_auxiliar_palavra)
        
        self.botao_fundo_auxiliar_tempo = Button(text="", background_color=(1, 1, 1, 2.5), disabled=True, size_hint=(0.3, 0.11), pos_hint={'center_x': 0.5, 'top': 0.45})
        self.layout.add_widget(self.botao_fundo_auxiliar_tempo)

        # Área de Palavra e Contador
        self.palavra_label = Label(text="Aguardando palavra...", font_size='50sp', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'top': 0.6}, color=(0, 1, 0, 1))
        self.tempo_label = Label(text="Tempo: 1:00", font_size='24sp', size_hint=(0.8, 0.4), pos_hint={'center_x': 0.5, 'top': 0.6},color=(0, 1, 0, 1))

        self.botao_gerar = Button(text="Gerar Palavra", on_press=self.gerar_palavra, background_color=(1, 0.85, 0, 1), size_hint=(0.2, 0.1), pos_hint={'center_x': 0.4, 'top': 0.3})
        self.botao_iniciar = Button(text="Iniciar Contador", on_press=self.iniciar_contador, background_color=(0.5, 0.5, 0.5, 1), disabled=True, size_hint=(0.2, 0.1), pos_hint={'center_x': 0.6, 'top': 0.3})
        self.botao_reiniciar = Button(text="Reiniciar Jogo", on_press=self.reiniciar_jogo, background_color=(1, 0.5, 0.5, 1), size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'top': 0.1})

        self.layout.add_widget(self.palavra_label)
        self.layout.add_widget(self.tempo_label)
        self.layout.add_widget(self.botao_gerar)
        self.layout.add_widget(self.botao_iniciar)
        self.layout.add_widget(self.botao_reiniciar)
        self.layout.add_widget(pontuacao_layout)
        self.layout.add_widget(botoes_pontuacao_layout)
        
        self.add_widget(self.layout)

    def set_tempo(self, tempo):
        self.temporizador = tempo
        self.tempo_label.text = f"Tempo: {self.temporizador}s"  # Atualiza o texto do tempo inicial


    def gerar_palavra(self, instance):
        if self.palavras:
            self.palavra_label.text = random.choice(self.palavras)
            self.botao_iniciar.disabled = False

    def iniciar_contador(self, instance):
        self.botao_iniciar.disabled = True
        self.segundos_restantes = self.temporizador
        self.tempo_label.text = f"Tempo: {self.segundos_restantes}s"
        self.contagem = Clock.schedule_interval(self.atualizar_contador, 1)

    def atualizar_contador(self, dt):
        self.segundos_restantes -= 1
        if self.segundos_restantes <= 0:
            self.tempo_label.text = "Tempo Esgotado!"
            Clock.unschedule(self.contagem)
        else:
            self.tempo_label.text = f"Tempo: {self.segundos_restantes}s"

    def adicionar_ponto_equipe_a(self, instance):
        self.equipe_a_pontos += 1
        self.pontuacao_label_a.text = f"Equipe A: {self.equipe_a_pontos}"

    def adicionar_ponto_equipe_b(self, instance):
        self.equipe_b_pontos += 1
        self.pontuacao_label_b.text = f"Equipe B: {self.equipe_b_pontos}"

    def retirar_ponto_equipe_a(self, instance):
        self.equipe_a_pontos = max(0, self.equipe_a_pontos - 1)
        self.pontuacao_label_a.text = f"Equipe A: {self.equipe_a_pontos}"

    def retirar_ponto_equipe_b(self, instance):
        self.equipe_b_pontos = max(0, self.equipe_b_pontos - 1)
        self.pontuacao_label_b.text = f"Equipe B: {self.equipe_b_pontos}"
    
    def reiniciar_jogo(self, instance):
        self.palavra_label.text = "Aguardando palavra..."
        self.equipe_a_pontos = 0
        self.equipe_b_pontos = 0
        self.pontuacao_label_a.text = f"Equipe A: {self.equipe_a_pontos}"
        self.pontuacao_label_b.text = f"Equipe B: {self.equipe_b_pontos}"
        self.botao_iniciar.disabled = True
        self.segundos_restantes = self.temporizador
        if self.contagem:
            Clock.unschedule(self.contagem)
        self.tempo_label.text = f"Tempo: {self.temporizador}s"
        self.manager.current = 'inicio'

class GerenciadorDeTelas(ScreenManager):
    def __init__(self, **kwargs):
        super(GerenciadorDeTelas, self).__init__(**kwargs)
        self.add_widget(InicioScreen(name='inicio'))
        self.add_widget(JogoScreen(name='jogo'))

class MeuApp(App):
    def build(self):
        return GerenciadorDeTelas()

if __name__ == '__main__':
    MeuApp().run()
