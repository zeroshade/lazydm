from lazydm.tests import *

class TestResourcesController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='resources', action='index'))
        # Test response...
