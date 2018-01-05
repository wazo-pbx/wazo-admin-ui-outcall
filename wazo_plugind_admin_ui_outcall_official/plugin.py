# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_admin_ui.helpers.plugin import create_blueprint

from .service import OutcallService
from .view import OutcallView

outcall = create_blueprint('outcall', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']

        OutcallView.service = OutcallService()
        OutcallView.register(outcall, route_base='/outcalls')
        register_flaskview(outcall, OutcallView)

        core.register_blueprint(outcall)