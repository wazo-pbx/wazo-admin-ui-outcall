# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask_menu.classy import classy_menu_item
from marshmallow import fields

from wazo_admin_ui.helpers.classful import BaseView
from wazo_admin_ui.helpers.mallow import BaseSchema, BaseAggregatorSchema, extract_form_fields

from .form import OutcallForm


class OutcallSchema(BaseSchema):

    class Meta:
        fields = extract_form_fields(OutcallForm)


class AggregatorSchema(BaseAggregatorSchema):
    _main_resource = 'outcall'

    outcall = fields.Nested(OutcallSchema)


class OutcallView(BaseView):

    form = OutcallForm
    resource = 'outcall'
    schema = AggregatorSchema

    @classy_menu_item('.outcalls', 'Outcalls', order=4, icon="long-arrow-left")
    def index(self):
        return super(OutcallView, self).index()
