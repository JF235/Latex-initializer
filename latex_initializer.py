import sys
import os
import shutil
import pandas as pd
import re

"""
Funcionamento do programa:
    1. O programa tem a localização do arquivo fonte latex.zip que guarda a pasta pré-construída de um arquivo LaTeX.
    
    2. Recebe em linha de comando o endereço do destino, onde a pasta será criada.
    
    3. O latex.zip é copiado para o destino
    
    4. O arquivo .zip é descompactado e a cópia é removida.
"""
def build():
    # Arquivo base do build
    filename = r"latex.zip"
    src = r"C:\Users\jfcmp\Coisas do Jota\Code\Python\Latex initializer" + "\\" + filename
    
    # Destino do Build
    dest = r"C:\Users\jfcmp\Coisas do Jota\Code\Python\teste"
    #dest = sys.argv[1]

    # Cria uma cópia do arquivo base e descompacta o no destino.
    shutil.copy(src,dest)
    copied_file = dest + "\\" + filename
    shutil.unpack_archive(copied_file, dest)
    os.remove(copied_file)


"""
    Cria o arquivo packages.tex importando todos os pacotes presentes em packages.csv com os respectivos comentários e opções.
"""
def criar_packagesdottex():
    with open("packages.tex", "w", encoding="utf8") as packagestex:
        # Le o arquivo packages.csv como um csv.
        pacotes_df = pd.read_csv("packages.csv", sep = ";")
        no_pacotes = len(pacotes_df)
        # Percorre os indices do Dataframe (cada pacote)
        for i in range(no_pacotes): 
            nome, opcoes, descricao = tuple(pacotes_df.loc[i])
            # Verfica a presença de descrição
            if not pd.isnull(descricao):
                packagestex.write(f"% {descricao}\n")
            # Verifica a presença de opções
            if pd.isnull(opcoes):
                packagestex.write(r"\usepackage{" + nome + "}\n\n")
            else:
                packagestex.write(r"\usepackage" + f"[{opcoes}]" + "{" + nome + "}\n\n")

"""
    Dado o conteúdo de um arquivo packages.tex (string) será realizada uma comparação entre o conteúdo desse arquivo e o conteúdo do arquivo packages.csv
    
    Há casos onde o arquivo packages.csv pode estar defasado com relação ao packages.tex e, nesse cenário, será devolvido uma lista com os pacotes faltantes.  
"""
def checar_pacotes(conteudo):
    # Todos os pacotes presentes no arquivo .tex
    lista_pacotes_tex = re.findall(r"{([\w-]+)}", conteudo)
    # Todos os pacotes presentes no arquivo .csv
    packages_df = pd.read_csv("packages.csv", sep = ";")
    lista_pacotes_csv = packages_df["nome_pacote"]
    # Transforma as listas em sets
    pacotes_tex = set(lista_pacotes_tex)
    pacotes_csv = set(lista_pacotes_csv)
    # Checa se tem mais pacotes em tex do que em csv.
    # Para isso, a diferença entre os conjuntos (pacotes_tex - pacotes_csv) é o conjunto de pacotes exclusivos do arquivo packages.tex.
    exclusivos_tex = pacotes_tex - pacotes_csv
    return list(exclusivos_tex)

"""
    Adiciona as informações do pacote "nome_pacote" para o arquivo .csv
"""
def adicionar_pacote_para_csv(nome_pacote):
    nome, opcoes, comentario = "", "", ""
    with open("packages.tex", 'r', encoding="UTF8") as file:
        conteudo = file.read()
        opcoes = r"(?:\[(.*)\])?"
        usepackage = r"\\usepackage"
        comentario = r"% (.*)"
        pacote = "{(" + nome_pacote + ")}"
        
        padrao = comentario + r"\n" + usepackage + opcoes + pacote
         
        comentario, opcoes, nome  = re.findall(padrao, conteudo)[0]
    with open("packages.csv", "a", encoding="UTF8") as file:
        file.write(f"\n{nome};{opcoes};{comentario}")


"""
    Atualiza o conteúdo do arquivo packages.csv com os novos pacotes incluídos no packages.tex que estejam ausentes no primeiro.
"""
def atualizar_pacotes():
    conteudo = ""
    with open("packages.tex", 'r', encoding="UTF8") as file:
        conteudo += file.read()
    exclusivos_tex = checar_pacotes(conteudo)
    if exclusivos_tex != []:
        for nome_pacote in exclusivos_tex:
            adicionar_pacote_para_csv(nome_pacote)

if __name__ == "__main__":
    build()