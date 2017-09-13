Ferramentas do desenvolvedor
============================

Ativando o modo desenvolvedor
-----------------------------

1. Conecte em seu banco de dados (Não é necessário se conectar como admim, esta função esta disponível para todos os usuários, mas o admin tem mais ferramentas)
2. Clique no menu **Settings**
3. No lado inferior direito clique em **Activate developer mode**

.. code-block:: python

    # Tambem é possibel ativar o modo desenvolvedor alterando a URL:
    # Antes do # sign, insira: ?debug=. Por exemplo:
    http://localhost:8069/web#menu_id=102&action=94
    # Altere para:
    http://localhost:8069/web?debug=#menu_id=102&action=94

Quando ativo
------------
- Acesso a configurações técnicas;
- O JavaScript e o CSS não são compactados;
- Você recebe dicas ao colocar o cursor em cima de um campo: nome tecnico, tipo e etc;
- Um menu drop-down é exibido no topo com informações tecnicas, sobre o modelo exibido, as visões, ações, workflows, filtros e etc.


Configurações Técnicas
----------------------
Acesse cada um dos menus abaixo, eles são ferramentas muito úteis durante o desenvolvimento:

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
