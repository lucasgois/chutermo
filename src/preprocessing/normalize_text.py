import unicodedata
import os
import re
import chardet

def detect_encoding(filepath):
    """
    Detecta automaticamente o encoding de um arquivo.
    """
    with open(filepath, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def normalize_and_lowercase(text):
    """
    Normaliza o texto:
    - Remove acentos e caracteres especiais
    - Remove números
    - Remove todos os caracteres que não sejam letras ou espaços
    - Converte para minúsculas
    - Remove espaços múltiplos
    """
    # Remove acentos e normaliza
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')

    # Remove números e caracteres especiais, mantém apenas letras e espaços
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Converte para minúsculas
    text = text.lower()

    # Remove espaços múltiplos e espaços no início/fim
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def extract_five_letter_words(input_filepath):
    """
    Lê um arquivo com detecção automática de encoding,
    extrai todas as palavras de 5 letras e retorna um conjunto (sem duplicatas).
    """
    five_letter_words = set()

    try:
        # Detecta o encoding automaticamente
        encoding = detect_encoding(input_filepath)
        print(f"  Encoding detectado: {encoding}")

        # Lê o arquivo com o encoding detectado
        with open(input_filepath, 'r', encoding=encoding, errors='ignore') as f:
            for line in f:
                # Normaliza a linha
                normalized_line = normalize_and_lowercase(line.strip())

                # Divide a linha em palavras
                words = normalized_line.split()

                # Filtra apenas palavras com exatamente 5 letras
                for word in words:
                    if len(word) == 5:
                        five_letter_words.add(word)

    except FileNotFoundError:
        print(f"  Erro: O arquivo '{input_filepath}' não foi encontrado.")
        return set()
    except Exception as e:
        print(f"  Erro ao ler o arquivo: {e}")
        return set()

    return five_letter_words

if __name__ == "__main__":
    raw_data_dir = 'C:/Users/Lucas/Documents/Projeto/chutermo/data/raw'
    processed_data_dir = 'C:/Users/Lucas/Documents/Projeto/chutermo/data/processed'

    # Nome do arquivo de saída único
    output_file_path = os.path.join(processed_data_dir, 'lexico.txt')

    # Garante que o diretório de saída exista
    os.makedirs(processed_data_dir, exist_ok=True)

    # Lista todos os arquivos no diretório
    files = [f for f in os.listdir(raw_data_dir)
             if os.path.isfile(os.path.join(raw_data_dir, f))]

    if not files:
        print("Nenhum arquivo encontrado no diretório de entrada.")
    else:
        print(f"Encontrados {len(files)} arquivo(s) para processar.\n")

        # Conjunto para armazenar TODAS as palavras de 5 letras (sem duplicatas)
        all_five_letter_words = set()

        for filename in files:
            input_file_path = os.path.join(raw_data_dir, filename)

            print(f"Processando: {filename}")
            words_from_file = extract_five_letter_words(input_file_path)
            print(f"  Palavras de 5 letras encontradas: {len(words_from_file)}")

            # Adiciona as palavras ao conjunto geral
            all_five_letter_words.update(words_from_file)
            print()

        # Salva todas as palavras em um único arquivo
        try:
            # Ordena as palavras alfabeticamente antes de salvar
            sorted_words = sorted(all_five_letter_words)

            with open(output_file_path, 'w', encoding='utf-8') as f:
                for word in sorted_words:
                    f.write(word + '\n')

            print("="*50)
            print(f"✓ Processamento concluído!")
            print(f"✓ Total de palavras únicas de 5 letras: {len(sorted_words)}")
            print(f"✓ Arquivo salvo em: {output_file_path}")
            print("="*50)
        except Exception as e:
            print(f"Erro ao salvar o arquivo final: {e}")