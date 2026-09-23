import copy

from django.forms import CharField, ChoiceField, Field, Form, Select
from django.test import SimpleTestCase


class BasicFieldsTests(SimpleTestCase):

    def test_field_sets_widget_is_required(self):
        self.assertTrue(Field(required=True).widget.is_required)
        self.assertFalse(Field(required=False).widget.is_required)

    def test_cooperative_multiple_inheritance(self):
        class A:
            def __init__(self):
                self.class_a_var = True
                super().__init__()

        class ComplexField(Field, A):
            def __init__(self):
                super().__init__()

        f = ComplexField()
        self.assertTrue(f.class_a_var)

    def test_field_deepcopies_widget_instance(self):
        class CustomChoiceField(ChoiceField):
            widget = Select(attrs={'class': 'my-custom-class'})

        class TestForm(Form):
            field1 = CustomChoiceField(choices=[])
            field2 = CustomChoiceField(choices=[])

        f = TestForm()
        f.fields['field1'].choices = [('1', '1')]
        f.fields['field2'].choices = [('2', '2')]
        self.assertEqual(f.fields['field1'].widget.choices, [('1', '1')])
        self.assertEqual(f.fields['field2'].widget.choices, [('2', '2')])

    def test_field_deepcopy_copies_error_messages(self):
        field = CharField(error_messages={'required': 'Required.'})
        field_copy = copy.deepcopy(field)
        self.assertIsNot(field_copy.error_messages, field.error_messages)
        field_copy.error_messages['required'] = 'Other required.'
        self.assertEqual(field.error_messages['required'], 'Required.')

    def test_form_instances_do_not_share_field_error_messages(self):
        class ProfileForm(Form):
            name = CharField()

        form1 = ProfileForm()
        form2 = ProfileForm()
        self.assertIsNot(
            form1.fields['name'].error_messages,
            form2.fields['name'].error_messages,
        )
        form1.fields['name'].error_messages['required'] = 'Name is required.'
        self.assertEqual(
            form2.fields['name'].error_messages['required'],
            'This field is required.',
        )


class DisabledFieldTests(SimpleTestCase):
    def test_disabled_field_has_changed_always_false(self):
        disabled_field = Field(disabled=True)
        self.assertFalse(disabled_field.has_changed('x', 'y'))
