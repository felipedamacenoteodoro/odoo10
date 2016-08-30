Introdução a Criação de modulos
===============================

Introdução
----------

**Objetivo:** Entender como um modulo Odoo é estruturado, seus componentes e
como realizar o desenvolvimento incremental do mesmo.


Criando e instalando um novo modulo
-----------------------------------

.. code-block:: shell

    cd specific-parts
    mkdir meu_modulo
    cd meu_modulo
    touch __init__.py
    nano __openerp__.py

- Adicione no aquivo __openerp__.py um dicionário

.. code-block:: python

    {'name': 'Meu modulo'}

.. nextslide::

1. Inicie o odoo
2. Ative o modo desenvolvedor
3. Acesse configurações > Atualizar lista de modulos ( Devemos fazer isso sempre que um novo modulo é disponibilizado em um banco de dados )
4. Procure seu modulo na lista de modulos e o instale-o.

.. nextslide::

- Um modulo odoo é um diretório contendo arquivos;
- O nome da pasta é o nome tecnico;
- O 'name' definido no dicionário do manifesto é o Titulo do modulo.
- O arquivo __openerp__.py é o manifesto do modulo. Ele contem um dicionário com os detalhes do modulo: descrição, dependencias, data que deve ser carregada e etc;
- O diretorio deve ser importável pelo python, ou seja ter um arquivo __init__.py mesmo que vazio. Ele tambem pode conter os modulos python e submodulos que devem ser importados.

Arquivo de Manifesto
--------------------
1. Preencha seu arquivo de manifesto com as chaves mais significativas conforme o exemplo:

.. code-block:: python

    # -*- coding: utf-8 -*-
    {
        'name': "Title",
        'summary': "Short subtitle phrase",
        'description': """Long description""",
        'author': "Your name",
        'license': "AGPL-3",
        'website': "http://www.example.com",
        'category': 'Uncategorized',
        'version': '8.0.1.0.0',
        'depends': ['base'],
        'data': ['views.xml'],
        'demo': ['demo.xml'],
    }

.. nextslide::

2. Defina um icone para o seu modulo, copiando uma imagem PNG para a pasta
static/description/icon.png

- O trecho -*- coding: utf-8 -*- permite que utilizemos caracteres não ASCII no arquivo.
- **name:** O titulo do modulo
- **summary:** Um subtitulo com uma linha
- **description:** Deve ser escrito no padrão `ReStructuredText <http://docutils.sourceforge.net/docs/user/rst/quickstart.html>`_
- **author:** O nome dos autores separados por virgula.
- **license:** AGPL-3 , LGPL-3 , Other OSI approved license etc.
- **website:** Url para dar mais informações sobre os autores
- **category:** `Lista de categorias possiveis <https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml>`_

.. nextslide::

- **versao:** Versão do modulo
- **depends:** É uma lista de com os nomes tecnicos que este modulo depende.

**Importante:** Se não depender de nenhum modulo, ao menos deve depender do modulo **base**

Qualquer referencia que seu modulo realize com xmls ids, visões ou modelos refenciados por este modulo.

Esta lista garante que tudo será carregado na ordem correta.

.. nextslide::

- **data:** Lista dos caminhos dos arquivos de dados
- **demo:** Lista dos caminhos dos arquivos de demo


Estrutura de arquivos do modulo
-------------------------------

Crie os arquivos:

.. code-block:: shell

    cd path/to/my-module
    mkdir models
    touch models/__init__.py
    mkdir controllers
    touch controllers/__init__.py
    mkdir views
    mkdir security
    mkdir data
    mkdir demo
    mkdir i18n
    mkdir -p static/description

.. nextslide::

Edite o arquivo __init__.py com os dados:

.. code-block:: python

    # -*- coding: utf-8 -*-
    from . import models
    from . import controllers


.. nextslide::

.. code-block:: shell

    .
    ├── __init__.py
    ├── __openerp__.py
    │
    ├── controllers
    │
    └── __init__.py
    ├── data
    ├── i18n
    ├── models
    │
    └── __init__.py
    ├── security
    ├── static
    │
    └── description
    └── views

.. nextslide::

Um modudo Odoo pode conter três tipos de aquivos:

- Arquivos python
- Arquivos de dados: XML / CSV / YML
- Arquivos Web: Css / Qweb / HTML


Adicionando modelos
-------------------

Crie um arquivo na pasta models, chamado de meu_modulo.py Com o conteudo:

.. code-block:: python

    # -*- coding: utf-8 -*-

    from openerp import models, fields

    class MeuModulo(models.Model):

        _name = 'meu.modulo'

        name = fields.Char(u'Nome', required=True)
        date = fields.Date('Date')
        partner_ids = fields.Many2many('res.partner',
        string='Parceiro')

Crie um arquivo __init__.py na pasta models importando o seu modulo:

.. code-block:: python

    from . import meu_modulo

.. nextslide::

Edite o arquivo __init__.py da raiz para importar a pasta models:

.. code-block:: python

    from . import models


.. nextslide::

- Modelos Odoo são objetos derivados da classe Odoo Model.
- Quando um novo modulo é definido ele é adicionado a tabela de modelos (ir_model)
- Modelos tem alguns atributos definidos com underline. O mais importante é o _name que define um identificador unico do modelo na intancia
- As mudanças nos Modelos são carregadas quando atualizamos os modulos;

Atualize seu modulo e verifique o banco de dados foi alterado e as tabelas de dados.


Adicionando Menus e visões
--------------------------

Crie um arquivo de visão na pasta views/meu_modulo.xml com o conteudo:

.. code-block:: xml

    <?xml version="1.0" encoding="utf-8"?>
    <openerp>
        <data>
            <act_window
                id="meu_modulo_action"
                name="Minha Ação"
                res_model="meu.modulo" />

            <menuitem
                id="meu_modulo_menu"
                name="Meu Menu"
                action="meu_modulo_action"
                parent=""
                sequence="5" />
        </data>
    </openerp>

Adicione o na sessão data no arquivo __openerp__.py

.. code-block:: xml

    'data': ['views/meu_modulo.xml'],

.. nextslide::

Complete o arquivo de dados:

.. code-block:: xml

    <act_window
        id="meu_modulo_action"
        name="Minha Ação"
        res_model="meu.modulo" />

    <menuitem
        id="meu_modulo_menu"
        name="Meu Menu"
        action="meu_modulo_action"
        parent=""
        sequence="5" />


.. nextslide::

Atualize seu modulo e verifique as alterações


.. nextslide::

Defina um formulário personalizado.

.. code-block:: xml

     <record id="meu_modulo_view_form" model="ir.ui.view">
        <field name="name">Meu modulo Form</field>
        <field name="model">meu.modulo</field>
        <field name="arch" type="xml">
            <form>
                <group>
                    <field name="name"/>
                    <field name="partner_ids" widget="many2many_tags"/>
                </group>
                <group>
                    <field name="date"/>
                </group>
            </form>
        </field>
     </record>

.. nextslide::

Defina uma visão lista

.. code-block:: xml

    <record id="meu_modulo_view_tree" model="ir.ui.view">
    <field name="name">Meu Modulo List</field>
    <field name="model">meu.modulo</field>
        <field name="arch" type="xml">
            <tree>
                <field name="name"/>
                <field name="date"/>
            </tree>
        </field>
    </record>


.. nextslide::

Defina uma busca personalizada

.. code-block:: xml

    <record id="meu_modulo_view_search" model="ir.ui.view">
        <field name="name">Meu modulo Search</field>
        <field name="model">meu.modulo</field>
        <field name="arch" type="xml">
            <search>
                <field name="name"/>
                <field name="partner_ids"/>
                <filter string="S/ Parceiros"
                    domain="[('partner_ids','=',False)]"/>
            </search>
        </field>
    </record>

Criando modulos a partir de um template
---------------------------------------

.. code-block:: python

    No buildout
    cd parts/server
    ./odoo.py scaffold teste /tmp/

    ls /tmp/teste
