odoo.define('mitserv_import.Reconciliation', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var LineRenderer = require('account.ReconciliationRenderer');
    var relational_fields = require('web.relational_fields');
    var basic_fields = require('web.basic_fields');
    var core = require('web.core');
    var time = require('web.time');
    var qweb = core.qweb;
    var _t = core._t;

    self.fields.partner_id.$el.find("input").attr("placeholder", self._initialState.st_line.communication_partner_name || _t("Select Partner"));
    console.log(LineRenderer)
    LineRenderer.LineRenderer.prototype.start = function () {
        var self = this;
        var def1 = this._makePartnerRecord(this._initialState.st_line.partner_id, this._initialState.st_line.partner_name).then(function (recordID) {
            self.fields = {
                partner_id: new relational_fields.FieldMany2One(self,
                    'partner_id',
                    self.model.get(recordID),
                    {mode: 'edit'}
                )
            };
            self.fields.partner_id.appendTo(self.$('.accounting_view caption'));
            self.fields.partner_id.$el.find("input").attr("placeholder", self._initialState.st_line.communication_partner_name || _t("Select Partner"));
            console.log("test here")
        });
        this.$('thead .line_info_button').attr("data-content", qweb.render('reconciliation.line.statement_line.details', {'state': this._initialState}));
        this.$el.popover({
            'selector': '.line_info_button',
            'placement': 'left',
            'container': this.$el,
            'html': true,
            'trigger': 'hover',
            'animation': false,
            'toggle': 'popover'
        });
        console.log(LineRenderer)
        console.log(this)
        var def2 = LineRenderer.apply(this, arguments);
        return $.when(def1, def2);
    }
})
/**
 * rendering of the bank statement action contains progress bar, title and
 * auto reconciliation button
 */
// var TestRenderer = Widget.extend(LineRenderer, {
//     template: 'reconciliation.line',
//     /**
//      * @override
//      */
//     init: function (parent, model, state) {
//         this._super(parent);
//         this.model = model;
//         this._initialState = state;
//     },
//
//      /**
//      * @override
//      */
//     start: function () {
//         var self = this;
//         var def1 = this._makePartnerRecord(this._initialState.st_line.partner_id, this._initialState.st_line.partner_name).then(function (recordID) {
//             self.fields = {
//                 partner_id : new relational_fields.FieldMany2One(self,
//                     'partner_id',
//                     self.model.get(recordID),
//                     {mode: 'edit'}
//                 )
//             };
//             self.fields.partner_id.appendTo(self.$('.accounting_view caption'));
//             self.fields.partner_id.$el.find("input").attr("placeholder", self._initialState.st_line.communication_partner_name || _t("Select Partner"));
//             console.log("test here")
//         });
//         this.$('thead .line_info_button').attr("data-content", qweb.render('reconciliation.line.statement_line.details', {'state': this._initialState}));
//         this.$el.popover({
//             'selector': '.line_info_button',
//             'placement': 'left',
//             'container': this.$el,
//             'html': true,
//             'trigger': 'hover',
//             'animation': false,
//             'toggle': 'popover'
//         });
//         var def2 = this._super.apply(this, arguments);
//         return $.when(def1, def2);
//     },
// });
//
//
// return {
//     TestRenderer: TestRenderer,
// };
// });
