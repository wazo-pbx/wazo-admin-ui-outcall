# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import jsonify, request
from flask_babel import lazy_gettext as l_
from flask_menu.classy import classy_menu_item

from wazo_admin_ui.helpers.classful import BaseView, LoginRequiredView
from wazo_admin_ui.helpers.classful import extract_select2_params, build_select2_response

from .form import OutcallForm


class OutcallView(BaseView):
    form = OutcallForm
    resource = 'outcall'

    @classy_menu_item('.outcalls', l_('Outcalls'), order=4, icon="long-arrow-left")
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        trunks_id = [trunk['id'] for trunk in resource['trunks']]
        for extension in resource['extensions']:
            extension['prefix_'] = extension['prefix']
            del extension['prefix']
        form = self.form(data=resource, trunks_id=trunks_id)
        return form

    def _populate_form(self, form):
        form.trunks_id.choices = self._build_set_choices_trunks(form.trunks)
        for form_extension in form.extensions:
            form_extension.context.choices = self._build_set_choices_context(form_extension)
        form.schedules[0].form.id.choices = self._build_set_choices_schedule(form.schedules[0])
        form.call_permissions[0].form.id.choices = self._build_set_choices_callpermissions(form.call_permissions[0])
        return form

    def _build_set_choices_context(self, extension):
        if not extension.context.data or extension.context.data == 'None':
            context = self.service.get_first_outcall_context()
        else:
            context = self.service.get_context(extension.context.data)

        if context:
            return [(context['name'], context['label'])]

        return [(extension.context.data, extension.context.data)]

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

    def _build_set_choices_schedule(self, schedule):
        if not schedule.form.id.data or schedule.form.id.data == 'None':
            return []
        return [(schedule.form.id.data, schedule.form.name.data)]

    def _build_set_choices_callpermissions(self, callpermissions):
        if not callpermissions.form.id.data or callpermissions.form.id.data == 'None':
            return []
        return [(callpermissions.form.id.data, callpermissions.form.name.data)]

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        if 'trunks_id' in resource:
            resource['trunks'] = [{'id': int(trunk_id)} for trunk_id in resource['trunks_id']]
        else:
            resource['trunks'] = []
        for extension in resource['extensions']:
            if extension.get('id'):
                extension['id'] = int(extension['id'])
            extension['prefix'] = extension['prefix_']
            del extension['prefix_']
        return resource

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('outcall', {}))
        form.populate_errors(resources.get('extensions', {}))
        return form


class OutcallDestinationView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        outcalls = self.service.list(**params)
        results = [{'id': outcall['id'], 'text': outcall['name']} for outcall in outcalls['items']]
        return jsonify(build_select2_response(results, outcalls['total'], params))
