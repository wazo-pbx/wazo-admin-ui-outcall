# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_wtf import FlaskForm

from wtforms.fields import (SubmitField,
                            StringField,
                            SelectMultipleField,
                            FieldList,
                            FormField)
from wtforms.validators import InputRequired


class OutcallExtensionForm(FlaskForm):
    context = StringField('Context')
    exten = StringField('Extension')
    caller_id = StringField('Caller ID')
    external_prefix = StringField('External prefix')
    prefix = StringField('Prefix')
    strip_digits = StringField('Strip digits')


class OutcallForm(FlaskForm):
    name = StringField('Name', [InputRequired()])
    description = StringField('Description')
    extensions = FieldList(FormField(OutcallExtensionForm))
    trunk = SelectMultipleField('Trunks', choices=[])
    submit = SubmitField('Submit')
