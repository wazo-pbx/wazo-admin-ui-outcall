# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wtforms.fields import (SubmitField,
                            BooleanField,
                            StringField,
                            SelectMultipleField,
                            FieldList,
                            FormField)
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Length, NumberRange

from wazo_admin_ui.helpers.form import BaseForm


class OutcallExtensionForm(BaseForm):
    context = StringField('Context')
    exten = StringField('Extension', [Length(max=40)])
    caller_id = StringField('Caller ID', [Length(max=80)])
    external_prefix = StringField('External prefix', [Length(max=64)])
    strip_digits = IntegerField('Strip digits', [NumberRange(min=0)])


class OutcallForm(BaseForm):
    name = StringField('Name', [InputRequired(), Length(max=128)])
    description = StringField('Description')
    extensions = FieldList(FormField(OutcallExtensionForm))
    trunk = SelectMultipleField('Trunks', choices=[])
    preprocess_subroutine = StringField('Preprocess Subroutine')
    internal_caller_id = BooleanField('Internal Caller ID')
    submit = SubmitField('Submit')
