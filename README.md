# 📊 API de Relatórios de Anúncios - Flask

Este projeto é uma API desenvolvida em **Python + Flask** que consome dados de uma API externa e gera **relatórios de anúncios** para diferentes plataformas de marketing digital, exportando os dados em **CSV** e exibindo-os em tabelas HTML.

## 🚀 Funcionalidades

✅ Consome dados de uma API externa  
✅ Gera relatórios detalhados por plataforma  
✅ Exporta os relatórios no formato CSV  
✅ Exibe os relatórios em tabelas HTML  
✅ Possui rotas organizadas e modularizadas

## 🛠 Tecnologias Utilizadas

- **Python 3**
- **Flask** (Framework web)
- **Pandas** (Manipulação de dados)
- **Bootstrap** (Estilização das tabelas HTML)
- **Requests** (Consumo da API externa)

## 🔧 Como Rodar o Projeto

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2. **Crie um ambiente virtual e instale as dependências:**
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Inicie o servidor Flask:**
```bash
flask run
```

4. **Acesse no navegador:**
```bash
http://127.0.0.1:5000
```

## 📰 Endpoints da API

| Método | Rota                   | Descrição |
|--------|-------------------------|-----------|
| `GET`  | `/`                     | Página inicial |
| `GET`  | `/accounts/<platform>`  | Lista todas as contas da plataforma especificada |
| `GET`  | `/fields/<platform>`    | Lista todos os campos da plataforma especificada |
| `GET`  | `/insights/<platform>`  | Lista todas os insights da plataforma especificada |
| `GET`  | `/platforms`            | Lista todas as plataformas disponíveis |
| `GET`  | `/export/<platform>`    | Exporta o CSV da plataforma especificada |
| `GET`  | `/geral`                | Exibe todos os anúncios de todas as plataformas |
| `GET`  | `/geral/resumo`         | Exibe um resumo agregado de todas as plataformas |
| `GET`  | `/<platform>`           | Exibe um resumo da plataformas especificada |
| `GET`  | `/<platform>/resumo`    | Exibe um resumo agregado da plataformas especificada por 'account_name' |


## 🛠 Exemplo de Requisição

Para exportar um relatório da plataforma **Facebook**, execute no terminal:

```bash
curl -X GET http://127.0.0.1:5000/export/facebook
```

## 📚 Estrutura do Projeto

```
📆 seu-projeto/
 ┣ 📂 routes/          # Arquivos com as rotas Flask
 ┃ ┣ 📄 accounts.py
 ┃ ┣ 📄 fields.py
 ┃ ┣ 📄 home.py
 ┃ ┣ 📄 insights.py
 ┃ ┣ 📄 platforms.py
 ┃ ┣ 📄 reports.py
 ┣ 📂 services/        # Lógica de processamento e exportação
 ┃ ┣ 📄 api.py
 ┃ ┣ 📄 reports_services.py
 ┣ 📂 templates/       # Arquivos HTML para exibição
 ┃ ┣ 📄 platform_general_summary.html
 ┃ ┣ 📄 platform_general.html
 ┃ ┣ 📄 platform_report.html
 ┃ ┣ 📄 platform_summary.html
 ┣ 📂 views/       # Views associadas as rotas
 ┃ ┣ 📄 views_general_summary.py
 ┃ ┣ 📄 views_general.py
 ┃ ┣ 📄 views_platform.py
 ┃ ┣ 📄 views_summary.py
 ┣ 📄 app.py           # Arquivo principal Flask
 ┣ 📄 requirements.txt  # Dependências do projeto
 ┣ 📄 README.md        # Documentação do projeto
```

## 👨‍💻 Autor

Desenvolvido por **Tiago F. Hinterholz**  
🔗 [LinkedIn](https://www.linkedin.com/in/tiago-hinterholz)  
🔗 [GitHub](https://github.com/tiagohinterholz)  

