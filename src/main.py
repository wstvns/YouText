from yt_dlp import YoutubeDL
import whisper
import os
import static_ffmpeg

def downloadVideo(url):
    # Configuracoes para baixar o video e extrair o audio diretamente em MP3
    ydl_opts = {
        'format': 'bestaudio/best',  # Melhor qualidade de audio disponivel
        'outtmpl': '%(title)s.%(ext)s',  # Nome do arquivo de saida
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Extrai o audio
            'preferredcodec': 'mp3',  # Converte para MP3
            'preferredquality': '192',  # Qualidade do audio
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        # Retorna o nome do arquivo MP3 gerado
        return info_dict.get('title', 'video') + '.mp3'

def AudiotoText(filename):
    # Carrega o Whisper e transcreve o audio
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    print("Texto transcrito:")
    print(result["text"])
    return result["text"]

def main():
    print('''
    Essa ferramenta converte videos do YouTube para arquivos mp3 e, em seguida, os transcreve para texto usando o Whisper.
    ''')
    
    # Input do link do YouTube
    link = input("Por favor, insira o link do vídeo do YouTube: ")
    print("URL: " + link)
    
    # Solicita o modelo Whisper a ser usado
    model = input("Por favor, insira o modelo Whisper a ser usado (ex: 'base', 'small', 'medium', 'large'): ")
    print("MODEL: " + model)
    
    # Inicializa o FFMPEG
    print("Iniciando FFMPEG...")
    static_ffmpeg.add_paths()

    # Baixa o video e converte para MP3
    print("Baixando video e convertendo para MP3... Aguarde.")
    try:
        filename = downloadVideo(link)
        print(f"Pronto! Video convertido para MP3: {filename}")
    except Exception as e:
        print("Erro ao baixar ou converter o video:", e)
        return

    # Transcreve o audio para texto
    try:
        mymodel = whisper.load_model(model)
        print("Transcrevendo audio para texto... Isso pode demorar um pouco.")
        result = mymodel.transcribe(filename)
        print("Texto transcrito:")
        print(result["text"])



        # Remove o arquivo de audio apos a transcricao
        os.remove(filename)
        print(f"Arquivo de audio removido: {filename}")
        print("Processo concluído com sucesso!")
        return result["text"]
    except Exception as e:
        print("Erro ao transcrever audio para texto:", e)
        return

if __name__ == "__main__":
    main()