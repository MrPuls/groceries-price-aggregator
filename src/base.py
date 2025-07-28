from abc import abstractmethod, ABC


class GroceriesAggregator(ABC):

    @abstractmethod
    def get_categories(self):
        pass

    @abstractmethod
    def get_products(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_products_bulk(self, *args, **kwargs):
        pass