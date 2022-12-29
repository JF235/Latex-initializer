# Criando a pasta
echo "Initializing LaTeX document."

python "C:\Users\jfcmp\Coisas do Jota\Code\Python\Latex initializer\latex_initializer.py" -build $pwd

echo "Done."


# Pergunta se deseja abrir o tutorial
$Open_tutorial = Read-Host -Prompt 'Deseja abrir o tutorial? (y|n)'

# Abre a pasta "latex" e, possivelmente, o tutorial. 
cd latex
code .
if ($Open_tutorial -eq "y") {
    code "C:\Users\jfcmp\Coisas do Jota\Vault-1\Programas e Tutoriais\Tutoriais\Latex"
}