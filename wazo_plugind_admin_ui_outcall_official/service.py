# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.confd import confd
from wazo_admin_ui.helpers.service import BaseConfdService


class OutcallService(BaseConfdService):

    resource_confd = 'outcalls'

    def get_trunk(self, trunk_id):
        return confd.trunks.get(trunk_id)

    def create(self, outcall):
        outcall['id'] = super(OutcallService, self).create(outcall)['id']
        self._update_trunks_relations(outcall)

    def update(self, outcall):
        super(OutcallService, self).update(outcall)
        self._update_trunks_relations(outcall)

    def _update_trunks_relations(self, outcall):
        if outcall.get('trunks'):
            confd.outcalls(outcall['id']).update_trunks(outcall['trunks'])

