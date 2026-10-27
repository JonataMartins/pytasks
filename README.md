# PyTasks // Quest Log

Um gerenciador de tarefas com identidade visual inspirada em jogos retrô e pixel art, desenvolvido com Python e Flask. Cadastre missões, defina prazos finais e acompanhe sua lista organizada por dia.

## Funcionalidades

- Cadastrar tarefas com descrição de até 120 caracteres.
- Definir um prazo final para cada tarefa (opcional).
- Organizar automaticamente as tarefas por dia, com grupos para hoje, amanhã, outras datas e tarefas sem prazo.
- Destacar tarefas atrasadas que ainda não foram concluídas.
- Marcar tarefas como concluídas ou pendentes.
- Visualizar missões em duas abas independentes: “Em andamento” e “Concluídas”, mantendo a organização por dia em cada aba.
- Excluir tarefas com confirmação.
- Visualizar totais de missões, tarefas pendentes e concluídas, além de uma barra de progresso.
- Salvar os dados localmente em um banco SQLite, inclusive depois de fechar a aplicação.
- Usar uma interface responsiva com estética retrô/pixel art.
- Migrar automaticamente bancos antigos adicionando a coluna de prazo, sem apagar as tarefas existentes.

## Tecnologias

- Python 3.10 ou superior
- Flask
- SQLite (biblioteca padrão do Python)
- HTML5 e CSS3
- Fontes Press Start 2P e VT323 via Google Fonts (requer internet para carregá-las; há fontes alternativas caso não carreguem)

## Como executar

1. Instale o Python 3.10 ou superior.
2. Crie e ative um ambiente virtual (recomendado):

   **Windows**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **Linux/macOS**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute a aplicação:
   ```bash
   python app.py
   ```
5. Acesse `http://127.0.0.1:5000` no navegador.

O arquivo `tasks.db` é criado automaticamente na pasta do projeto na primeira execução.

## Estrutura do projeto

```text
pytasks/
├── app.py              # Rotas, funções e acesso ao banco
├── requirements.txt    # Dependências Python
├── README.md           # Documentação do projeto
├── tasks.db            # Criado automaticamente ao executar
├── templates/
│   └── index.html      # Interface HTML renderizada pelo Flask
└── static/
    └── style.css       # Tema pixel art e estilos responsivos
```

## Conceitos demonstrados

- Funções para separar responsabilidades.
- Validação de formulários e condicionais.
- Manipulação e formatação de datas com `datetime`.
- Agrupamento de tarefas por dia.
- Rotas Flask com métodos HTTP GET e POST.
- Consultas SQL parametrizadas e persistência com SQLite.
- Templates HTML com Jinja e estilos CSS responsivos.