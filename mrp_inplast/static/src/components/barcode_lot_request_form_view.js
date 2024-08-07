/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";

class BarcodeLotFormController extends FormController {

    setup() {
        super.setup();
        this.notification = useService("notification");
    }

    async onWillSaveRecord(record) {
        this.savingRecordId = record.resId;
        return super.onWillSaveRecord(...arguments);
    }

    async onRecordSaved(record) {
        debugger;
        if (record.resId !== this.savingRecordId) {
            this.notification.add(
                _t("The maintenance request has successfully been created."),
                { type: "success" }
            );
        }
        return super.onRecordSaved(...arguments);
    }
}

export const BarcodeLotFormView = {
    ...formView,
    Controller: BarcodeLotFormController,
};

registry.category("views").add("barcode_lot_request_form", BarcodeLotFormView);
