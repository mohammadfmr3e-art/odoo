<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <!-- ==================== LIST VIEW ==================== -->
    <record id="view_debt_collection_record_list" model="ir.ui.view">
        <field name="name">debt.collection.record.list</field>
        <field name="model">debt.collection.record</field>
        <field name="arch" type="xml">
            <list string="Debt Collection"
                  decoration-danger="is_overdue==True"
                  decoration-success="state=='collected'"
                  decoration-muted="state=='uncollectible'">
                <field name="patient_number"/>
                <field name="patient_name"/>
                <field name="encounter_number"/>
                <field name="exit_date"/>
                <field name="debt_amount" sum="Total Debt"/>
                <field name="paid_amount" sum="Total Paid"/>
                <field name="remaining_amount" sum="Total Remaining"/>
                <field name="next_contact_date"/>
                <field name="responsible_user_id"/>
                <field name="state" widget="badge"
                       decoration-success="state=='collected'"
                       decoration-danger="state=='uncollectible'"
                       decoration-info="state=='in_progress'"/>
                <field name="is_overdue" column_invisible="1"/>
                <field name="currency_id" column_invisible="1"/>
            </list>
        </field>
    </record>

    <!-- ==================== FORM VIEW ==================== -->
    <record id="view_debt_collection_record_form" model="ir.ui.view">
        <field name="name">debt.collection.record.form</field>
        <field name="model">debt.collection.record</field>
        <field name="arch" type="xml">
            <form string="Debt Collection Record">
                <header>
                    <field name="state" widget="statusbar" statusbar_visible="new,in_progress,collected"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="patient_name" placeholder="Patient Name"/></h1>
                    </div>
                    <group>
                        <group string="Patient Info">
                            <field name="patient_number"/>
                            <field name="encounter_number"/>
                            <field name="exit_date"/>
                        </group>
                        <group string="Financial Summary">
                            <field name="currency_id" groups="base.group_multi_currency"/>
                            <field name="debt_amount"/>
                            <field name="paid_amount"/>
                            <field name="remaining_amount"/>
                        </group>
                    </group>
                    <group>
                        <group string="Follow-up">
                            <field name="last_contact_date"/>
                            <field name="next_contact_date"/>
                            <field name="responsible_user_id"/>
                            <field name="is_overdue" invisible="1"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Payments">
                            <field name="payment_line_ids">
                                <list editable="bottom">
                                    <field name="payment_date"/>
                                    <field name="amount"/>
                                    <field name="note"/>
                                </list>
                            </field>
                        </page>
                        <page string="Notes">
                            <field name="notes" placeholder="Follow-up notes, reasons for delay, agreements with patient..."/>
                        </page>
                    </notebook>
                </sheet>
                <div class="oe_chatter">
                    <field name="message_follower_ids"/>
                    <field name="activity_ids"/>
                    <field name="message_ids"/>
                </div>
            </form>
        </field>
    </record>

    <!-- ==================== SEARCH VIEW ==================== -->
    <record id="view_debt_collection_record_search" model="ir.ui.view">
        <field name="name">debt.collection.record.search</field>
        <field name="model">debt.collection.record</field>
        <field name="arch" type="xml">
            <search string="Search Debt Records">
                <field name="patient_name"/>
                <field name="patient_number"/>
                <field name="encounter_number"/>
                <field name="responsible_user_id"/>
                <filter string="Needs Follow-up Today" name="followup_today"
                        domain="[('next_contact_date', '&lt;=', context_today().strftime('%Y-%m-%d'))]"/>
                <filter string="Overdue Follow-up" name="overdue" domain="[('is_overdue', '=', True)]"/>
                <separator/>
                <filter string="New" name="state_new" domain="[('state','=','new')]"/>
                <filter string="In Progress" name="state_in_progress" domain="[('state','=','in_progress')]"/>
                <filter string="Fully Collected" name="state_collected" domain="[('state','=','collected')]"/>
                <filter string="Uncollectible" name="state_uncollectible" domain="[('state','=','uncollectible')]"/>
                <separator/>
                <filter string="Exit Date" name="exit_date" date="exit_date"/>
                <group expand="0" string="Group By">
                    <filter string="Status" name="group_state" context="{'group_by': 'state'}"/>
                    <filter string="Responsible" name="group_responsible" context="{'group_by': 'responsible_user_id'}"/>
                    <filter string="Exit Month" name="group_exit_month" context="{'group_by': 'exit_date:month'}"/>
                </group>
            </search>
        </field>
    </record>

    <!-- ==================== PIVOT VIEW (Outstanding / Debt overview) ==================== -->
    <record id="view_debt_collection_record_pivot" model="ir.ui.view">
        <field name="name">debt.collection.record.pivot</field>
        <field name="model">debt.collection.record</field>
        <field name="arch" type="xml">
            <pivot string="Debt Overview">
                <field name="exit_date" type="row" interval="month"/>
                <field name="state" type="col"/>
                <field name="debt_amount" type="measure"/>
                <field name="paid_amount" type="measure"/>
                <field name="remaining_amount" type="measure"/>
            </pivot>
        </field>
    </record>

    <!-- ==================== GRAPH VIEW ==================== -->
    <record id="view_debt_collection_record_graph" model="ir.ui.view">
        <field name="name">debt.collection.record.graph</field>
        <field name="model">debt.collection.record</field>
        <field name="arch" type="xml">
            <graph string="Debt Overview" type="bar">
                <field name="exit_date" type="row" interval="month"/>
                <field name="remaining_amount" type="measure"/>
            </graph>
        </field>
    </record>

    <!-- ==================== ACTION: Debt Records ==================== -->
    <record id="action_debt_collection_record" model="ir.actions.act_window">
        <field name="name">Debt Collection Records</field>
        <field name="res_model">debt.collection.record</field>
        <field name="view_mode">list,form,pivot,graph</field>
        <field name="search_view_id" ref="view_debt_collection_record_search"/>
        <field name="context">{'search_default_state_in_progress': 1}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Create a new debt collection record
            </p>
        </field>
    </record>

    <!-- ==================== PAYMENTS: List + Pivot for monthly collection report ==================== -->
    <record id="view_debt_collection_payment_list" model="ir.ui.view">
        <field name="name">debt.collection.payment.list</field>
        <field name="model">debt.collection.payment</field>
        <field name="arch" type="xml">
            <list string="Payments" create="true">
                <field name="payment_date"/>
                <field name="patient_name"/>
                <field name="amount" sum="Total Collected"/>
                <field name="responsible_user_id"/>
                <field name="note"/>
            </list>
        </field>
    </record>

    <record id="view_debt_collection_payment_pivot" model="ir.ui.view">
        <field name="name">debt.collection.payment.pivot</field>
        <field name="model">debt.collection.payment</field>
        <field name="arch" type="xml">
            <pivot string="Monthly Collection Report">
                <field name="payment_month" type="row"/>
                <field name="responsible_user_id" type="col"/>
                <field name="amount" type="measure"/>
            </pivot>
        </field>
    </record>

    <record id="view_debt_collection_payment_graph" model="ir.ui.view">
        <field name="name">debt.collection.payment.graph</field>
        <field name="model">debt.collection.payment</field>
        <field name="arch" type="xml">
            <graph string="Monthly Collection" type="bar">
                <field name="payment_month" type="row"/>
                <field name="amount" type="measure"/>
            </graph>
        </field>
    </record>

    <record id="action_debt_collection_payment" model="ir.actions.act_window">
        <field name="name">Collection / Payments Report</field>
        <field name="res_model">debt.collection.payment</field>
        <field name="view_mode">pivot,graph,list</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                No payments recorded yet
            </p>
        </field>
    </record>

</odoo>
