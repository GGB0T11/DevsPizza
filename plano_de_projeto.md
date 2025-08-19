## Objetivo

**Geral:**

- Desenvolver um sistema multiplataforma de gerenciamento de estoque para pizzarias, que automatize e facilite o controle de entrada e saída de insumos.
  **Específicos:**
- Desenvolver um módulo para controle de entrada e saída de produtos, com registro automático das movimentações de estoque.
- Implementar um sistema de notificação automática para alertas de reposição de insumos em níveis críticos.
- Implementar a geração de relatórios detalhados de uso e histórico de movimentações, possibilitando a análise precisa dos padrões de consumo.
- Garantir a compatibilidade do sistema com dispositivos móveis e desktops, permitindo acesso remoto e flexível para os gestores.

---

## Justificativa

- A gestão de estoque em pequenas pizzarias frequentemente é realizada de forma manual ou com ferramentas genéricas que não atendem às necessidades específicas do segmento, como o controle dinâmico de insumos perecíveis, reposição em tempo hábil e relatórios personalizados de consumo. Essa realidade compromete a eficiência operacional, aumenta o desperdício, reduz a margem de lucro e afeta a satisfação do cliente.

- Nesse contexto, torna-se viável a criação de um sistema Web responsivo capaz de automatizar a entrada e saída de produtos, emitir alertas e gerar relatórios detalhados.

- O projeto se destaca ao propor uma solução simples e acessível voltada para um nicho específico, contribuindo para a melhoria na gestão interna das pizzarias. Esses resultados poderão servir de base para futuros aprimoramentos e adaptações em outros estabelecimentos de pequeno porte.

---

## Escopo

- O escopo do projeto compreende o desenvolvimento de um sistema web responsivo para o gerenciamento de estoque em pizzarias. O objetivo é proporcionar uma ferramenta prática, acessível e funcional que auxilie na organização de insumos, controle de movimentações e apoio à tomada de decisão.

**As funcionalidades incluídas nessa versão do sistema são:**

- Cadastro de produtos e insumos;
- Controle de entrada e saída de estoque com registro automático;
- Notificação para reposição em níveis críticos;
- Geração de relatórios de consumo e movimentações;
- Interface web responsiva para desktop e dispositivos móveis;
- Controle de acesso por perfis de usuário.

Não está incluído: sistema de pagamentos, gerenciamento de entregadores, previsão de demanda com inteligência artificial e suporte multilíngue. Esses itens poderão ser considerados em versões futuras da ferramenta.

---

## Metodologia

- O trabalho caracteriza-se como uma pesquisa **aplicada**, com abordagem **quali-quantitativa**, visando desenvolver uma solução tecnológica concreta para um problema específico.
- Será usado o **método de desenvolvimento iterativo**, com validação contínua em entregas parciais. A abordagem será baseada em **Scrum**, adaptada ao contexto acadêmico, com sprints curtos e metas claras.

**Tecnologias utilizadas**

- **Backend:** Python com Django
- **Frontend:** Templates do Django com **Tailwind CSS**
- **Banco de dados:** SQLite
- **Hospedagem:** _A decidir_ (Heroku / PythonAnywhere / VPS)
- **Controle de versão:** Git + GitHub
- **Autenticação:** Sistema de usuários do próprio Django
- **Conteinerização:** Docker e Docker-compose

Essa escolha prioriza simplicidade na configuração, agilidade no desenvolvimento e um visual moderno e responsivo com Tailwind CSS.

---

## Recursos necessários

**Tecnológicos**

- Computador com internet
- Editor de código (VS Code ou similar)
- Git + GitHub
- Ambiente Python com Django
- Tailwind CSS integrado ao Django (via PostCSS ou CDN, conforme escolha)
  **Conhecimentos**
- Python / Django (modelos, views, templates, autenticação)
- HTML + Tailwind CSS
- SQL básico (SQLite)
  **Outros**
- Documentação oficial do Django e Tailwind
- Materiais de referência acadêmica e técnica

---

## Riscos

| **Risco Identificado**                           | **Probabilidade** | **Impacto** | **Plano de Mitigação**                                                        |
| ------------------------------------------------ | ----------------- | ----------- | ----------------------------------------------------------------------------- |
| Dificuldade na integração de Tailwind com Django | Média             | Média       | Realizar testes prévios e seguir documentação oficial do Tailwind para Django |
| Falta de tempo devido a outras obrigações        | Alta              | Alta        | Planejar cronograma realista e priorizar funcionalidades principais           |
| Problemas na implantação (hospedagem)            | Média             | Média       | Realizar testes em serviços gratuitos previamente                             |
| Perda de código ou dados                         | Baixa             | Alta        | Uso rigoroso de Git/GitHub e backups regulares                                |

---

## Produto final / Entregáveis

- **Sistema Web Funcional**
  - Módulo de cadastro de produtos e categorias
  - Controle de movimentações
  - Relatórios e notificações
  - Interface responsiva com Tailwind CSS
- **Banco de dados relacional (SQLite)**
- **Documentação técnica e acadêmica**
- **Apresentação final**

---

## Critérios de sucesso

1. Sistema funcionando com todos os módulos principais.
2. Interface responsiva com Tailwind CSS em desktops e dispositivos móveis.
3. Geração de relatórios automáticos.
4. Satisfação mínima de 80% dos usuários colaboradores.
5. Redução de pelo menos 20% no desperdício de insumos.
6. Entrega dentro dos prazos planejados.
7. Documentação completa.

