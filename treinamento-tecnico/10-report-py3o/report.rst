Relatórios
==========

Um dos principais recursos do framework Odoo é a geração de relatórios. Relatórios em Odoo são arquivos gerados automáticamente contendo dados de um recordset.

Relatórios Qweb
---------------

1.	 Defina a visão do seu relatório:

.. code-block:: xml

    <template id="qweb_res_partner_birthdays">
        <t t-call="report.html_container">
            <t t-call="report.internal_layout">
                <div class="page">
                    <h2>Partner's birthdays</h2>
                    <div t-foreach="docs" t-as="o" class="row mt4 mb4">
                        <div class="col-md-6"><t t-esc="o.name" /></div>
                        <div class="col-md-6">
                            <t t-if="o.birthdate" t-esc="o.birthdate" />
                            <t t-if="not o.birthdate">-</t>
                    </div>
                    </div>
                </div>
            </t>
        </t>
    </template>

.. nextslide::

2. Use o template em um relatório:

.. code-block:: xml

    <report id="report_res_partner_birthdays"
        name="meu_modulo.qweb_res_partner_birthdays"
        model="res.partner"
        string="Birthdays"
        report_type="qweb-pdf" />


report_py3o
-----------

O módulo report_py3o permite montar relatórios em pdf de forma mais fácil e rápida através de tabelas no libreoffice writer.