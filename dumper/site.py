from six import string_types

from django.db.models import signals

from .invalidation import invalidate_paths


def register(model):
    def invalidate_instance(sender, instance, **kwargs):
        invalidate_instance_paths(instance)

    signals.post_save.connect(invalidate_instance, model, weak=False)
    signals.pre_delete.connect(invalidate_instance, model, weak=False)
    for through in get_manytomany_through_from_model(model):
        signals.m2m_changed.connect(invalidate_instance, through, weak=False)


def get_manytomany_through_from_model(model):
    for field in model._meta.many_to_many:
        yield field.rel.through


def invalidate_instance_paths(instance):
    paths = get_paths_from_model(instance)
    invalidate_paths(paths)


def get_paths_from_model(instance):
    paths = instance.dependent_paths()
    if isinstance(paths, string_types):
        model_name = instance.__class__.__name__
        raise TypeError(
            ('dependent_paths on {model_name} should return a list of paths, '
             ' not a string'.format(model_name=model_name))
        )
    return paths
