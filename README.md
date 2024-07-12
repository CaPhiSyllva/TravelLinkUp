# TravelLinkUp API

TravelLinkUp é uma API desenvolvida para facilitar o gerenciamento de viagens. A API permite a criação, gerenciamento e confirmação de viagens, envio de convites por email e registro de atividades associadas às viagens. Este documento fornece uma visão geral da API, incluindo como configurar o projeto, a estrutura do banco de dados, as rotas disponíveis e exemplos de uso.

## Índice

- [Estrutura do Projeto](#estrutura-do-projeto)
- [Configuração do Projeto](#configuração-do-projeto)
  - [Requisitos](#requisitos)
  - [Instalação](#instalação)
- [Banco de Dados](#banco-de-dados)
  - [Estrutura das Tabelas](#estrutura-das-tabelas)
- [Rotas da API](#rotas-da-api)
  - [Viagens](#viagens)
  - [Links](#links)
  - [Participantes](#participantes)
  - [Atividades](#atividades)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
src/
├── controllers/
│   ├── activity_creator.py
│   ├── activity_finder.py
│   ├── link_creator.py
│   ├── link_finder.py
│   ├── participant_confirmer.py
│   ├── participant_creator.py
│   ├── participant_finder.py
│   ├── trip_confirmer.py
│   ├── trip_creator.py
│   └── trip_finder.py
├── drivers/
│   └── email_sender.py
├── main/
│   ├── routes/
│   │   └── trips_routes.py
│   └── server/
│       └── server.py
├── models/
│   ├── repositories/
│   │   ├── activities_repository.py
│   │   ├── email_repository.py
│   │   ├── links_repository.py
│   │   ├── participants_repository.py
│   │   └── trips_repository.py
│   └── settings/
│       └── db_connection_handler.py
└── create_email.py
run.py
```

## Configuração do Projeto

### Requisitos

- Python 3.8+
- Flask
- SQLite3
- requests
- smtplib
- email.mime

### Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/travel-linkup.git
   cd travel-linkup
   ```

2. Crie um ambiente virtual e ative-o:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

### Banco de Dados

As tabelas do banco de dados serão criadas automaticamente ao iniciar o servidor.

### Configuração do Email

O script `create_email.py` é utilizado para criar uma conta Ethereal para o envio de emails. Execute o script e substitua os detalhes da conta no arquivo `src/drivers/email_sender.py`.

### Inicialização do Servidor

Para iniciar o servidor Flask, execute:

```sh
python run.py
```

O servidor estará disponível em `http://localhost:3000`.

## Banco de Dados

### Estrutura das Tabelas

- **trips**
  ```sql
  CREATE TABLE IF NOT EXISTS 'trips'(
    id TEXT PRIMARY KEY,
    destination TEXT NOT NULL,
    start_date DATETIME,
    end_date DATETIME,
    owner_name TEXT NOT NULL,
    owner_email TEXT NOT NULL,
    status INTEGER -- 1 para verdadeiro (true), 0 para falso (false)
  );
  ```

- **emails_to_invite**
  ```sql
  CREATE TABLE IF NOT EXISTS 'emails_to_invite'(
    id TEXT PRIMARY KEY,
    trip_id TEXT,
    email TEXT NOT NULL,
    FOREIGN KEY (trip_id) REFERENCES trips(id)
  );
  ```

- **links**
  ```sql
  CREATE TABLE IF NOT EXISTS 'links'(
    id TEXT PRIMARY KEY,
    trip_id TEXT,
    link TEXT NOT NULL,
    title TEXT NOT NULL,
    FOREIGN KEY (trip_id) REFERENCES trips(id)
  );
  ```

- **participants**
  ```sql
  CREATE TABLE IF NOT EXISTS 'participants' (
      id TEXT PRIMARY KEY,
      trip_id TEXT NOT NULL,
      emails_to_invite_id TEXT NOT NULL,
      name TEXT NOT NULL,
      is_confirmed INTEGER, -- 1 para verdadeiro (true), 0 para falso (false)
      FOREIGN KEY (trip_id) REFERENCES trips(id),
      FOREIGN KEY (emails_to_invite_id) REFERENCES emails_to_invite(id)
  );
  ```

- **activities**
  ```sql
  CREATE TABLE IF NOT EXISTS 'activities' (
      id TEXT PRIMARY KEY,
      trip_id TEXT NOT NULL,
      title TEXT NOT NULL,
      occurs_at DATETIME,
      FOREIGN KEY (trip_id) REFERENCES trips(id)
  );
  ```

## Rotas da API

### Viagens

- **Criar Viagem**
  - **URL:** `/trips`
  - **Método:** `POST`
  - **Descrição:** Cria uma nova viagem.
  - **Corpo da Requisição:**
    ```json
    {
      "destination": "Destino",
      "start_date": "2023-07-20",
      "end_date": "2023-07-25",
      "owner_name": "Nome do Dono",
      "owner_email": "email@dono.com",
      "emails_to_invite": ["email1@exemplo.com", "email2@exemplo.com"]
    }
    ```

- **Obter Detalhes da Viagem**
  - **URL:** `/trips/<tripId>`
  - **Método:** `GET`
  - **Descrição:** Obtém detalhes de uma viagem específica.

- **Confirmar Viagem**
  - **URL:** `/trips/<tripId>/confirm`
  - **Método:** `GET`
  - **Descrição:** Confirma uma viagem específica.

### Links

- **Criar Link**
  - **URL:** `/trips/<tripId>/links`
  - **Método:** `POST`
  - **Descrição:** Cria um novo link para uma viagem específica.
  - **Corpo da Requisição:**
    ```json
    {
      "url": "http://exemplo.com",
      "title": "Título do Link"
    }
    ```

- **Obter Links da Viagem**
  - **URL:** `/trips/<tripId>/links`
  - **Método:** `GET`
  - **Descrição:** Obtém todos os links de uma viagem específica.

### Participantes

- **Convidar Participante**
  - **URL:** `/trips/<tripId>/invites`
  - **Método:** `POST`
  - **Descrição:** Convida um participante para uma viagem específica.
  - **Corpo da Requisição:**
    ```json
    {
      "email": "email@participante.com",
      "name": "Nome do Participante"
    }
    ```

- **Obter Participantes da Viagem**
  - **URL:** `/trips/<tripId>/participants`
  - **Método:** `GET`
  - **Descrição:** Obtém todos os participantes de uma viagem específica.

- **Confirmar Participante**
  - **URL:** `/participants/<participantId>/confirm`
  - **Método:** `PATCH`
  - **Descrição:** Confirma a participação de um participante específico.

### Atividades

- **Criar Atividade**
  - **URL:** `/trips/<tripId>/activities`
  - **Método:** `POST`
  - **Descrição:** Cria uma nova atividade para uma viagem específica.
  - **Corpo da Requisição:**
    ```json
    {
      "title": "Título da Atividade",
      "occurs_at": "2023-07-21T10:00:00"
    }
    ```

- **Obter Atividades da Viagem**
  - **URL:** `/trips/<tripId>/activities`
  - **Método:** `GET`
  - **Descrição:** Obtém todas as atividades de uma viagem específica.

## Contribuição

Contribuições são bem-vindas! Para contribuir, siga os passos abaixo:

1. Faça um fork do projeto.
2. Crie uma nova branch (`git checkout -b feature/MinhaFeature`).
3. Faça suas alterações.
4. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`).
5. Faça o push para a branch (`git push origin feature/MinhaFeature`).
6. Abra um Pull Request.

Se precisar de ajuda, sinta-se à vontade para abrir uma issue no repositório.
