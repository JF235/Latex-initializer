# Do que se trata $\LaTeX$ Initializer?

Uma aplicação que gera automaticamente uma pasta `latex` com toda a organização de arquivos e hierarquia de pastas para a elaboração de um documento.

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

Tem um arquivo `packages.csv` com os pacotes padrões que estão associados a cada projeto. 

Sempre que se deseja atualizar os pacotes que estão em `packages.csv` com relação aos pacotes usados em um dado projeto, é preciso executar `package_updater.ps1`. Dessa maneira, ele vai comparar todos os pacotes do csv com aqueles que estão em `packages.tex`, adicionando os pacotes extras do `.tex` no `.csv`.

Observe que o contrário não acontece. O arquivo `.tex` não é modificado durante esse processo, ou seja, os arquivos que tem no `.csv`, mas não tem `.tex` não são atualizados.