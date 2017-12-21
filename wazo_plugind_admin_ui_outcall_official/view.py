# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import classy_menu_item

from wazo_admin_ui.helpers.classful import BaseView

from .form import OutcallForm


class OutcallView(BaseView):

    form = OutcallForm
    resource = 'outcall'

    @classy_menu_item('.outcalls', 'Outcalls', order=4, icon="long-arrow-left")
    def index(self):
        return super(OutcallView, self).index()

    def _map_resources_to_form(self, resource):
        trunks_id = [trunk['id'] for trunk in resource['trunks']]
        form = self.form(data=resource, trunks_id=trunks_id)
        return form

    def _populate_form(self, form):
        form.trunks_id.choices = self._build_set_choices_trunks(form.trunks)
        return form

    def _build_set_choices_trunks(self, trunks):
        results = []
        for trunk in trunks:
            if not trunk.form.id.data or trunk.form.name.data == 'None':
                results.append((trunk.form.id.data, trunk.form.name.data))
            else:
                trunk_data = self.service.get_trunk(trunk.form.id.data)
                if trunk_data['endpoint_sip']:
                    results.append((trunk_data['id'], trunk_data['endpoint_sip']['username']))
                elif trunk_data['endpoint_custom']:
                    results.append((trunk_data['id'], trunk_data['endpoint_custom']['interface']))
        return results

    def _map_form_to_resources(self, form, form_id=None):
        resource = super(OutcallView, self)._map_form_to_resources(form, form_id)
        resource['trunks'] = [{'id': int(trunk_id)} for trunk_id in resource['trunks_id']]
        return resource

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('outcall', {}))
        return form
