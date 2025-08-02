# Estruturas de Dados Interativas

## Descrição

Este projeto é uma coleção de implementações de estruturas de dados fundamentais em Python, cada uma com uma interface gráfica interativa desenvolvida com Tkinter. O objetivo é fornecer uma maneira visual e interativa de entender e manipular diferentes estruturas de dados, tornando o aprendizado mais acessível e prático. Cada estrutura é apresentada em uma aba separada, permitindo aos usuários realizar operações como inserção, remoção, busca e visualização em tempo real.

## Estruturas de Dados Incluídas

- **Árvore Binária**: Uma árvore binária com inserção em ordem de nível, exclusão, busca e visualização gráfica. Nós encontrados na busca são destacados em verde claro.
- **Árvore AVL**: Uma árvore de busca binária auto-balanceada com inserção, exclusão, busca, balanceamento via rotações e visualização. Exibe alturas dos nós e destaca nós encontrados.
- **Pilha (Stack)**: Uma pilha com operações de empilhar, desempilhar, visualizar o topo e visualização gráfica, com o topo destacado.
- **Fila (Queue)**: Uma fila com operações de enfileirar, desenfileirar e visualização gráfica, indicando frente e final.
- **Lista Encadeada (Linked List)**: Uma lista encadeada com inserção no início e fim, remoção, busca e visualização, com nós encontrados destacados.
- **Tabela Hash (Hash Table)**: Uma tabela hash com inserção, busca, remoção e visualização, destacando baldes e itens encontrados.

## Requisitos

- **Python 3.x**: Necessário para executar o programa.
- **Tkinter**: Biblioteca gráfica incluída com Python.
- **hashlib** (para Tabela Hash): Incluído com Python.

## Como Executar

1. Certifique-se de ter Python 3.x instalado.
2. Clone o repositório ou baixe os arquivos.
3. Execute o comando:

   ```
   python main.py
   ```
4. Uma janela será aberta com abas para cada estrutura de dados. Selecione a aba desejada para interagir com a estrutura correspondente.

## Uso

- **Navegação**: Use o menu de abas para selecionar a estrutura de dados desejada.
- **Interação**: Insira valores no campo de entrada e clique nos botões para realizar operações (ex.: inserir, remover, buscar).
- **Visualização**: A estrutura é atualizada automaticamente no canvas após cada operação, com nós/itens encontrados destacados em verde claro ou dourado (tabela hash).
- **Mensagens**: O status na parte inferior exibe resultados das operações (ex.: "Inserido: 10", "Valor não encontrado").
- **Redimensionamento**: A visualização se ajusta automaticamente ao redimensionar a janela.

## Contribuições

Contribuições são bem-vindas! Para contribuir, por favor, crie um fork do repositório, faça suas alterações e envie um pull request. Um arquivo CONTRIBUTING.md será adicionado em breve com diretrizes detalhadas.

## Licença

Este projeto está licenciado sob a Licença MIT.

## Agradecimentos

- **Tkinter**: Biblioteca usada para criar as interfaces gráficas interativas.
- **Python Community**: Por fornecer recursos e documentação que inspiraram este projeto.

## Estrutura do Projeto

| Arquivo | Descrição |
| --- | --- |
| `main.py` | Arquivo principal que integra todas as estruturas em uma interface com abas. |
| `binarytree.py` | Implementação da árvore binária com GUI. |
| `treeavl.py` | Implementação da árvore AVL com GUI. |
| `pilha.py` | Implementação da pilha com GUI. |
| `fila.py` | Implementação da fila com GUI. |
| `lista.py` | Implementação da lista encadeada com GUI. |
| `tabelaHash.py` | Implementação da tabela hash com GUI. |

## Notas Adicionais

- O projeto é ideal para estudantes e profissionais que desejam explorar estruturas de dados de forma visual.
- As visualizações são otimizadas para clareza, mas árvores grandes podem apresentar sobreposição visual.
- Para suporte ou sugestões, abra uma issue no repositório.