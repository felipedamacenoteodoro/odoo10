Atualizando modulos
===================

Instalando/Atualizando modulos
------------------------------

- Interface web;
- Pela linha de comando;


Instalando ( -i init ):

.. code-block:: shell

    bin/start_odoo -d dbname -i addon1,addon2 --stop-after-init

Atualizando ( -u upgrade ):

.. code-block:: shell

    bin/start_odoo -d dbname -u addon1,addon2 --stop-after-init

Instalação de um modulo
-----------------------

1. Se houver executa o script **preinit**;
2. **Carrega** o código Python do módulo, analisa as definições de modelos e se preciso **altera** a estrutura do banco de dados;
3. **Carrega** os dados do módulo;
4. **Carrega** os dados de demonstração se for o caso;
5. Se houver executa o script **postinit**;
6. Valida as visões do módulo;
7. Se os dados de **demonstração** e os **testes** estiverem ativados executa os testes do módulo;
8. Atualiza o status do módulo no banco de dados;
9. Atualiza as traduções do módulo no banco de dados.

Atualização de um módulo
------------------------

1. Se houver executa o script **pré migração**;
2. **Atualiza** o código Python do módulo, analisa as definições de modelos e se preciso **atualiza** a estrutura do banco de dados;
3. **Atualiza** os dados de dados do módulo se necessário;
4. **Atualiza** os dados de demonstração se necessário;
5. Se houver executa o script **pos migração**;
6. Valida as visões do módulo;
7. Se os dados de **demonstração** e os **testes** estiverem ativados executa os testes do módulo;
8. Atualiza a versão do módulo no banco de dados;
9. Atualiza as traduções do módulo no banco de dados.

Notas:
- Ao atualizar um módulo pela linha de comando que não esta instalado: nada ocorre.
- Ao instalar um módulo pela linha de comando que já está instalado: reinstala o módulo e pode causar efeitos indesejados.
