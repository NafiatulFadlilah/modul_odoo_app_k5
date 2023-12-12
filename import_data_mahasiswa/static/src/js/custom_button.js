/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
export class AkademikListController extends ListController {
    setup() {
        super.setup();
    }
    OnTestClick() {
        this.actionService.doAction({
            type: 'ir.actions.act_window',
            res_model: 'wizard.dataakademik.csv',
            name: 'Baca Data Akademik Mahasiswa dari CSV',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new',
            res_id: false,
        });
    }
}
registry.category("views").add("custom_button", {
    ...listView,
    Controller: AkademikListController,
    buttonTemplate: "button_akademik.ListView.Buttons",
});