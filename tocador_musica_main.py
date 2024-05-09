from tocador_musica_controller import Controller
from tocador_musica_model import Model
from tocador_musica_view import View

if __name__ == '__main__':
    '''Função principal, instância instâncias de Model, View e Controller'''
        
    tocador_musica_model = Model()
    tocador_musica_view = View()
    tocador_musica_controller = Controller(model=tocador_musica_model, view=tocador_musica_view)
    tocador_musica_view.view_main()
    tocador_musica_controller.run()