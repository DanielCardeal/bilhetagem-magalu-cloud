# Parte 1

Os princípios SOLID e o design funcional são fundamentais no desenvolvimento de grandes sistemas de software, pois facilitam a evolução incremental do sistema. Isso ocorre devido ao desenvolvimento de subsistemas altamente desacoplados e com comportamentos bem definidos.

O desacoplamento ajuda a identificar, em alto nível, onde melhorias precisam ser feitas e, talvez o mais vantajoso, onde nenhuma mudança é necessária. Como consequência, é mais fácil planejar e executar reescritas sem necessariamente propagar as mudanças para outros projetos. Além disso, o desacoplamento promovido tanto pelos princípios SOLID quanto pelo design funcional também melhora a colaboração entre as equipes de desenvolvimento. Equipes podem trabalhar em partes do sistema de forma independente, com confiança de que alterações em uma parte não causarão efeitos colaterais indesejados em outras áreas do sistema.

Além de facilitar a evolução do sistema, essas metodologias também tornam mais fácil verificar o comportamento do sistema como um todo. O uso recorrente da composição de funções puras, por exemplo, reduz a complexidade dos testes, pois elimina a necessidade de considerar efeitos colaterais na cadeia de execução da aplicação.

Naturalmente, isso não exclui a necessidade de testes de integração. No entanto, a "superfície de contato" a ser considerada é menor e melhor definida, o que simplifica a detecção dos pontos críticos a serem testados. Isso também permite que o comportamento dos sistemas seja validado sem a necessidade de entender detalhes da sua implementação interna, mas apenas compreendendo o comportamento esperado do subsistema e suas interfaces.

Em resumo, a combinação dos princípios SOLID e do design funcional oferece uma abordagem poderosa para construir e evoluir sistemas de software complexos. Ambos promovem a modularidade, escalabilidade e resiliência a mudanças, permitindo que as equipes de desenvolvimento criem soluções robustas e flexíveis. A aplicação consistente desses princípios resulta em sistemas mais fáceis de testar, manter e expandir, sem a necessidade de grandes reescritas ou mudanças disruptivas. Portanto, adotá-los desde o início do desenvolvimento é crucial para a criação de arquiteturas que suportem a evolução contínua e a adaptação às mudanças de mercado.

# Parte 2

## Ingestor

O sistema ingestor recebe um volume imenso de dados

## API privada

### POST /api/v1/{tenant}/{product_sku}

**Descrição:** Registra um novo pulso de consumo de um determinado tenant/produto.
**Autenticação:** API key
**Body:**

```json
{
  "used_amount": 50,
  "use_unity": "GB x seg",
  "api_key": "..."
}
```

**Observações:**

- O ingestor não valida as informações de uso informadas no pulso, só as registra.

# Processador e armazenador (P&A)

## API

### POST /api/v1/{tenant}/{product_sku}

**Descrição:** registra um novo agregado de consumo dos produtos
**Autenticação:** SSL com autenticação mútua
**Body:**

```json
{
    "aggregate_ammount": 50,
    "use_unity": "GB x sec",
    "timestamp": <date>
}
```

**Observações:**

- P&A é responsável por validar que o `tenant` pode usar `produt_sku`.
- P&A é responsável por converter as medidas em uma única unidade.


### GET /api/v1/{tenant}?date=YYYY-MM

**Descrição:** recupera o relatório de uso de todos os produtos para um dado `tenant` em um determinado ano/mês
**Response:**

```json
[
    "tenant": {tenant},
    "year": {YYYY},
    "month": {MM},
    "total_cost": 158000, // R$158,00
    "aggregates": [
        "product_sku_1": {
            "aggregate_ammount": 1500,
            "use_unity": "Gb x sec",
            "cost_per_unity": 100, // R$0,10
            "total_cost": 150000,  // R$150,00
        },
        "product_sku_2": {
            "aggregate_ammount": 8000,
            "use_unity": "api_call",
            "cost_per_unity": 1, // R$0,001
            "total_cost": 8000,  // R$8,00
        },
        ...
    ]
]
```

**Observações:**

- O custo por unidade e o custo total são convertidos a milésimos de real. Usam-se inteiros para evitar problemas de arredondamento com floats.

### GET /api/v1/{tenant}/{product_sku}?date=YYYY-MM

**Descrição:** recupera o relatório de uso de todos os produtos para um dado `tenant` em um determinado ano/mês
**Response:**

```json
[
    "tenant": {tenant},
    "year": {year},
    "month": {month},
    "total_cost": 158000, // R$158,00
    "aggregates": [
        "product_sku_1": {
            "aggregate_ammount": 1500,
            "use_unity": "Gb x sec",
            "cost_per_unity": 100, // R$0,10
            "total_cost": 150000,  // R$150,00
        },
    ]
]
```

**Observações:**

- O custo por unidade e o custo total são convertidos a milésimos de real. Usam-se inteiros para evitar problemas de arredondamento com floats.
