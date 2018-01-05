# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.confd import confd
from wazo_admin_ui.helpers.service import BaseConfdService


class OutcallService(BaseConfdService):

    resource_confd = 'outcalls'

    def get_first_outcall_context(self):
        result = confd.contexts.list(type='outcall', limit=1, direction='asc', order='id')
        for context in result['items']:
            return context

    def get_context(self, context):
        result = confd.contexts.list(name=context)
        for context in result['items']:
            return context

    def get_trunk(self, trunk_id):
        return confd.trunks.get(trunk_id)

    def create(self, outcall):
        outcall['id'] = super(OutcallService, self).create(outcall)['id']
        self._update_trunks_relations(outcall)
        self._update_extensions_relations(outcall)
        self._update_schedules_relations(outcall)

    def update(self, outcall):
        super(OutcallService, self).update(outcall)
        self._update_trunks_relations(outcall)
        self._update_extensions_relations(outcall)
        self._update_schedules_relations(outcall)

    def _update_trunks_relations(self, outcall):
        if outcall.get('trunks'):
            confd.outcalls(outcall['id']).update_trunks(outcall['trunks'])

    def _update_extensions_relations(self, outcall):
        extensions = outcall.get('extensions', [])
        extension_ids = set([e.get('id') for e in extensions])
        existing_extensions = confd.outcalls.get(outcall['id'])['extensions']
        existing_extension_ids = set([e['id'] for e in existing_extensions])
        extension_ids_to_remove = existing_extension_ids - extension_ids

        for extension in extensions:
            if extension.get('id'):
                self._update_or_associate_extension(outcall, extension)
            else:
                self._create_or_associate_extension(outcall, extension)

        self._delete_extension_and_associations(outcall, extension_ids_to_remove)
        confd.outcalls.update(outcall)

    def _delete_extension_and_associations(self, outcall, extension_ids_to_remove):
        for id_to_remove in extension_ids_to_remove:
            confd.outcalls(outcall).remove_extension(id_to_remove)
            confd.extensions.delete(id_to_remove)

    def _create_or_associate_extension(self, outcall, extension):
        existing_extension = self._get_first_existing_extension(extension)

        if not existing_extension:
            extension['id'] = confd.extensions.create(extension)['id']
        else:
            extension['id'] = existing_extension['id']

        self._add_or_update_extension_relation(outcall, extension)

    def _get_first_existing_extension(self, extension):
        if extension['exten'] is None:
            return None
        items = confd.extensions.list(exten=extension['exten'],
                                      context=extension['context'])['items']
        return items[0] if items else None


    def _update_or_associate_extension(self, outcall, extension):
        confd.extensions.update(extension)
        self._add_or_update_extension_relation(outcall, extension)

    def _add_or_update_extension_relation(self, outcall, extension):
        confd.outcalls(outcall).add_extension(extension,
                                              prefix=extension['prefix'],
                                              external_prefix=extension['external_prefix'],
                                              strip_digits=extension['strip_digits'],
                                              caller_id=extension['caller_id'])

    def _update_schedules_relations(self, outcall):
        schedules = outcall.get('schedules')
        if schedules:
            existing_outcall = confd.outcalls.get(outcall)
            if existing_outcall['schedules']:
                schedule_id = existing_outcall['schedules'][0]['id']
                confd.outcalls(outcall).remove_schedule(schedule_id)

            if schedules[0].get('id'):
                confd.outcalls(outcall).add_schedule(schedules[0])