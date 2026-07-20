<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <menuitem id="menu_debt_collection_root"
              name="Debt Collection"
              sequence="60"/>

    <menuitem id="menu_debt_collection_records"
              name="Debt Records"
              parent="menu_debt_collection_root"
              action="action_debt_collection_record"
              sequence="10"/>

    <menuitem id="menu_debt_collection_reports"
              name="Collection Reports"
              parent="menu_debt_collection_root"
              action="action_debt_collection_payment"
              sequence="20"/>

</odoo>
