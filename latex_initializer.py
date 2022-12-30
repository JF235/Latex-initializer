import sys
import os
import shutil
import pandas as pd
import re
import stat

def make_archive(source, destination):
    """
    Função de: http://www.seanbehan.com/how-to-use-python-shutil-make_archive-to-zip-up-a-directory-recursively-including-the-root-folder/
    
    Ele lida com o problema de zipar somente os arquivos dentro pasta, sem considerar a pasta em si.
    
    Com essa função quando eu zipar latex/ eu tenho latex.zip com a primeira pasta interna sendo a própria latex/
    """
    base = os.path.basename(destination)
    name = base.split('.')[0]
    format = base.split('.')[1]
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    #print(source, destination, archive_from, archive_to)
    shutil.make_archive(name, format, archive_from, archive_to)
    shutil.move('%s.%s'%(name,format), destination)


def build():
    """
    Funcionamento do programa:
        
        1. O programa tem a localização do arquivo fonte latex.zip que guarda a pasta pré-construída de um arquivo LaTeX.
        
        2. Recebe em linha de comando o endereço do destino, onde a pasta será criada.
        
        3. O latex.zip é copiado para o destino
        
        4. O arquivo .zip é descompactado e a cópia é removida.
    """
    global SRC
    global DEST

    # Copiar a pasta latex_src para latex
    latex_dir = SRC + r"\latex"
    latex_src_dir =  SRC + r"\latex_src"
    shutil.copytree(latex_src_dir, latex_dir, dirs_exist_ok = True)
    
    # Checar se há opções customizadas.
    doc = input("Deseja criar um documento (p)adrão ou (c)ustomizado? (p|c) ")
    if doc == "c":
        predef = input("Qual o estilo predefinido? ")
        
        # Sobrescreve os arquivos em \latex\configs com os arquivos de predefs\<predef>\
        configs_dir = latex_dir + r"\configs"
        predef_dir = SRC + r"\predefs" + f"\\{predef}"
        shutil.copytree(predef_dir, configs_dir, dirs_exist_ok = True)
    
    # Criar .zip
    make_archive(latex_dir, latex_dir + ".zip")
    os.system(f'rmdir /S /Q "{latex_dir}"')
    
    # Cria uma cópia do arquivo base e descompacta o no destino.
    filename = "latex.zip"
    shutil.copy(SRC + f"\\{filename}", DEST)
    copied_file = DEST + f"\\{filename}"
    shutil.unpack_archive(copied_file, DEST)
    os.remove(latex_dir + ".zip")
    os.remove(copied_file)

def criar_packagesdottex(pacotes_tex):
    """
        Cria o arquivo packages.tex importando todos os pacotes presentes em packages.csv com os respectivos comentários e opções.
    """
    
    global SRC
    with open(pacotes_tex, "w", encoding="utf8") as packagestex:
        # Le o arquivo packages.csv como um Dataframe do pandas.
        pacotes_df = pd.read_csv(f"{SRC}\\packages.csv", sep = ";")
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


def checar_pacotes(conteudo):
    """
    Dado o conteúdo de um arquivo packages.tex (string) será realizada uma comparação entre o conteúdo desse arquivo e o conteúdo do arquivo packages.csv
    
    Há casos onde o arquivo packages.csv pode estar defasado com relação ao packages.tex e, nesse cenário, será devolvido uma lista com os pacotes faltantes.  
    """
    
    global SRC
    # Todos os pacotes presentes no arquivo .tex
    usepackage = r"\\usepackage"
    opcoes = r"(?:\[.*\])?"
    pacote = "{(" + r"[\w-]+" + ")}"
    padrao = usepackage + opcoes + pacote
    lista_pacotes_tex = re.findall(padrao, conteudo)
    # Todos os pacotes presentes no arquivo .csv
    packages_df = pd.read_csv(f"{SRC}\\packages.csv", sep = ";")
    lista_pacotes_csv = packages_df["nome_pacote"]
    # Transforma as listas em sets
    pacotes_tex = set(lista_pacotes_tex)
    pacotes_csv = set(lista_pacotes_csv)
    # Checa se tem mais pacotes em tex do que em csv.
    # Para isso, a diferença entre os conjuntos (pacotes_tex - pacotes_csv) é o conjunto de pacotes exclusivos do arquivo packages.tex.
    exclusivos_tex = pacotes_tex - pacotes_csv
    return list(exclusivos_tex)


def adicionar_pacote_para_csv(nome_pacote, pacotes_tex):
    """
    Adiciona as informações do pacote "nome_pacote" para o arquivo .csv
    """
    
    global SRC
    nome, opcoes, comentario = "", "", ""
    with open(pacotes_tex, 'r', encoding="UTF8") as file:
        conteudo = file.read()
        # Construindo a ER (Expressão Regular) que irá dar match com o comando "%comentário\n\usepackage[opcao]{pacote}"
        comentario = r"(?:%[ ]?(.*)\n)?"
        usepackage = r"\\usepackage"
        opcoes = r"(?:\[(.*)\])?"
        pacote = "{(" + nome_pacote + ")}"
        padrao = comentario + usepackage + opcoes + pacote
        # Devolve os grupos presentes na ER.
        comentario, opcoes, nome  = re.findall(padrao, conteudo)[0]
    with open(f"{SRC}\\packages.csv", "a", encoding="UTF8") as file:
        # Append uma linha extra no csv.
        file.write(f"\n{nome};{opcoes};{comentario}")



def atualizar_pacotes_csv(pacotes_tex):
    """
    Atualiza o conteúdo do arquivo packages.csv com os novos pacotes incluídos no packages.tex que estejam ausentes no primeiro.
    """
    
    conteudo = ""
    with open(pacotes_tex, 'r', encoding="UTF8") as file:
        conteudo += file.read()
    # Faz a checagem e coleta o nome dos novos pacotes em uma lista, exclusivos_tex.
    exclusivos_tex = checar_pacotes(conteudo)
    if exclusivos_tex != []:
        for nome_pacote in exclusivos_tex:
            print(f"Adicionando {nome_pacote}.")
            adicionar_pacote_para_csv(nome_pacote, pacotes_tex)
    else:
        print("Os pacotes já estão atualizados.")

def verificar_simetria_csv():
    """
    Verifica a simetria dos campos: incompatibilidade, importado_antes, importados_depois.
    
    1. Se incompatibilidade de A tem B, então incompatibilidade de B deve ter A.
    2. Se importado_antes de A tem B, então importado_depois de B deve ter A.
    3. Se importado_depois de A tem B, então importado_antes de B deve ter A.  
    """
    path = f"{SRC}\\packages.csv"
    df = pd.read_csv(path, sep = ";")
    df.fillna('', inplace=True) # subsitui nan por string vazia
    # Checar simetria (1) incompatibilidades
    for i in range(len(df)):
        checar_simetria_incomp(i, df)
    df.to_csv("new.csv",sep=';', index=False)


def obter_lista_incomp(i, df):
    """
    Obtém a lista de incompatibilidades de índice i.
    """
    incomp_list = df.loc[i]["incompatibilidades"].split(",")
    incomp_list = [incomp.strip() for incomp in incomp_list]
    # Se o campo está vazio, ele devolve uma lista vazia.
    if incomp_list == [""]:
        incomp_list = []
    return incomp_list

def checar_simetria_incomp(i, df):
    """
    Checa a simetria de incompatibilidades de índice i.
    """
    # Lista de incompatibilidades do pacote atual
    pacote_atual = df.loc[i]["nome_pacote"]
    lista_incomp = obter_lista_incomp(i, df)
    for incomp in lista_incomp:
        idx = list(df["nome_pacote"]).index(incomp)
        # Caso B esteja em A. Checa se A está em B e, no caso negativo, atualiza o dataframe.
        if pacote_atual not in obter_lista_incomp(idx, df):
            print(f"Problema nas incompatibildiades de {incomp}. Falta {pacote_atual}.")
            nova_lista_incomp = obter_lista_incomp(idx, df)
            nova_lista_incomp.append(pacote_atual)
            df.loc[idx]["incompatibilidades"] = ",".join(nova_lista_incomp)

if __name__ == "__main__":
    global SRC, DEST
    
    # Configurando os caminhos
    SRC = r"C:\Users\jfcmp\Coisas do Jota\Code\Python\Latex initializer"
    DEST = sys.argv[-1]
    if DEST == SRC:
        raise Exception("O aplicativo está sendo executada na própria pasta.")
    
    modo = sys.argv[1]
    # BUILD
    if modo == "-build":
        build()
    # UPDATE
    elif modo == "-update":
        pacotes_tex = f"{DEST}\\configs\\packages.tex"
        alvo_update = sys.argv[2]
        if alvo_update == "tex":
            # Atualiza o conteúdo de packages.tex em dest, com o conteúdo de packages.csv
            criar_packagesdottex(pacotes_tex)
        elif alvo_update == "csv":
            # Atualiza o conteúdo do .csv
            atualizar_pacotes_csv(pacotes_tex)
    
    