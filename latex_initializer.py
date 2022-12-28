import sys
import os
import shutil

"""
Funcionamento do programa:
    1. O programa tem a localização do arquivo fonte latex.zip que guarda a pasta pré-construída de um arquivo LaTeX.
    
    2. Recebe em linha de comando o endereço do destino, onde a pasta será criada.
    
    3. O latex.zip é copiado para o destino
    
    4. O arquivo .zip é descompactado e a cópia é removida.

"""
def main():
    filename = r"latex.zip"
    src = r"C:\Users\jfcmp\Coisas do Jota\Code\Python\Latex initializer" + "\\" + filename
    # C:\Users\jfcmp\Coisas do Jota\Code\Python\teste
    dest = sys.argv[1]

    shutil.copy(src,dest)
    copied_file = dest + "\\" + filename
    shutil.unpack_archive(copied_file, dest)
    os.remove(copied_file)

if __name__ == "__main__":
    main()