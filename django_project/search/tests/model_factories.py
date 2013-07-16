import factory

from ..models import Search


class SearchF(factory.Factory):
    """
    Search model factory
    """
    FACTORY_FOR = Search
