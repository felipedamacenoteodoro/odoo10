Desenvolvimento Avançado
========================

Alterar o usuário através de uma ação
-------------------------------------
As vezes é necessário que uma ação seja executada com um contexto de segurança diferente. 
Como por exemplo, executar uma ação como administrador. 

Vamos utilizar um usuário comum e modificar o número do telefone de uma empresa usando sudo().

1. Definir um modelo qu extenda o modelo res_company:

.. code-block:: python

	class ResCompany(models.Model):
		_inherit = 'res.company'

2. Criar um método chamado update_phone_number():

.. code-block:: python

	@api.multi
	def update_phone_number(self, new_number):

.. nextslide::


3. Dentro do método, tenha certeza que a ação está sendo executada em um simples registro

.. code-block:: python

		self.ensure_one()


4. Modifique o usuário do ambiente:

.. code-block:: python

	company_as_superuser = self.sudo()

5. Escreva o novo número de telefone:

.. code-block:: python

	company_as_superuser.phone = new_number

.. nextslide::

Se você precisar de um usuário específico, 
pode utilizar um recordset contendo o usuário ou o id do usuário no banco de dados. Ex. utilizando o usuário "public_user"


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

.. code-block:: python

	class ProductProduct(models.Model):
		_inherit = 'product.product'

2. Crie um método chamado stock_in_location():

.. code-block:: python

	@api.model
	def stock_in_location(self, location):

.. nextslide ::

3. Dentro do método, recupere um registro product.product:

.. code-block:: python

	product_in_loc = self.with_context(
		location=location.id,
		active_test=False
	)


4. Busque todos os produtos:

.. code-block:: python

	all_products = product_in_loc.search([])

.. nextslide :: 
5. Crie um array com o nome do produto e o nível de estoque de todos os produtos presente no local especificado:

.. code-block:: python

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

1. Escreva uma classe que estenda res.partner:

.. code-block:: python

	class ResPartner(models.Model):
		_inherit = 'res.partner'

2. Crie um método chamado partners_by_country():

.. code-block:: python

	@api.model:
	def partners_by_country(self):


3. Dentro do método, escreva a sua query:

.. code-block:: python

	sql = ('SELECT country_id, array_agg(id) '
		'FROM res_partner '
		'WHERE active=true AND country_id IS NOT NULL '
		'GROUP BY country_id')

.. nextslide::

4. Execute a query:

.. code-block:: python

	self.env.cr.execute(sql)

5. Interagir com o resultado da query para popular o dict:

.. code-block:: python

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

.. nextslide::

O método utilizado não retorna nada. Isso faz com que a caixa do wizard seja fechada após a execução
da ação. Uma possíbildiade é ter um método que retorno um dict com os campos de um ir.action. Neste
caso, o cliente web irá processar a ação se algum item de menu for clicado pelo usuário.

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


Definir métodos de onchange
---------------------------

Chamar o método onchange no lado do servidor
--------------------------------------------

Portar o código da API antiga para a Nova
-----------------------------------------
