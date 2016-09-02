Neste capitulo nós cobriremos os seguintes tópicos:
* Usar estágios e características do Kanban
* Criando ações de servidores
* Adicionando mensagens e características de rastreamento
* Usar código Python em ações de servidores
* Usar ações automatizadas em condições de tempo
* usar ações automatizadas em condições de eventos
* Inspecionar fluxos de trabalho (workflows)

Introdução
==========
Espera-se que aplicações de negócios não sejam apenas repositórios de dados, 
mas também lidar com complexo fluxos de trabalhos de negócios. Odoo inclui um
motor de fluxos de trabalho (engine workflow).

As regras de automação são muito relevantes para a customização e também para
o desenvolvimento de novos módulos de funções adicionais, portanto desenvol-
vedores precisam estar bem familiariazados com as regras de automação. Assim 
pode-se evitar excesso de engenharia em regras de negócios que podem ser
implementados através de customizações funcionais. Algumas destas técnicas 
também podem ser usadas por usuários experientes ou consultores funcionais para
adicionar alguns processos de negócios simples sem a necessidade de criação
de módulos adicionais.

Usando Estágios e Características de Kanban
===========================================
A faixa de Kanban é um método simples de fluxo de trabalho. É organizado em 
colunas, cada uma correspondendo a um estágio, e o progresso dos itens de 
trabalho andam da esquerda para a direita até chegar ao fim.

Existem algumas características usadas em várias faixas de Kanban, provendo
um padrão comum que pode ser usado em nosso próprio módulo. Vamos vê-las:

Se preparando
=============
Para seguir este passo-a-passo, você precisará do módulo de Gerenciamento de
Projetos instalado.

Como fazer ?
============
Para começar a usar a faixa de kanban de projetos faça:

1. Selecione a opção "Projeto" no menu superior e crie um novo Projeto.
2. Dê um nome para o novo projeto e clique no botão "Salvar". Em seguida, 
   pressione o botão "Tarefas" na parte superior direita do formulário.
   Isso abrirá a visão Kanban para as tarefas do projeto.
3. Clique na barra vertical "Adicionar Nova Coluna" a direita, digite "Agora"
   na caixa de diálogo, e clique em "Adicionar". Repita os passos para incluir
   os estágios "Atrasado" e "Completo".
4. Passe o mouse por cima do estágio "Completo" e um ícone de roda dentada
   aparecerá. Clique nela e escolha a opção "Editar".
5. Na janela de "Editar Colunas", marque a opção "Dobrado nas Tarefas" e salve.

Como funciona ?
===============
Kanban é um dos tipos de visão disponíveis, e ela é capaz de organizar itens
agrupados em colunas. Se usarmos estágios os itens de trabalho, nós teremos
um painel Kanban. A lista de estágio pode ser configurada para atender as
necessidades específicas dos usuários.

Estágios devem ter um atributo "Dobrado", significando que a coluna correspon-
dente na visão Kanban deve estar dobrada. É esperado que itens "Em Progresso"
estejam desdobrados na visão Kanban e itens concluídos, normalmente "Feito" ou
"Cancelado", devem estar dobrados.

Cada item de trabalho tem uma referência para o estágio em que está. Também
pode ter um Estado do Kanban, representa por um botão parecido com uma luz 
de sinal de trânsito (ou semelhante), e uma Prioridade, representado por uma
estrela. O cartão Kanban também pode ter um atributo de cor, usado como cor
de fundo.

Enquanto o Estágio representa a situação atual do processo do item de trabalho, 
o "Estado Kanban" provê informações sobre a possibilidade para avançar ao 
próximo estágio. É um campo de "Seleção", normalmente chamado de "kanban_state",
no formulário, e a visualização Kanban é usada com a ferramenta
"kanban_state_selection" e pode ter 3 opções:
* Um valor cinza neutro, o padrão (o valor "normal" no banco de dados)
* Um valor vermelho "Bloqueado" (o valor "blocked" no banco de dados), signifi-
  cando que há alguma razão para reter o item de trabalho no estágio atual.
* Um valor verde "Projeto para o Próximo Estágio" (o valor "done" no banco de
  dados), significando que o item de trabalho está pronto para ser puxado para
  o próximo estágio.
  
O campo "Prioridade" também é um campo de Seleção, e é mostrado com a ferramenta
"priority" no formulário e na vizualização kanban. As opções de seleção são 
esperadas como um número, começando de 0, valor normal (não classificado),
e outros valores para classificações.

E tem mais
==========
Estágios são adicionados ao modelo (models) através de um campo referenciado
Many2one referenciando a um estágio modelo definindo os possíveis estágios.
Na vizualização do formulário, eles podem ser representados com a ajuda de uma
ferramenta barra de estado (statusbar). Para mais detalhes em vizualizações
(views), ferramentas (widgets), e formatando vizualizações Kanban, você pode-se
referir ao Capítulo 8, Visualizações de Back-end.

O estágio de Kanban complementar é suportado por um campo de seleção (Selection)
e sua definição é tipicamente:

  kanban_state = fields.Selection(
      [('normal', 'Normal'), ('blocked', 'Bloqueado'), ('done', 'Pronto para
  o próximo estágio')], 'Estado Kanban', default='normal')
  
Na vizualização do formulário, ele pode ser especificado pela ferramenta
"kanban_state_selection":

  <field name="kanban_state" widget="kanban_state_selection" />
  
Em relação ao campo Prioridade (Priority), também é um campo Seleção (Selection)
e o número de opções normalmente fica entre 2 e 4:

  priority = fields.Selection(
      [('0', 'Normal'), ('1', 'Baixo'), ('2', 'Alto'),
       ('3', 'Urgente')],
      'Prioridade', default='0')
      
Em vizualização de formulários, pode-se usar a ferramenta Prioridade (priority):

  <field name="priority" widget="priority" />
  
Criando ações de servidor (server actions)
==========================================

As ações de servidor sustentam as ferramentas de automação do Odoo. Elas 
permitem escrever ações a serem feitas. Estas ações ficam disponível para 
serem chamados por gatilhos de eventos, ou para serem acionados automaticamente 
quando certas condições de tempo são atingidas.
O caso mais simples é deixar o usuário executar uma ação em um documento sele-
cionando a ação a partir do botão "Mais" dentro do objeto. Nós vamos criar uma 
ação como esta para tarefas de projeto, para "Definir como Prioritário" definir 
uma data final (deadline) para a tarefa selecionada em 3 dias a partir de hoje.

Se preparando
=============
Nós precisaremos de uma instância Odoo com o módulo de Projeto instalado. Nós
também precisaremos do Modo Desenvolvedor ativado. Se não estiver ativado,
ative-o através do menu "Sobre o Odoo".

Como fazer ?
============
Para criar uma ação de servidor e usar a opção "Mais", siga este passo-a-passo:

1. No menu Configurações (Settings), selecione o menu Configurações Técnicas
   (Technical) | Ações (Actions) | Ações de Servidor (Server Actions), e clique
   no botão Criar (Create) no topo da lista de registros.
2. Preencha o formulário de ações de servidor com os seguintes valores:
   * Nome da Ação (Server Action): Definir como Prioritário
   * Modelo (Base Model): Tarefa (Task)
   * Ação (Action To Do): Escrever em um registro (Write On a Record)
   * Política de Atualização (Update Policy): Alterar o registro atual (Update
     the Current Record)
3. Na ação do servidor, debaixo do campo Mapeamento de Valor (Value Mapping), 
   adicione as seguintes linhas:
   * Como o primeiro valor, vamos entrar os seguintes parâmetros:
     * Campo (Field): Prazo Final (Deadline)
     * Tipo de Avaliação (Evaluation Type): Expressão Python (Python expression)
     * Valor (Value): datetime.date.today()+ datetime.timedelta(days=3)
   * Como o segundo valor, vamos entrar os seguintes parâmetros:
     * Campo (Field): Prioridade (Priority)
     * Tipo de Avaliação (Evaluation Type): Valor (Value)
     * Valor (Value): 1
4. Salve a ação de servidore clique em "Adicionar no botão 'Mais'" no canto
   superior direito, para torná-lo disponível no botão Mais na Tarefas de 
   Projetos.
5. Para testá-lo, para o menu Projeto, selecione o menu Busque | Tarefas,
   e abra uma tarefa qualquer. Clicando no botão Mais você deve ver a opção
   "Marque como Prioritário". Selecionando-a vai marcar a estrela da tarefa e
   mudar o prazo final para daqui a 3 dias.
   
Como isso funciona ?
====================
Ações de servidores funcionam como um Modelo (Model), então uma das primeiras
coisas a fazer é definir um Modelo Base (Base Model) que queremos trabalhar.
No nosso exemplo usamos tarefas de projetos.

Depois devemos selecionar o tipo de ação a executar. Existem algumas opções:
* Enviar Email (Send Email) permite enviar emails a partir de modelos (e-mail
  template), e usá-lo para enviar um email quando a ação é disparada.
* Iniciar um Sinal de Fluxo de Trabalho (Trigger a Workflow Signal) faz somente
  isso mesmo, em fluxos de trabalho Odoo, Sinais (Signals) podem ser disparados
  e usados para disparar transições de fluxo de trabalho.
* Executar uma Ação de Cliente (Run a Client Action) dispara um cliente ou uma
  ação de janela (window action), do mesmo jeito quando um item de menu é cli-
  cado.
* Criar ou Copiar um novo Registro (Create or Copy a new Record) permite a você
  criar um novo registro, no modelo atual ou em outro modelo.
* Escrever em um Registro (Write on a Record) permite a você definir valores
  no registro atual ou em outro modelo.
* Executar Código Python (Execute Python Code) permite a você escrever código
  arbitrário a ser executado, quando nenhuma das outras opções é flexível o 
  suficiente para o que precisamos.

Para nosso exemplo, nós usamos "Escrever em um Registro" para definir alguns
valores no registro atual. Nós definimos Prioridade para 1, para ativar uma
estrela na tarefa, e definimos o campo Prazo Máximo. Este é mais interessante,
como o valor a ser definido vem de uma expressão Python. Nosso exemplo faz uso
do módulo python datetime para computar 3 dias a partir de hoje.

Expressões arbitrárias Python podem ser usadas ali, também como em vários outros
tipos de disponíveis. Por razões de segurança, o código é checado pela função 
safe_eval, implementado no Odoo em odoo/openerp/tools/safe_eval.py. Isso signi-
fica que algumas expressões Python podem não ser permitidas, mas isso raramente
gera algum problema.

E tem mais
==========
O código Python é analisado em um contexto restrito, onde os seguintes objetos
estão disponíveis para uso:
* env: Esta é uma referência para o objeto Environment, assim como self.env em
  um método class.
* model: Esta é uma referência para a classe de modelo que a ação de servidor
  tem ação. No nosso exemplo, é o equivalente ao self.env['project.task'].
* workflow: Esta é uma referência para o objeto do motor de fluxo de trabalho do
  Odoo.
* Warning: Esta é uma referência para o openerp.exceptions.Warning, permitindo
  validações que bloqueiem ações não intencionais. Ele pode ser usado como:
  raise Warning('Mensagem!').
* object ou obj: Isto provê referências para o registro atual, permitindo
  acessar seus campos e métodos.
* log: Está é uma função para registrar logs no modelo ir.logging, permitindo
  logar ações no banco de dados.
* datetime, dateutil e time: Isto provê acesso a bibliotecas Python.

   


Adicionando mensagens e rastreamento aos registros
==================================================



Utilizando código Python em ações de servidor
=============================================



Utilizando ações automatizadas baseadas em condições de tempo
=============================================================


Utilizando ações automáticas baseadas em condições de eventos
=============================================================

