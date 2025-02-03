/** @odoo-module **/

import { WebClient } from "@web/webclient/webclient";
import {patch} from "@web/core/utils/patch";

patch(WebClient.prototype, {
    setup() {
        const title = "Daminaa";
        super.setup();
        this.title.setParts({ zopenerp: title });
    }
});
