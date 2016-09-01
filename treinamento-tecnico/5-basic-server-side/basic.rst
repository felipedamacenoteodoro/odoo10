Desenvolvimento Server Side
===========================

Revisão:
--------

Model
#####

- Model é uma representação de um objeto de negócio, sendo que até o momento eles podem ser persistentes e abstratos:

.. code-block:: python

    class A(models.Model):
        ...
    class B(models.AbstractMethod):
        ...

.. nextslide::

- Um model é basicamente uma classe Python! Que define vários atributos:
    - Atributos especiais iniciados com UNDERLINE _name, _rec_name etc;
    - Campos salvos no banco de dados: "variaveis" definidas com fields;
    - O nome do campo no bando de dados é o mesmo nome dado a variavel!

.. code-block:: python

    class A(models.Model):
        _name ='a'
        valor = fields.Float(...)

Recordset
#########
- Um objeto Recordset representa os registros em uma tabela base ou os registros resultantes da execução de uma consulta.

- Quando metodos definidos em um modelo são executados o atributo self é um recorset.

.. code-block:: python

    def do_operation(self):
        print self # => a.model(1, 2, 3, 4, 5)
        for record in self:
            print record # => a.model(1), then a.model(2), then a.model(3), ...

Acesso aos campos
#################

**Recordsets proveem um padrão denominado "Active-Record"**:

Em Engenharia de software, active record é um padrão de projeto encontrado em softwares que armazenam seus dados em Banco de dados relacionais. Assim foi nomeado por Martin Fowler em seu livro Patterns of Enterprise Application Architecture[1].

A interface de um certo objeto deve incluir funções como por exemplo:

- Inserir(Insert) / Atualizar(Update) / Apagar(Delete);
- Propriedades que correspondam de certa forma diretamente às colunas do banco de dados associado.

.. nextslide::

Portanto modelos podem ser escritos e lidos de forma direta através de um record.

Mas somente nos singletons(apenas uma instancia de model). Setar um field dispara um update no banco de dados. Exemplo

.. code-block:: python

    >>> record.name
    Example Name
    >>> record.company_id.name
    Company Name
    >>> record.name = "Bob"
    >>> record.do_operation()


Desenvolvimento Server Side
---------------------------

* Definindo metódos de modelos e usando API decorators
* Saída de erros para os usuários
* Obtendo um recordset para um modelo diferente
* Criando novas records
* Update de valores de uma recordset
* Procurando por registros
* Combinando recordsets

.. nextslide::

* Filtrando recordsets
* Atravessando as relações de registros
* Estendendo a lógica de negócios definido em um modelo
* Estendendo write() e create()
* Customizando como os registros são procurados

Introdução
----------
Quando falamos de Modelo de Aplicações, nós vimos como declarar ou externder
modelos em módulos customizados. As receitas deste capítulo abgrangem campos
calculados bem como métodos para restringir os valores dos campos.

Vamos focar nos conceitos básicos de desenvolvimento do lado servidor seguindo as
definições Odoo de metodos, manipulação de registros e estender metódos herdados.


Model methods & API Decorators
------------------------------
As classes de modelo podem conter:

- Campos para os dados personalizados, através da definição de fields;
- Comportamento personalizado através da definição de métodos da classe;

Vamos ver como escrever um método que pode ser chamado por um botão na interface
do usuário, ou por algum outro pedaço de código em nossa aplicação.

Este método irá atuar sobre LibraryBooks e executar as ações necessárias para
alterar o estado de uma seleção de livros.

.. nextslide::

Adicione o campo state no modelo LibraryBook como exibido abaixo:

.. literalinclude:: code/1.py
   :language: python
   :linenos:

.. nextslide::

Para definir um metódo na LibraryBook para permitir a mudança do estado de
uma seleção de livros, precisaremos adicionar o seguinte código na definição
do modelo:

1. Adicione um método auxiliar para verificar se a mudança de estado é permitido:

.. literalinclude:: code/2.py
   :language: python
   :linenos:

.. nextslide::

2. Adicione um método para alterar o estado de alguns livros para um
novo passado como um argumento:

.. literalinclude:: code/3.py
   :language: python
   :linenos:

.. nextslide::

Definimos dois metodos:

- Eles são metodos Python comuns, tendo self como argumento, mas também podem ter argumentos adicionais.
- Os metodos são decorados com **decorators** definidos em openerp.api
- Eles realizam a conversão entre a antiga API(v5-v9) e a nova api (v8+). Portando v10 teremos somente a nova api.

Enviroment
----------

- self.env.cr : Database cursor
- self.env.user : Usuário que fez a chamada
- self.env.context : É o contexto, um dicionário python, contendo diversas informações como:
    - Linguagem do usuário;
    - Timezone
    - E outras chaves especificas definidas em tempo de execução através da interface de usuaŕio


Saída de erros para os usuários
-------------------------------

Como apresentar uma mensagem amigável ao usuário quando quando ocorrer um erro

* *Simulando o erro*: causado por uma problema de permissão, disco cheio, etc. IOError ou OSError.

.. literalinclude:: code/4.py
   :language: python
   :linenos:

.. nextslide::

1. Adicione o seguinte import no início do arquivo pyton

.. literalinclude:: code/5.py
   :language: python
   :linenos:

.. nextslide::

2. Modifique o metódo para capturar a excessão e gerar uma saída legível:

.. literalinclude:: code/6.py
   :language: python
   :linenos:

Obtendo um recordset para um modelo diferente
---------------------------------------------

Quando escrevemos código para o Odoo, os metódos do modelo atual são chamados via self.
Não é possível instânciar diretamente uma classe de um modelo diferente.

Para isso, vamos escrever um pequeno método no modelo library.book buscando todas os
library.members.

.. nextslide::
1. Na classe LibraryBooks, escreva um metódo chamado  get_all_library_members:

.. literalinclude:: code/7.py
   :language: python
   :linenos:

2. No corpo do método, use o seguinte código:

.. literalinclude:: code/8.py
   :language: python
   :linenos:


Criando novas records
---------------------

Criando registros para popular a tabela de parceiros.
Vamos criar o representante de uma empresa com alguns contatos.

.. literalinclude:: code/9.py
   :language: python
   :linenos:

.. nextslide::

Executando...

1. Dentro do método que irá criar o novo parceiro, recupere a data formatada com string
como esperado pelo método create():

.. literalinclude:: code/10.py
   :language: python
   :linenos:

2. Prepare o dict que conterá os dados do primeiro contato.

.. literalinclude:: code/11.py
   :language: python
   :linenos:

.. nextslide::

3. Prepare o dict que conterá os dados do segundo contato.

.. literalinclude:: code/12.py
   :language: python
   :linenos:

4. Prepare o dict com os valores dos campos da empresa.

.. literalinclude:: code/13.py
   :language: python
   :linenos:

.. nextslide::

5.Chame o método create para criar o novo registro.

.. literalinclude:: code/14.py
   :language: python
   :linenos:

Quando o método create() é chamado no passo 5, 3 registros são criados:

* Um para o parceiro principal - a empresa - , quando retornado por *create*
* Um para cada um dos 2 contatos, quando disponível em record.child_ids



Update de valores de uma recordset
----------------------------------

A lógica de negócios, muitas vezes significa actualização de registos, 
alterando os valores de alguns dos seus campos.

Veremos como adicionar um contato de um parceiro e modificar o campo 
data do parceiro.

Para atualizar um parceiro, escreva um novo método chamado add_contact() como este:

Opção 1:

.. literalinclude:: code/15.py
   :language: python
   :linenos:

.. nextslide::

Opção 2:

.. literalinclude:: code/16.py
   :language: python
   :linenos:


Procurando por registros
------------------------
Procurar por registros é uma opção comum nas operações do negócio.
Vamos ver como procurar um parceiro (empresa) e seus contatos pelo *nome da empresa*

1. Obtenha um conjunto de registros vázios do res.partner

.. literalinclude:: code/17.py
   :language: python
   :linenos:

.. nextslide::

2. Escrevam seu critério para o domínio de busca:

.. literalinclude:: code/18.py
   :language: python
   :linenos:

3. Chame o método search() com o domínio e retorne o recordset:

.. literalinclude:: code/19.py
   :language: python
   :linenos:


Combinando recordsets
---------------------

Às vezes, você vai achar obteve registros que não são exatamente o que você precisa.

Supported Operations RecordSet also support set operations you can add, union and intersect, ... recordset:

.. literalinclude:: code/20.py
   :language: python
   :linenos:


Filtrando recordsets
--------------------

1. Defina o método de aceitar o conjunto de registros original:

2. Defina uma função interna:

3. Chame o método filter()

.. literalinclude:: code/21.py
   :language: python
   :linenos:



Atravessando as relações de registros
-------------------------------------

1.	 Crie um método chamado get_email_addresses().
2.	 Chame o método mapped() para retornar todos os e-mails de contatos dos parceiros.
3.	 Crie um método chamado get_companies()
4.	 Chame o método mapped() para retornar as empresas dos parceiros

.. literalinclude:: code/22.py
   :language: python
   :linenos:

Estendendo a lógica definido em um modelo
-----------------------------------------------------
Quando a definimos um modelo que estende outro modelo, muitas vezes é necessário personalizar 
o comportamento de alguns métodos definidos no modelo original.
Esta é uma tarefa muito fácil no Odoo, e um dos recursos mais poderosos do quadro framework.

.. nextslide::

Crie um novo módulo adicional chamado library_loan_return_date que depende do meu_modulo.
Neste módulo, extenda o modelo library.book.loan como a seguir:

.. literalinclude:: code/23.py
   :language: python
.. literalinclude:: code/28.py
   :language: csv
   :linenos:
   :linenos:

Extenda o modelo library.member como a seguir:

.. literalinclude:: code/24.py
   :language: python
   :linenos:

.. nextslide::

Para extender a lógica do modelo library.loan.wizard, você precisa dos seguintes passos:

1. No módulo meu_modulo, modifique o método record_loans() na classe LibraryLoanWizard.

.. literalinclude:: code/25.py
   :language: python
   :linenos:

.. nextslide:: 

2. Em library_loan_return_date, crie uma classe que extenda library.loan.wizard e defina
o método _prepare_loan como a seguir:

.. literalinclude:: code/26.py
   :language: python
   :linenos:



Estendendo write() e create()
-----------------------------

Iremos estender os métodos write() e create() para controlar o acesso de alguns campos de registros.

Modifique o arquivo security/ir.model.access.csv para dar permitir o acesso dos usuários aos livros.

.. literalinclude:: code/27.csv
   :language: csv
   :linenos:

.. nextslide::

Adicione o campo manager_remarks no modelo library.book. Nos precisamos somente queo os grupo
Library Managers tenham privilégios para escrever nos campos.

.. literalinclude:: code/28.py
   :language: csv
   :linenos:

.. nextslide::

Para previnir que usuários que não fazem parte do grupo "Library Managers" modifiquem o valor 
de *manager_remarks*, vamos modificar o seguinte:

1. Extender o método create()
2. Extender o método write()
3. externder o método fields_get()

.. nextslide::

.. literalinclude:: code/29.py
   :language: csv
   :linenos:

*continua*

.. nextslide::

.. literalinclude:: code/30.py
   :language: csv
   :linenos:


Customizando como os registros são procurados
---------------------------------------------
