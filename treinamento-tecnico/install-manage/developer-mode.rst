Ferramentas do desenvolvedor
==============================

Ativando o modo desenvolvedor
-----------------------------

1. Conecte em seu banco de dados (Não é necessário se conectar como admim, esta função esta disponível para todos os usuários, mas o admin tem mais ferramentas)
2. Clique na seta proxima ao nome do usuário;
3. No menu acesse **about/sobre**
4. No diálogo exibido, clique em **activate developer mode**

.. code-block:: python

    # Tambem é possibel ativar o modo desenvolvedor alterando a URL:
    # Antes do # sign, insira: ?debug=. Por exemplo:
    http://localhost:8069/web#menu_id=102&action=94
    # Altere para:
    http://localhost:8069/web?debug=#menu_id=102&action=94

Quando ativo
------------

- O JavaScript e o CSS não são compactados;
- Você recebe dicas ao colocar o cursor em cima de um campo: nome tecnico, tipo e etc;
- Um menu drop-down é exibido no topo com informações tecnicas, sobre o modelo exibido, as visões, ações, workflows, filtros e etc.

Configurações tecnicas
----------------------
1. Verifique se seu usuário pertence ao grupo "Procedimentos Tecnicos" (Acesso as configurações do sistema e configuração dos modulos instalados);
2. Acesse Configurações > Configurações.

- Email
- Ações
- Interface de usuário
- Estrutura do banco de dados
- Automação
- Workflows
- Calendário

.. nextslide::

- Relatórios
- Sequencias e identificadores
- Parametros
- Segurança
- Recursos










