# API RESTful de Imóveis

API RESTful desenvolvida em Flask com Python para gerenciamento de imóveis, com testes automatizados (Pytest) e persistência em banco MySQL.

## Tabela de Contrato das Rotas

| Método | Rota | Descrição | Entrada (JSON / Params) | Resposta de Sucesso | Código HTTP Sucesso | Erros Possíveis e Códigos |
| --- | --- | --- | --- | --- | --- | --- |
| **GET** | `/imoveis` | Lista todos os imóveis | Nenhum | Lista de imóveis `[...]` | **200 OK** | 500 (Erro do Servidor) |
| **GET** | `/imoveis?tipo={tipo}` | Filtra imóveis por tipo | Query Param `tipo` | Lista de imóveis `[...]` | **200 OK** | 500 (Erro do Servidor) |
| **GET** | `/imoveis?cidade={cidade}` | Filtra imóveis por cidade | Query Param `cidade` | Lista de imóveis `[...]` | **200 OK** | 500 (Erro do Servidor) |
| **GET** | `/imoveis?tipo={t}&cidade={c}` | Combina filtros tipo e cidade | Query Params `tipo` e `cidade` | Lista de imóveis `[...]` | **200 OK** | 500 (Erro do Servidor) |
| **GET** | `/imoveis/<id>` | Busca um imóvel específico pelo ID | Nulo (passado na URL) | Objeto do imóvel `{...}` | **200 OK** | 404 (Não encontrado) |
| **POST** | `/imoveis` | Cadastra um novo imóvel | JSON do imóvel (sem `id`) | Objeto do imóvel criado com `id` | **201 Created** | 400 (Campos obrigatórios ausentes ou JSON inválido) |
| **PUT** | `/imoveis/<id>` | Atualiza um imóvel existente | JSON com os dados | Objeto atualizado | **200 OK** | 400 (JSON inválido), 404 (Imóvel não existe) |
| **DELETE** | `/imoveis/<id>` | Remove um imóvel pelo ID | Nenhum | Corpo vazio | **204 No Content** | 404 (Imóvel não existe) |

### Regras de Validação
- **Campos Obrigatórios no Cadastro (`POST`):** `logradouro` e `cidade`.
- **Campo Gerado Automático:** `id` (não pode ser informado ou alterado pelo cliente).
- **Formatos:** `valor` deve ser numérico e `data_aquisicao` deve seguir o formato `AAAA-MM-DD`.

### Exemplo de JSON de Entrada (`POST /imoveis`):
```json
{
  "logradouro": "Rua Quatá",
  "tipo_logradouro": "Rua",
  "bairro": "Vila Olímpia",
  "cidade": "São Paulo",
  "cep": "04546-042",
  "tipo": "apartamento",
  "valor": 750000.00,
  "data_aquisicao": "2023-05-10"
}
Exemplo de JSON de Saída (201 Created ou 200 OK):
{
  "id": 1,
  "logradouro": "Rua Quatá",
  "tipo_logradouro": "Rua",
  "bairro": "Vila Olímpia",
  "cidade": "São Paulo",
  "cep": "04546-042",
  "tipo": "apartamento",
  "valor": 750000.00,
  "data_aquisicao": "2023-05-10"
}


URL de Produção (AWS EC2)
http://18.227.74.168/imoveis
