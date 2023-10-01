# Import de bibliotecas
import flet as ft

def main(pagina):
    # ft.Text() cria um texto
    texto = ft.Text('Bem vindo ao chat!')

    chat = ft.Column()

    nome_usuario = ft.TextField(label='Escreva seu nome!')

    # Função de enviar mensagem as outras pessoas na conversa
    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem['tipo']
        if tipo == 'mensagem':
            texto_mensagem = mensagem['texto']
            usuario_mensagem = mensagem['usuario']
        # Adicionar mensagem no chat
            chat.controls.append(ft.Text(f'{usuario_mensagem}: {texto_mensagem}'))
        else:
            usuario_mensagem = mensagem['usuario']
            chat.controls.append(ft.Text(f'{usuario_mensagem} entrou no chat.', size=12, italic=True, color=ft.colors.BLUE_600))
        pagina.update()

    # Função que permite um usuario de comunicar com outro
    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    # Função que conecta o envio de mensagem com o tunel de mensagens
    def enviar_mensagem(evento):
        pagina.pubsub.send_all({'texto': campo_mensagem.value, 'usuario': nome_usuario.value, 'tipo': 'mensagem'})
        # Limpar o campo de mensagem
        campo_mensagem.value = ''
        pagina.update()

    campo_mensagem = ft.TextField(label='Digite sua mensagem!')
    botao_enviar_mensagem = ft.ElevatedButton('Enviar', on_click=enviar_mensagem)

    # Função que após digitar o nome de usuario, fecha o popup e entra na conversa
    def entrar_popup(evento):
        pagina.pubsub.send_all({'usuario': nome_usuario.value, 'tipo': 'entrada'})
        # Adicionar o chat
        pagina.add(chat)
        # Fechar o popup
        popup.open = False
        # Remover o botão de iniciar chat e o texto inicial
        pagina.remove(bota_iniciar)
        pagina.remove(texto)
        # Criar campo de mensagem e botão de enviar mensagem um do lado do outro
        pagina.add(ft.Row(
            [campo_mensagem, botao_enviar_mensagem]
        ))
        pagina.update()

    # Função que abre o popup para digitar o nome de usuario e entrar na conversa
    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text('Bem vindo!'),
        content=nome_usuario,
        actions=[ft.ElevatedButton('Entrar', on_click=entrar_popup)],
    )

    def entrar_chat(evento):
        pagina.dialog = popup
        popup.open = True
        pagina.update()

    # ft.ElevatedButton cria um botão
    bota_iniciar = ft.ElevatedButton('Iniciar chat', on_click=entrar_chat) # É possivel passar parametros para o ElevatedButton
    # Inclusive uma função no onclick

    # O .add adiciona o que foi criado na pagina
    pagina.add(texto)
    pagina.add(bota_iniciar)

ft.app(target=main, view=ft.WEB_BROWSER, port=8000) # O parametro view=ft.WEB_BROWSER permite visualizar o site em modo web browser