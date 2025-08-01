from datetime import datetime

from aggregators.atb_soup import AtbAggregator
from aggregators.varus import VarusAggregator
from aggregators.silpo import SilpoAggregator
from aggregators.metro import MetroAggregator
from multiprocessing import Pool
from utils import writer


def get_aggregator_data(aggregator_class):
    aggregator = aggregator_class()
    products = aggregator.get_products_bulk()
    return products


def main():
    aggregator_classes = [
        AtbAggregator,
        VarusAggregator,
        SilpoAggregator,
        MetroAggregator
    ]

    filename = 'shops'
    results = []
    with Pool(processes=len(aggregator_classes)) as pool:
        aggregated_products = pool.map(get_aggregator_data, aggregator_classes)

        results += aggregated_products
    writer.write_to_csv(filename, ['category', 'name', 'price', 'ref', 'shop'], results)


if __name__ == "__main__":
    time = datetime.now()
    main()
    time = datetime.now() - time
    print(f"All finished in {time}")