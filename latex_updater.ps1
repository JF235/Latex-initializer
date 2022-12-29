$att = Read-Host -Prompt 'Quer atualizar qual arquivo? (tex|csv)'

# Camada de segurança na atualização de tex
$confirm = "n"
if ($att -eq "tex"){
    $confirm = Read-Host -Prompt "Tem certeza que deseja atualizar o .tex? O arquivo local sera sobrescrito e o seu conteudo perdido. (y|n)"
} elseif ($att -eq "csv") {
    $confirm = "y"
}

if ($confirm -eq "y"){
    python "C:\Users\jfcmp\Coisas do Jota\Code\Python\Latex initializer\latex_initializer.py" -update $att $pwd
    echo "Atualizado."
} else {
    echo "Atualizacao cancelada."
}
