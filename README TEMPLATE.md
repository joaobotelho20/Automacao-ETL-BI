# 📊 Data Science Template

Bem-vindo ao repositório do projeto de Data Science. Este documento fornece uma visão geral da estrutura do template de projeto

## 📁 Estrutura do Projeto

```plaintext
data-science-project/
│
├── 📁 data/
│   ├── 📁 raw/                # Dados brutos, não processados
│   ├── 📁 processed/          # Dados processados, prontos para análise
│   └── 📁 external/           # Dados de fontes externas
│
├── 📁 notebooks/
│   ├── 📁 exploratory/        # Notebooks para análise exploratória
│   ├── 📁 reporting/          # Notebooks para geração de relatórios
│   └── 📁 experiments/        # Notebooks para experimentos e testes
│
├── 📁 source code/
│   ├── 📁 data/               # Scripts para download ou geração de dados
│   ├── 📁 features/           # Scripts para criação de features a partir dos dados brutos
│   ├── 📁 models/             # Scripts para treinamento e avaliação de modelos
│   ├── 📁 visualization/      # Scripts para criação de visualizações e gráficos
│   └── 📁 librarys/           # Scripts para criação de bibliotecas em seu código 
│
├── 📁 tests/                  # Scripts para testes de unidade e integração
│
├── 📁 reports/
│   ├── 📁 figures/            # Figuras e gráficos gerados
│   └── 📁 final/              # Relatórios finais
│
├── 📁 config/                 # Arquivos de configuração e parâmetros do projeto
│
├── 📋 requirements.txt        # Lista de dependências do projeto
├── 📖 README.md               # Descrição do projeto e instruções modelo
├── 📖 README TEMPLATE.md      # Descrição do template estruturado aqui
└── 🚫 .gitignore              # Arquivo gitignore
```

### 📂 Descrição dos Diretórios

- **data/**: Diretório para armazenar os dados do projeto.
  - **raw/**: Dados brutos, não processados.
  - **processed/**: Dados processados, prontos para análise.
  - **external/**: Dados de fontes externas.

- **notebooks/**: Diretório para notebooks Jupyter.
  - **exploratory/**: Notebooks para análise exploratória.
  - **reporting/**: Notebooks para geração de relatórios.
  - **experiments/**: Notebooks para experimentos e testes.

- **src/**: Diretório para código-fonte do projeto.
  - **data/**: Scripts para download ou geração de dados.
  - **features/**: Scripts para criação de features a partir dos dados brutos.
  - **models/**: Scripts para treinamento e avaliação de modelos.
  - **visualization/**: Scripts para criação de visualizações e gráficos.
  - **librarys/**: Scripts para criação de bibliotecas em seu código. 

- **tests/**: Scripts para testes de unidade e integração.

- **reports/**: Diretório para relatórios e figuras.
  - **figures/**: Figuras e gráficos gerados.
  - **final/**: Relatórios finais.

- **config/**: Arquivos de configuração e parâmetros do projeto.

- **requirements.txt**: Lista de dependências do projeto.

- **README.md**: Modelo para ser utilizado inicialmente personalizável para seu projeto.
- 
- **README.md**: Descrição do template e instruções iniciais.

- **.gitignore**: Arquivo gitignore para especificar quais arquivos não devem ser versionados.

## 🤝 Como Contribuir

1. Faça um fork deste repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nome-da-feature`).
3. Commit suas alterações (`git commit -am 'Adiciona nova feature'`).
4. Envie para o branch (`git push origin feature/nome-da-feature`).
5. Abra um Pull Request.

Autor: João Botelho
