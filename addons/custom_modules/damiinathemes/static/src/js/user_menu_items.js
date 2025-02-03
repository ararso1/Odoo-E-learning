/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { isMacOS } from "@web/core/browser/feature_detection";
import { escape } from "@web/core/utils/strings";
import { session } from "@web/session";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
// Remove items from the user_menuitems registry
registry
    .category("user_menuitems")
    .remove("documentation");

registry
    .category("user_menuitems")
    .remove("support");

registry
    .category("user_menuitems")
    .remove("odoo_account");
