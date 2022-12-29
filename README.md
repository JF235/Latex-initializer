# Do que se trata $\LaTeX$ Initializer?

Uma aplicação que gera automaticamente uma pasta `latex` com toda a organização de arquivos e hierarquia de pastas para a elaboração de um documento.

```powershell
latex_initializer.ps1
```

Também serve para manter atualizados os pacotes usados em cada um dos projetos.

```
latex_updater.ps1
```

## Em poucas palavras

```powershell
# INICIALIZANDO
PS ...\Path\> latex_initializer.ps1
Initializing LaTeX document.
Done.
# Vai abrir a pasta "latex" no VScode
Deseja abrir o tutorial? (y|n): n 
# Opção de abrir a pasta de tutorial no VScode

# ATUALIZAÇÃO DE PACOTES
PS ...\Path\latex> latex_updater.ps1
Quer atualizar qual arquivo? (tex|csv): tex
# vai atualizar packages.tex no projeto atual.
# Caso fosse "csv", atualizaria os pacotes na pasta da aplicação
```

# Sobre a estrutura da pasta

```
{latex}
|   content.tex
|   {imgs}
|   |   (todas as imagens usadas)
|   {configs}
|   |   main.tex
|   |   titlepage.tex
|   |   configs.tex
|   |   packages.tex

{} - pastas
() - descrição em alto nível
```

# Gerenciamento de Pacotes

Tem um arquivo `packages.csv`, no local da aplicação, com todos os pacotes padrões que estão associados a cada projeto.

## Atualizando o `packages.csv`

Sempre que se deseja atualizar os pacotes que estão em `packages.csv` com relação aos pacotes usados em um dado projeto, é preciso executar `package_updater.ps1` e digitar `csv`. Dessa maneira, ele vai comparar todos os pacotes do `packages.csv` com aqueles que estão em `packages.tex`, adicionando os pacotes extras do `.tex` no `.csv`.

Observe que o contrário não acontece durante esse processo. O arquivo `.tex` não é modificado durante a execução do update com opção `csv`, ou seja, os pacotes exclusivos do `csv` não vão para o `tex`.

Para isso será necessário a execução do updater com o argumento `tex`.

## Atualizando o `packages.tex`

Há também como atualizar os pacotes no `.tex`, reescrevendo todo o seu conteúdo com base no `.csv`. Basta executar o updater com o argumento `tex`. No programa a rotina `criar_packagesdottex(pacotes_tex)` será executada.

Aviso: o arquivo `.tex` será reescrito e, portanto, o conteúdo original será **perdido**!