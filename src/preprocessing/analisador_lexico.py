import json
from collections import Counter, defaultdict
from pathlib import Path

def calcular_peso(frequencias):
    """
    Calcula o peso normalizado (0 a 1.0) proporcional às frequências.
    O peso mantém a proporção entre as frequências.
    """
    if not frequencias:
        return {}

    valores = list(frequencias.values())
    min_freq = min(valores)
    max_freq = max(valores)

    # Se todos têm a mesma frequência
    if max_freq == min_freq:
        return {k: 1.0 for k in frequencias.keys()}

    # Normalização proporcional
    pesos = {}
    for chave, freq in frequencias.items():
        peso = (freq - min_freq) / (max_freq - min_freq)
        pesos[chave] = round(peso, 6)

    return pesos

def analisar_lexico(arquivo_entrada='../data/processed/lexico.txt'):
    """
    Analisa o arquivo léxico e gera estatísticas completas.
    """
    # Ler o arquivo
    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            texto = f.read().upper()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado!")
        return

    # Remover espaços e quebras de linha para análise
    palavras = texto.split()

    # 1. Quantidade de cada letra
    letras = Counter()
    for palavra in palavras:
        letras.update(palavra)

    # 2. Quantidade de cada letra em cada posição
    letras_por_posicao = defaultdict(Counter)
    max_tamanho = 0
    for palavra in palavras:
        max_tamanho = max(max_tamanho, len(palavra))
        for pos, letra in enumerate(palavra):
            letras_por_posicao[pos][letra] += 1

    # 3. Binômios mais comuns
    binomios = Counter()
    for palavra in palavras:
        for i in range(len(palavra) - 1):
            binomio = palavra[i:i+2]
            binomios[binomio] += 1

    # 4. Binômios mais comuns em cada posição
    binomios_por_posicao = defaultdict(Counter)
    for palavra in palavras:
        for i in range(len(palavra) - 1):
            binomio = palavra[i:i+2]
            binomios_por_posicao[i][binomio] += 1

    # 5. Trinômios mais comuns
    trinomios = Counter()
    for palavra in palavras:
        for i in range(len(palavra) - 2):
            trinomio = palavra[i:i+3]
            trinomios[trinomio] += 1

    # 6. Trinômios mais comuns em cada posição
    trinomios_por_posicao = defaultdict(Counter)
    for palavra in palavras:
        for i in range(len(palavra) - 2):
            trinomio = palavra[i:i+3]
            trinomios_por_posicao[i][trinomio] += 1

    # Gerar relatórios
    gerar_relatorios(
        letras, letras_por_posicao,
        binomios, binomios_por_posicao,
        trinomios, trinomios_por_posicao,
        max_tamanho,
        'C:/Users/Lucas/Documents/Projeto/chutermo/data/statistics'
    )

    print("\nAnálise concluída! Arquivos gerados:")
    print("  - letras_frequencia.json")
    print("  - letras_por_posicao.json")
    print("  - binomios_frequencia.json")
    print("  - binomios_por_posicao.json")
    print("  - trinomios_frequencia.json")
    print("  - trinomios_por_posicao.json")

def gerar_relatorios(letras, letras_por_posicao, binomios, binomios_por_posicao,
                     trinomios, trinomios_por_posicao, max_tamanho, output_dir):
    """
    Gera arquivos JSON com as análises e pesos.
    """

    # 1. Letras - Frequência Geral
    letras_data = []
    pesos_letras = calcular_peso(letras)
    for letra, freq in letras.most_common():
        letras_data.append({
            'letra': letra,
            'quantidade': freq,
            'peso': pesos_letras[letra]
        })

    with open(Path(output_dir) / 'letras_frequencia.json', 'w', encoding='utf-8') as f:
        json.dump(letras_data, f, ensure_ascii=False, indent=2)

    # 2. Letras por Posição
    letras_pos_data = {}
    for pos in range(max_tamanho):
        if pos in letras_por_posicao:
            freq_pos = letras_por_posicao[pos]
            pesos_pos = calcular_peso(freq_pos)
            letras_pos_data[f'posicao_{pos}'] = [
                {
                    'letra': letra,
                    'quantidade': freq,
                    'peso': pesos_pos[letra]
                }
                for letra, freq in freq_pos.most_common()
            ]

    with open(Path(output_dir) / 'letras_por_posicao.json', 'w', encoding='utf-8') as f:
        json.dump(letras_pos_data, f, ensure_ascii=False, indent=2)

    # 3. Binômios - Frequência Geral
    binomios_data = []
    pesos_binomios = calcular_peso(binomios)
    for binomio, freq in binomios.most_common(100):  # Top 100
        binomios_data.append({
            'binomio': binomio,
            'quantidade': freq,
            'peso': pesos_binomios[binomio]
        })

    with open(Path(output_dir) / 'binomios_frequencia.json', 'w', encoding='utf-8') as f:
        json.dump(binomios_data, f, ensure_ascii=False, indent=2)

    # 4. Binômios por Posição
    binomios_pos_data = {}
    for pos in range(max_tamanho - 1):
        if pos in binomios_por_posicao:
            freq_pos = binomios_por_posicao[pos]
            pesos_pos = calcular_peso(freq_pos)
            binomios_pos_data[f'posicao_{pos}'] = [
                {
                    'binomio': binomio,
                    'quantidade': freq,
                    'peso': pesos_pos[binomio]
                }
                for binomio, freq in freq_pos.most_common(50)  # Top 50 por posição
            ]

    with open(Path(output_dir) / 'binomios_por_posicao.json', 'w', encoding='utf-8') as f:
        json.dump(binomios_pos_data, f, ensure_ascii=False, indent=2)

    # 5. Trinômios - Frequência Geral
    trinomios_data = []
    pesos_trinomios = calcular_peso(trinomios)
    for trinomio, freq in trinomios.most_common(100):  # Top 100
        trinomios_data.append({
            'trinomio': trinomio,
            'quantidade': freq,
            'peso': pesos_trinomios[trinomio]
        })

    with open(Path(output_dir) / 'trinomios_frequencia.json', 'w', encoding='utf-8') as f:
        json.dump(trinomios_data, f, ensure_ascii=False, indent=2)

    # 6. Trinômios por Posição
    trinomios_pos_data = {}
    for pos in range(max_tamanho - 2):
        if pos in trinomios_por_posicao:
            freq_pos = trinomios_por_posicao[pos]
            pesos_pos = calcular_peso(freq_pos)
            trinomios_pos_data[f'posicao_{pos}'] = [
                {
                    'trinomio': trinomio,
                    'quantidade': freq,
                    'peso': pesos_pos[trinomio]
                }
                for trinomio, freq in freq_pos.most_common(50)  # Top 50 por posição
            ]

    with open(Path(output_dir) / 'trinomios_por_posicao.json', 'w', encoding='utf-8') as f:
        json.dump(trinomios_pos_data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    print("Iniciando análise léxica...")
    analisar_lexico('C:/Users/Lucas/Documents/Projeto/chutermo/data/processed/lexico.txt')