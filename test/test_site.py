from django.test import TestCase

from dumper import site

from .models import SimpleModel, RelatedModel


class TestGetPathsFromModel(TestCase):

    def model_from_dependent_paths(self, paths):
        model = lambda: None
        model.dependent_paths = lambda: paths
        return model

    def test_list_paths(self):
        paths = ['/path']
        model = self.model_from_dependent_paths(paths)
        self.assertEqual(site.get_paths_from_model(model), paths)

    def test_string_path_raises_error(self):
        paths = 'should_be_list'
        model = self.model_from_dependent_paths(paths)
        with self.assertRaises(TypeError):
            site.get_paths_from_model(model)


class TestGetManyToManyThroughFromModel(TestCase):
    def test_none_from_simple_model(self):
        self.assertFalse(
            list(site.get_manytomany_through_from_model(SimpleModel))
        )

    def test_one_from_related_model(self):
        throughs = list(site.get_manytomany_through_from_model(RelatedModel))
        self.assertEqual(len(throughs), 1)
        self.assertIn(RelatedModel.related.through, throughs)
