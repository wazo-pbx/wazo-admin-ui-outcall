# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_admin_ui.helpers.plugin import create_blueprint
from wazo_admin_ui.helpers.destination import register_listing_url

from .service import OutcallService
from .view import OutcallView, OutcallDestinationView

outcall = create_blueprint('outcall', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']

        OutcallView.service = OutcallService()
        OutcallView.register(outcall, route_base='/outcalls')
        register_flaskview(outcall, OutcallView)

        OutcallDestinationView.service = OutcallService()
        OutcallDestinationView.register(outcall, route_base='/outcall_destination')

        register_listing_url('outcall', 'outcall.OutcallDestinationView:list_json')

        core.register_blueprint(outcall)
