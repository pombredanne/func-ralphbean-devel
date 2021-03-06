import unittest
import turbogears
from turbogears import testutil

from funcweb.widget_automation import *
from funcweb.widget_validation import *

class TestWidgetListFactory(unittest.TestCase):

    def setUp(self):
        self.widget_factory = WidgetListFactory(self.get_test_default_args(),minion="myminion",module="mymodule",method="my_method")

    def test_default_args(self):
        """
        Test to check the default args if they were assigned
        """
        compare_with = self.get_test_default_args()
        widget_list=self.widget_factory.get_widgetlist()

        #print "The widget list is like :",widget_list

        for argument_name,argument_options in compare_with.iteritems():
            assert widget_list.has_key(argument_name) == True
            #test the label
            assert pretty_label(argument_name) == getattr(widget_list[argument_name],'label')
            #print getattr(widget_list[argument_name],'label')

            #print "The argument name is :",argument_name
            #because some of them dont have it like boolean
            if argument_options.has_key('default'):
                assert argument_options['default'] == getattr(widget_list[argument_name],'default')

            if argument_options.has_key("description"):
                assert argument_options['description']==getattr(widget_list[argument_name],'help_text')

            if argument_options.has_key("options"):
                assert argument_options['options'] == getattr(widget_list[argument_name],"options")

    def test_add_specialized_list(self):
        """
        Testing the internals of the special list widget
        """
        test_list_data = self.get_test_default_args()['list_default']
        widget_list_object = self.widget_factory.get_widgetlist_object()
        #not very efficient but works
        #hash_widget_object should be a widgets.RepeatingFieldSet
        list_widget_object = [h_obj for h_obj in widget_list_object if getattr(h_obj,'name')=='list_default'][0]

        assert isinstance(list_widget_object.fields[0],widgets.TextField) == True
        assert getattr(list_widget_object.fields[0],'name') == 'listfield'
        assert getattr(list_widget_object.fields[0],'label') == 'List Field'


    def test_add_specialized_hash(self):
        """
        Testing the internals of the special hash widget
        """
        test_hash_data = self.get_test_default_args()['hash_default']
        widget_list_object = self.widget_factory.get_widgetlist_object()
        #not very efficient but works
        #hash_widget_object should be a widgets.RepeatingFieldSet
        hash_widget_object = [h_obj for h_obj in widget_list_object if getattr(h_obj,'name')=='hash_default'][0]

        #print hash_widget_object.fields
        #check the key data
        assert isinstance(hash_widget_object.fields[0],widgets.TextField) == True
        assert getattr(hash_widget_object.fields[0],'name') == 'keyfield'
        assert getattr(hash_widget_object.fields[0],'label') == 'Key Field'
        #check the value data
        assert isinstance(hash_widget_object.fields[1],widgets.TextField) == True
        assert getattr(hash_widget_object.fields[1],'name') == 'valuefield'
        assert getattr(hash_widget_object.fields[1],'label') == 'Value Field'


    def test_get_widgetlist_object(self):
        """
        Test the final widgetlist object
        """
        compare_with = self.get_test_default_args()
        widget_list_object = self.widget_factory.get_widgetlist_object()

        #print widget_list_object

        all_fields = [getattr(field,"name") for field in widget_list_object]
        #print all_fields
        for argument_name in compare_with.keys():
            #print argument_name
            assert argument_name in all_fields
            #print getattr(widget_list_object,argument_name)


    def test_remote_form(self):
        schema_factory = WidgetSchemaFactory(self.get_test_default_args())
        schema_validator=schema_factory.get_ready_schema()
        widget_list_object = self.widget_factory.get_widgetlist_object()
        remote_form = RemoteFormAutomation(widget_list_object,schema_validator)
        #print remote_form

    def test_remote_form_factory(self):
        from turbogears.view import load_engines
        load_engines()

        schema_factory = WidgetSchemaFactory(self.get_test_default_args())
        schema_validator=schema_factory.get_ready_schema()

        # WidgetsList object
        widget_list_object = self.widget_factory.get_widgetlist_object()
        #print widget_list_object
        remote_form = RemoteFormFactory(widget_list_object,schema_validator).get_remote_form()

        #it is a key,value dict
        widget_list=self.widget_factory.get_widgetlist()
        #print widget_list
        all_fields = [getattr(field,"name") for field in remote_form.fields]
        #print all_fields
        #will check if the remote form object hass all the names in it
        for argument_name in widget_list.items():
            argument_name in all_fields


        #print remote_form.render()

    def test_pretty_label(self):
        """
        Testing the label converter util method
        """
        test_strings = ('service_name','some__other','cool-arg','somenormal','someweir*1*2*3*3')
        #print  pretty_label(test_strings[0])
        assert pretty_label(test_strings[0]) == 'Service Name'
        #print  pretty_label(test_strings[1])
        assert pretty_label(test_strings[1]) == 'Some Other'
        #print  pretty_label(test_strings[2])
        assert pretty_label(test_strings[2]) == 'Cool Arg'
        #print  pretty_label(test_strings[3])
        assert pretty_label(test_strings[3]) == 'Somenormal'
        #print  pretty_label(test_strings[4])
        assert pretty_label(test_strings[4]) == 'Someweir*1*2*3*3'

    def get_test_default_args(self):
        return {
                'string_default':{
                    'type':'string',
                    'default':'default string',
                    'optional':False,
                    'description':'default description'
                    },
                'int_default':{
                    'type':'int',
                    'default':'default int',
                    'optional':False,
                    'description':'default description'
                   },
                #no sense to have default
                'boolean_default':{
                    'type':'boolean',
                    'optional':False,
                    'description':'default description'
                   },
                'float_default':{
                    'type':'float',
                    'default':'default float',
                    'optional':False,
                    'description':'default description'

                    },
                'hash_default':{
                    'type':'hash',
                    'default':'default hash',
                    'optional':False,
                    'description':'default description',
                    'validator':'^[0-9]*$'

                    },
                'list_default':{
                    'type':'list',
                    'default':'default list',
                    'optional':False,
                    'description':'default description',
                    'validator':'^[0-9]*$'

                    },
                #will be converted to dropdown
                'special_string':{
                    'type':'string',
                    'default':'myfirst',
                    'options':['myfirst','mysecond','mythird'],
                    'optional':False,
                    'description':'default dropdown list'
                    }

                }
