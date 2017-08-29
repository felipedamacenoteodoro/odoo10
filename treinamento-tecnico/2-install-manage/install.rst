Setup ambiente de desenvolvimento
=================================

Pré requisitos:
---------------

- Para se desenvolver Odoo, é recomendável ambiente GNU/Linux;
- É recomendado utilizar a mesma distribuição e versão da produção: **Ubuntu 16.04 LTS**
- Conta no github: https://github.com


Dependencias:
-------------
.. to big

- GNU/Linux;
- PostgreSQL;
- Bibliotecas C;
- Python e Bibliotecas que estendem a stadard library;
- Outras dependências ( reports e outros );

Instalação:
-----------

1. Instalação das dependencias

.. code-block:: shell

	curl -s https://raw.githubusercontent.com/kmee/dependencias.odoo/master/install-dependencies.sh \
            | sudo bash

2. Instalação do postgres

.. code-block:: shell
	curl -s https://raw.githubusercontent.com/kmee/dependencias.odoo/master/install-postgres.sh \
            | sudo bash

3. Permissão do postgres para o seu usuário

.. code-block:: shell

        curl -s https://raw.githubusercontent.com/kmee/dependencias.odoo/master/https://github.com/kmee/dependencias.odoo/blob/master/create-postgres-user.sh \
            | sudo bash

Ambientes virtuais Python
-------------------------

- Python virtual environments, ou **virtualenv** são ambientes de trabalhos python isolados.
- Permitem aos desenvolvedores trabalharem com diferentes versões de bibliotecas python instaladas.
- É possivel criar quantos ambientes forem precisos;

`Documentação oficial <https://virtualenv.pypa.io/en/stable/>`_


Configuração do ambiente de desenvolvimento
-------------------------------------------

.. image:: image/tirinha.png
    :align: center


Buildout: Contruindo ambientes replicáveis (continua)
-----------------------------------------------------
  Na minha maquina funciona

  -- Alonso, desenvolvedor

Buildout é um sistema de *build* baseado em Python para a criação, montagem e
implantação de aplicativos de com vários componentes, alguns dos quais não são
necessáriamente baseados em Python. Ele permite você criar uma "receita" e
replicar o mesmo software posteriormente.

