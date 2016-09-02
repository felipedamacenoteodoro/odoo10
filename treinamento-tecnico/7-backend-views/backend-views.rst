Backend Views
=============

Introdução
----------
Neste módulo serão apresentados os seguintes tópicos:

* Adicionando um item ao menu e janelas de ações
* Ação para abrir uma visão específica
* Adicionando conteúdo e ações em uma view formulário
* Adicionando botões em formulários
* Passando parâmetros para formulários e ações: Contexto
* Definição de filtros em listas de gravação: Domínio
* Views Lista
* Views pesquisa
* Alterar views existentes: View herança

.. nextslide::

* Document-style em formulários
* Elementos de formulário dinâmico usando attrs
* Views embutidas
* Views Kanban
* Mostrar cartões Kanban em colunas de acordo com seu estado
* As visualizações do calendário e gantt
* As visualizações Gráfico e de articulação
* Relatórios Qweb

.. nextslide::


Adicionando um item ao menu e janelas de ações
----------------------------------------------

No XML do nosso módulo, siga os seguintes passos:

1. Defina uma ação a ser executada:

.. code-block:: python

	<act_window id="action_all_customers"
		name="All customers"
		res_model="res.partner"
		view_mode="tree,form"
		domain="[('customer', '=', True)]"
		context="{'default_customer': True}"
		limit="80" />

2. Crie a estrutura do menu:

.. code-block:: python

	<menuitem id="menu_custom_toplevel"
		name="My custom menu" />
	<menuitem id="menu_custom_left"
		parent="menu_custom_toplevel"
		name="This will appear in the left bar" />

.. nextslide::

3. Referencie a ação no menu:

.. code-block:: python

	<menuitem id="menu_all_customers"
		parent="menu_custom_left"
		action="action_all_customers"
		sequence="10"
		groups="" />



*Atualize o módulo para ver as alterções*

Ação para abrir uma visão específica
------------------------------------

Window actions automáticamente determinam a view que será usada, mas as vezes, precisamos que a ação abra uma view específica.

Vamos criar um formulário básico para o modelo de parceiros e criar uma window action específica para ela.

.. nextslide::

1. Definir o formulário mínimo para a visão:

.. code-block:: xml

	<record id="form_all_customers" model="ir.ui.view">
	<field name="name">All customers</field>
	<field name="model">res.partner</field>
	<field name="arch" type="xml">
		<form>
			<group>
				<field name="name" />
			</group>
		</form>
	</field>
	</record>


.. nextslide::

2. Diga a ação do formulário anterior para usar isto:

.. code-block:: xml

	<record id="action_all_customers_form"
			model="ir.actions.act_window.view">
		<field name="act_window_id" ref="action_all_customers" />
		<field name="view_id" ref="form_all_customers" />
		<field name="view_mode">form</field>
		<fieldn ame="sequence">10</field>
	</record>



Adicionando conteúdo e ações em uma view formulário
---------------------------------------------------

O tópico anterior mostrou como escolher uma visão específica para uma ação. Agora, vamos demonstrar
como tornar este formulário mais útil.


1. Defina a estrutura básica da view do formulário:

.. code-block:: xml

	<record id="form_all_customers" model="ir.ui.view">
		<field name="name">All customers</field>
		<field name="model">res.partner</field>
		<field name="arch" type="xml">
			<form>
				<!--conteúdo do formulário aqui -->
			</form>
		</field>
	</record>

.. nextslide::

2. Adicione uma head bar, utilizada para botões e pipeline de estágios:

.. code-block:: html

	<header>
		<button type="object"
			name="open_commercial_entity"
			string="Open commercial partner"
			class="oe_highlight" />
	</header>

3. Adicione campos ao formulário, usando group tags para visualizar e organizar:

.. code-block:: xml

	<group string="Content" name="my_content">
		<field name="name" />
		<field name="category_id" widget="many2many_tags" />
	</group>




Adicionando botões em formulários
---------------------------------

Já adicionamos botões no tópico anterior, mas existem diversos tipos de botões que podemos utilizar
no Odoo. 

Os os atributos type do botão determina a semântica utilizada por outros campos, veja os tipos possíveis
de valores para o botão:

* *action*

* *object*

* *workflow*

.. nextslide::

Vamos criar um botão que referencie a uma ação específica.

Adicione o botão no elemento header do formulário:

.. code-block:: xml

	<button type="action" name="%(base.action_partner_category_form)d"
		string="Open partner categories" />


Passando parâmetros para formulários e ações: Contexto
------------------------------------------------------

1. Criar uma nova ação, muito similar a do primeiro formulário que criamos:

.. code-block:: xml

	<act_window id="action_all_customers_fr"
		name="Tous les clients"
		res_model="res.partner"
		domain="[('customer', '=', True)]"
		context="{'lang': 'fr_FR', 'default_lang': 'fr_FR',
			'active_test': False}" />


2. Adicione um menu que chamará essa action

*Este passo será utilizado como um exercício que vocês deverão realizar sozinhos*



Definição de filtros em listas de gravação: Domínio
---------------------------------------------------

Vamos exibir um conjunto de parceiros na sua ação.


1. Adicionar uma ação para os parceiros que não são franceses:

.. code-block:: xml

	<record id="action_my_customers" model="ir.actions.act_window">
		<field name="name">
			All customers who don't speak French
		</field>
		<field name="res_model">res.partner</field>
		<field name="domain">
			[('customer', '=', True), ('user_id', '=', uid), ('lang',
			'!=', 'fr_FR')]
		</field>
	</record>

.. nextslide::

2. Adicione uma action de clientes que são clientes ou fornecedores:

.. code-block:: xml

	<record id="action_customers_or_suppliers"
			model="ir.actions.act_window">
		<field name="name">Customers or suppliers</field>
		<field name="res_model">res.partner</field>
		<field name="domain">
			['|', ('customer', '=', True), ('supplier', '=', True)]
		</field>
	</record>


3. Adicione menus que chamarão essa action:

*Este passo será utilizado como um exercício que vocês deverão realizar sozinhos*




Views Lista
-----------

1. Defina sua visão lista

.. code-block:: xml

	<record id="tree_all_customers" model="ir.ui.view">
		<field name="model">res.partner</field>
		<field name="arch" type="xml">
			<tree colors="blue: customer and supplier;
					green:customer;
					red: supplier">
				<field name="name" />
				<field name="customer" invisible="1" />
				<field name="supplier" invisible="1" />
			</tree>
		</field>
	</record>

2.	 Tell the action from the first recipe to use it:

.. code-block:: xml

	<record id="action_all_customers_tree" model="ir.actions.act_window.view">
		<field name="act_window_id" ref="action_all_customers" />
		<field name="view_id" ref="tree_all_customers" />
		<field name="sequence">5</field>
	</record>


Views pesquisa
--------------

1. Defina sua view de pesquisa

.. code-block:: xml

    <record id="search_all_customers" model="ir.ui.view">
        <field name="model">res.partner</field>
        <field name="arch" type="xml">
            <search>
                <field name="name" />
                <field name="category_id" filter_domain="[('category_id', 'child_of', self)]" />
                <field name="bank_ids" widget="many2one" />
                <filter name="suppliers" string="Suppliers" domain="[('supplier', '=', True)]" />
            </search>
        </field>
    </record>

.. nextslide::

2. Diga a sua ação para usar isto:

.. code-block:: xml

    <record id="action_all_customers" model="ir.actions.act_window">
        <field name="name">All customers</field>
        <field name="res_model">res.partner</field>
        <field name="domain">[('customer', '=', True)]</field>
        <field name="search_view_id" ref="search_all_customers" />
    </record>


Alterar views existentes: View herança
--------------------------------------

1. Injete o campo na visão formulário default:

.. code-block:: xml

    <record id="view_partner_form" model="ir.ui.view">
        <field name="model">res.partner</field>
        <field name="inherit_id" ref="base.view_partner_form" />
        <field name="arch" type="xml">
            <field name="website" position="after">
                <field name="write_date" />
            </field>
        </field>
    </record>


.. nextslide::

2. Adicione o campo para a view de busca default:

.. code-block:: xml

    <record id="view_res_partner_filter" model="ir.ui.view">
        <field name="model">res.partner</field>
        <field name="inherit_id" ref="base.view_res_partner_filter" />
        <field name="arch" type="xml">
            <xpath expr="." position="inside">
                <field name="write_date" />
            </xpath>
        </field>
    </record>

.. nextslide::

3. Adicione o campo para a visão lista default:


.. code-block:: xml

    <record id="view_partner_tree" model="ir.ui.view">
        <field name="model">res.partner</field>
        <field name="inherit_id" ref="base.view_partner_tree" />
        <field name="arch" type="xml">
            <field name="email" position="before">
                <field name="write_date" />
            </field>
        </field>
    </record>




Document-style em formulários
-----------------------------

Vamos melhorar a apresentação do formulário para o usuário.

1. Inincie seu formulário com o elemento header:

.. code-block:: xml

    <header>
        <button name="do_something_with_the_record" string="Do something" type="object"
                class="oe_highlight" />
        <button name="do_something_else" string="Second action" />
        <field name="state" widget="statusbar" />
    </header>

.. nextslide::

2. Então, adicione o elemento sheet:

.. code-block:: xml

    <sheet>


3. Primeiro, adicione alguns campos identificados:

.. code-block:: xml

    <div class="oe_left oe_title">
        <label for="name" />
            <h1>
                <field name="name" />
            </h1>
    </div>

.. nextslide::


4. Adicione botões que apontam para recursos relevantes para o objeto em sua própria caixa (se aplicável):

.. code-block:: xml

    <div class="oe_right oe_button_box" name="buttons">
        <button name="open_something_interesting"
            string="Open some linked record"
            type="object" class="oe_stat_button" />


5. Acrescente conteúdo:

.. code-block:: xml

    <group name="some_fields">
        <field name="field1" />
        <field name="field2" />
    </group>

.. nextslide::


6. Após a folha, adicione o widget Chatter (se aplicável)::

.. code-block:: xml
    
    </sheet>
    <div class="oe_chatter">
        <field name="message_follower_ids" widget="mail_followers"/>
        <field name="message_ids" widget="mail_thread"/>
    </div>


Elementos de formulário dinâmico usando attrs
---------------------------------------------


1. Defina um atributo attrs em algum elemento do formulário:

.. code-block:: xml

        <field name="parent_id"
            attrs="{'invisible': [('is_company', '=', True)],
        'required': [('is_company', '=', False)]}" />


2. Tome cuidado para que todos os campos que os quais você refere estão disponíveis no formulário::

.. code-block:: xml

    <field name="is_company" invisible="True" />


*Isso fará com que o parent_id seja um campo invisível se o parceiro é uma empresa, e exibir, se não é uma empresa.*


Views embutidas
---------------

Quando você mostra um campo one2many ou many2many em um formulário, você não tem muito controle sobre como ele
é processado se você não tiver usado um dos widgets especializados.

Neste tópico, vamos ver como definir private views para esses campos.

.. code-block:: xml

    <field name="child_ids">
        <tree>
            <field name="name" />
            <field name="email" />
            <field name="phone" />
        </tree>
        <form>
            <group>
                <field name="name" />
                <field name="function" />
            </group>
        </form>
    </field>

Views Kanban
------------

1. Defina uma visão kanban

.. code-block:: xml

    <record id="kanban_all_customers" model="ir.ui.view">
        <field name="model">res.partner</field>
        <field name="arch" type="xml">
        <kanban>

2. List os campos que você irá utilizar na view:

.. code-block:: xml

            <field name="name" />
            <field name="supplier" />
            <field name="customer" />

.. nextslide::

3. Ajuste o design:

.. code-block:: xml

            <templates>
                <t t-name="kanban-box">
                    <div class="oe_kanban_card">
                        <a type="open">
                            <field name="name" />
                        </a>
                        <t t-if="record.supplier.raw_value or
                            record.customer.raw_value">
                            is
                            <t t-if="record.customer.raw_value">
                                a customer
                                <t t-if="record.supplier.
                                    raw_value"> and </t>
                            </t>
                            <t t-if="record.supplier.raw_value">
                                a supplier
                            </t>
                        </t>
                    </div>
                </t>
            </templates>
        </kanban>
    </field>
</record>

.. nextslide::

4. Adicione essa view em uma das suas ações.

*Este passo será utilizado como um exercício que vocês deverão realizar sozinhos*


Mostrar cartões Kanban em colunas de acordo com seu estado
----------------------------------------------------------

As visualizações do calendário e gantt
--------------------------------------

As visualizações Gráfico e de articulação
-----------------------------------------

Relatórios Qweb
---------------
