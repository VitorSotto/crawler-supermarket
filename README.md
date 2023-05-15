# crawler-supermarket

Este é um crawler desenvolvido em Python que busca uma lista pré-definida de produtos em três sites distintos: Atacadão, SuperTonin e Savegnago. Os produtos são passados através de um arquivo de texto (txt) na linha de comando.

Esse sistema foi feito para um outro projeto chamado: [EconomizeJa-backend](https://github.com/VitorSotto/EconomizeJa-backend) e [EconomizeJa-frontend](https://github.com/VitorSotto/EconomizeJa-frontend) (o frontend ainda não foi criado)

O crawler utiliza as seguintes bibliotecas Python:

- Selenium: utilizada para interagir com os sites, realizar buscas e extrair informações.
- BeautifulSoup (bs4): utilizada para fazer a análise de HTML e extrair os dados desejados.
- Pandas: utilizada para manipulação e análise de dados.
- Unidecode: utilizada para lidar com caracteres especiais e acentos.

Além disso, o crawler faz uso de um banco de dados SQLite para armazenar os produtos encontrados.

## Requisitos

Certifique-se de ter as seguintes dependências instaladas:

- Python 3.x
- Bibliotecas: Selenium, BeautifulSoup, pandas, unidecode
- Webdriver para o Selenium (por exemplo, ChromeDriver para o Google Chrome)

## Estrutura do Código

O código-fonte do crawler segue uma abordagem orientada a objetos (POO), com as seguintes classes:

- `mercado`: classe base abstrata que representa um site. Possui métodos para realizar a busca de produtos e extrair informações dos resultados.
- `atacadao`, `supertonin` e `savegnago`: classes derivadas de `mercado` que implementam a busca e extração de dados específicos para cada site.

## Contribuição

Se você quiser contribuir para este projeto, fique à vontade para fazer um fork e enviar suas melhorias através de um pull request.

## Licença

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT). Sinta-se à vontade para utilizá-lo e modificá-lo de acordo com suas necessidades.

## Autores

- [@VitorSotto](https://github.com/VitorSotto)
- [@otaviobaroni](https://github.com/otaviobaroni)
- [@RafaelMatiass](https://github.com/RafaelMatiass)
