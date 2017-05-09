# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask_menu.classy import classy_menu_item

from wazo_admin_ui.helpers.classful import BaseView

from .form import OutcallForm


class OutcallView(BaseView):

    form = OutcallForm
    resource = 'outcall'

    @classy_menu_item('.outcalls', 'Outcalls', order=4, icon="long-arrow-left")
    def index(self):
        return super(OutcallView, self).index()

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('outcall', {}))
        return form
