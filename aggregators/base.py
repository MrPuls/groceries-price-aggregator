from abc import abstractmethod, ABC


class GroceriesAggregator(ABC):

    @abstractmethod
    def get_categories(self):
        pass

    @abstractmethod
    def get_products(self, *args, **kwargs):
        pass

    def get_products_bulk(self):
        bulk_results = []
        for category in self.get_categories():
            products = self.get_products(category)
            bulk_results += products
        return bulk_results