Desenvolvimento Avançado
========================

Alterar o usuário através de uma ação
-------------------------------------
As vezes é necessário que uma ação seja executada com um contexto de segurança diferente. 
Como por exemplo, executar uma ação como administrador. 

Vamos utilizar um usuário comum e modificar o número do telefone de uma empresa usando sudo().

1. Definir um modelo qu extenda o modelo res_company
2. Criar um método chamado update_phone_number()
3. Dentro do método, tenha certeza que a ação está sendo executada em um simples registro
4. Modifique o usuário do ambiente:


.. code-block:: python

	class ResCompany(models.Model):
		_inherit = 'res.company'

	@api.multi
	def update_phone_number(self, new_number):
          self.ensure_one()
          company_as_superuser = self.sudo()
          company_as_superuser.phone = new_number

.. nextslide::

Se você precisar de um usuário específico, pode utilizar um recordset contendo o
 usuário ou o id do usuário no banco de dados. Ex. utilizando o usuário "public_user"

.. code-block:: python

	public_user = self.env.ref('base.public_user')
	public_book = self.env['library.book'].sudo(public_user)


Chamar um metódo com um contexto modificado
-------------------------------------------

O context é parte do ambiente de um recordset. É utilizado para passar informações como timezone
ou idioma do usuário a partir da interface ou em parametros especificados em uma action. 

.. nextslide::

Para iniciarmos, vamos utilizar o addons stock e product. Abaixo, uma versão simplificada do modelo
product.product.

.. code-block:: python

	class product.product(models.Model):
		_name = 'product.product'
		name = fields.Char('Name', required=True)
		qty_available = fields.Float('Quantity on Hand',
					compute='_product_available')
		def _product_available(self):
			"""if context contains a key 'location' linked to a
			database id, then the stock available is computed within
			that location only. Otherwise the stock of all internal
			locations is computed"""
			pass # read the real source in addons/stock/product.py :)


.. nextslide ::

Para calcular os níveis de estoque de todos os produtos de um determinado local,
siga os passos abaixo.

1. Crie um modelo que estenda product.product
2. Crie um método chamado stock_in_location():
3. Dentro do método, recupere um registro product.product:
4. Busque todos os produtos:
5. Crie um array com o nome do produto e o nível de estoque de todos os produtos presente no local especificado
6. Verifique o resultado da chamada do metodo através do ipython

.. code-block:: python

     class ProductProduct(models.Model):
          _inherit = 'product.product'

          @api.model
          def stock_in_location(self, location):
               product_in_loc = self.with_context(
                    location=location.id,
                    active_test=False
               )
               all_products = product_in_loc.search([])

               stock_levels = []
               for product in all_products:
                    if product.qty_available:
                         stock_levels.append((product.name,
                         product.qty_available))
               return stock_levels

Executar um query SQL
---------------------

Quando não for possível utilizar o método search() em uma operação, vocÊ pode executar
queries SQL diretamente no Odoo. Por exemplo, vamos exibir os registros res.partner agrupados
por país. Vamos utilizar uma versão simplificada do modelo res.partner:

.. code-block:: python

	class ResPartner(models.Model):

		_name = 'res.partner'

		name = fields.Char('Name', required=True)
		email = fields.Char('Email')
		is_company = fields.Boolean('Is a company')
		parent_id = fields.Many2one('res.partner', 'Related Company')
		child_ids = fields.One2many('res.partner', 'parent_id',
					'Contacts')
		country_id = fields.Many2one('res.country', 'Country')

.. nextslide::

1. Escreva uma classe que estenda res.partner
2. Crie um método chamado partners_by_country()
3. Verifique o resultado da chamada do metodo através do ipython

.. code-block:: python

	class ResPartner(models.Model):
		_inherit = 'res.partner'

     @api.model:
     def partners_by_country(self):
          sql = ('SELECT country_id, array_agg(id) '
             'FROM res_partner '
             'WHERE active=true AND country_id IS NOT NULL '
             'GROUP BY country_id')
          self.env.cr.execute(sql)
         country_model = self.env['res.country']
         result = {}
         for country_id, partner_ids in self.env.cr.fetchall():
             country = country_model.browse(country_id)
             partners = self.search(
                 [('id', 'in', tuple(partner_ids))]
             )
             result[country] = partners
         return result

Wizard
------

Criação de um assistente para guiar o usuário em uma atividade.

Iremos utilizar um modelo simples para 'record book loans':

.. code-block:: python

	class LibraryBookLoan(models.Model):
		_name = 'library.book.loan'
		book_id = fields.Many2one('library.book', 'Book',
				required=True)
        member_id = fields.Many2one('library.member', 'Borrower',
				required=True)
        state = fields.Selection([('ongoing', 'Ongoing'),
				('done', Done')],
				'State',
				default='ongoing', required=True)

.. nextslide::

1. Crie um novo modelo transitório para o módulo:

.. code-block:: python

	class LibraryLoanWizard(models.TransientModel):

	    _name = 'library.loan.wizard'
	    member_id = fields.Many2one('library.member', 'Member')
	    book_ids = fields.Many2many('library.book', 'Books')


2. Crie um método callback executando uma ação no modelo transitório. 
Adicione o código abaixo na classe LibraryLoanWizard :

.. code-block:: python

	@api.multi
	def record_loans(self):
		for wizard in self:
		member = wizard.member_id
		books = wizard.book_ids
		loan = self.env['library.book.loan']
		for book in wizard.book_ids:
			loan.create({'member_id': member.id,
					'book_id': book.id})

3. Crie um form view para o modelo.

.. nextslide::

.. code-block:: xml

     <record id='library_loan_wizard_form' model='ir.ui.view'>
        <field name='name'>library loan wizard form view</field>
        <field name='model'>library.loan.wizard</field>
        <field name='arch' type='xml'>
            <form string="Borrow books">
                <sheet>
                    <group>
                        <field name='member_id'/>
                    </group>
                    <group>
                        <field name='book_ids'/>
                    </group>
                <sheet>
                <footer>
                    <button name='record_loans'
                        string='OK'
                        class='btn-primary'
                        type='object'/>
                    or
                    <button string='Cancel'
                        class='btn-default'
                        special='cancel'/>
                </footer>
            </form>
        </field>
    </record>

.. nextslide::

4. Crie uma action e uma entrada no menu para exibir o *wizard*. 

.. code-block:: python

    <act_window id="action_wizard_loan_books"
        name="Record Loans"
        res_model="library.loan.wizard"
        view_mode="form"
        target="new"
        />
    <menuitem id="menu_wizard_loan_books"
        parent="library_book_menu"
        action="action_wizard_loan_books"
        sequence="20"
        />

Redirecionando o usuário
------------------------

O método definido no wizard não retorna nada. Isso faz com que a caixa do wizard
seja fechada após a execução da ação. Uma possíbildiade é retorar um dict com os
campos de um ir.action. Neste caso, o cliente web irá processar a ação se como se
algum item de menu fosse clicado pelo usuário.

.. code-block:: python

    @api.multi
    def record_borrows(self):
        for wizard in self:
            member = wizard.member_id
            books = wizard.book_ids
            member.borrow_books(books)
        member_ids = self.mapped('member_id').ids
        action = {
            'type': 'ir.action.act_window',
            'name': 'Borrower',
            'res_model': 'library.member',
            'domain': [('id', '=', member_ids)],
            'view_mode': 'form,tree',
        }
        return action

.. nextslide::

Dica: Este macete pode ser adaptado para criarmos uma sequencia de wizards sendo executados.


Definir métodos de onchange
---------------------------

Quando escrevemos modelos Odoo, há frequentemente a necessidade de que campos
estejam interligados.

Vamos ver agora o conceito de onchange que é um metodo que é chamado quando um campo é modificado na visão.

.. nextslide::

Verificar exemplo feito c/  Luciano de retorno dos livros

.. code-block:: python

    class LibraryReturnsWizard(models.TransientModel):
        _name = 'library.returns.wizard'
        member_id = fields.Many2one('library.member', 'Member')
        book_ids = fields.Many2many('library.book', 'Books')
        @api.multi
        def record_returns(self):
            loan = self.env['library.book.loan']
            for rec in self:
                loans = loan.search(
                    [('state', '=', 'ongoing'),
                        ('book_id', 'in', rec.book_ids.ids),
                        ('member_id', '=', rec.member_id.id)]
                        )
                loans.write({'state': 'done'})

.. nextslide::

Para popular automáticamente a lista de livro quando o usuário mudar, é necessário adicionar
o método onchange em LibraryReturnsWizard:

.. code-block:: python

	@api.onchange('member_id')
	def onchange_member(self):
		loan = self.env['library.book.loan']
		loans = loan.search(
			[('state', '=', 'ongoing'),
			('member_id', '=', self.member_id.id)]
		)
		self.book_ids = loans.mapped('book_id')


.. nextslide::

- Quando o seu metodo de onchange estiver sendo executado, você tem acesso aos campos exibidos na visão atual, mas não necessáriamente todos os campos do modelo.
- Isto acontece por que os on changes podem ser chamados quando um registro esta sendo criado pelo usuário antes mesmo de ser salvo no banco de dados.
- Você não deve realizar transações dentro de metodos onchange, nunca deve persistir dados,visto que se o usuário cancelar a ação os dados serão perdidos.
- Adicionalmente os onchanges podem retornar dominios e avisos para o usuário

Method and decorator
====================


Method and decorator
--------------------

Os decoratos são apenas um mapeamento para a nova api.

``api`` namespace decoratos detectarão automaticamente a assinatura dos metodos. verificando se as assinaturas batem com a antiga ou a nova api.

Isto trouxe um pouco de lentidão, a versão 10 será vem mais rapida.

Os nomes reconhecidos são:

``cr, cursor, uid, user, user_id, id, ids, context``


@api.returns
------------

Garante o retorno de um unico recordset.

Ele ira retornar um Recordset de um modelo especifico: ::

    @api.returns('res.partner')
    def afun(self):
        ...
        return x  # a RecordSet

Se uma chamada da antiga api buscar o metodo o retorno sera automaticamente convertido em uma lista de ids.

Todos os decoradores herdam deste decorador para atualizar ou realizar o downgrade do valor retornado.

@api.one ( descontiunado!!!!!!!)
---------------------------

Este decorador automaticamente faz o lool nos recordsets recebidos: ::

  @api.one
  def afun(self):
      self.name = 'toto'

Utilizem o self.ensure_one()

Exemplo de substituição do wizard do emprestimo de livro.

.. note::
   Caution: the returned value is put in a list. This is not always supported by
   the web client, e.g. on button action methods. In that case, you should use
   ``@api.multi`` to decorate your method, and probably call `self.ensure_one()`
   in the method definition.


@api.multi
----------
O Self será o recordset corrente sem interação: ::

   @api.multi
   def afun(self):
       len(self)

@api.model
----------

Este  decorador ira converter uma chamada da antiga API para a nova API.
It allows to be polite when migrating code. ::

    @api.model
    def afun(self):
        pass

@api.constrains
---------------
Este decorador assegura que a função decorada sera chamada no create, write e unlink.

Opcionalmente pode ser realizado um raise para exibir uma mensage. Muita gente esta usando isto
para não precisar sobrescrever o write! Então foi criado um decorator @api.write

@api.depends
------------

Este decorador ira chamar a funçao decorada sempre que um campo especificado na lista
for alterado pelo ORM ou pelo formulário: ::

    @api.depends('name', 'an_other_field')
    def afun(self):
        pass


.. note::
   when you redefine depends you have to redefine all @api.depends,
   so it loses some of his interest.

.. nextslide::

View management
---------------
Um dos grandes avanços da nova API é que os campos com depends e onchange são inseridos automaticamente nas visões.
.. _@api.onchange:

@api.onchange
--------------

Este decorator ira dispar uma chamada a função decora se qualquer campo especificado no decorator
for alterado na visão: ::

  @api.onchange('fieldx')
  def do_stuff(self):
     if self.fieldx == x:
        self.fieldy = 'toto'

No exemplo anterior o campo `self` corresponde ao record atualmente editado.
Durante o on_change toda a execução do contexto é feito no cache. Então você não
precisa de preocupar em alterar o RecordSet dentro da função e alterar o banco de dados.


**Esta é grande diferença se comparado com o ``@api.depends``**

Quando a função retorna, as diferenças entre o cache e o RecordSet são retornados para o form.


@api.noguess
------------

Este decorator ira prevenir a nova API alterar o output do metodo.
