import pytest
from uuid import uuid4
from peterpy.entities import Product
from peterpy.repositories.memory_product_repository import MemoryProductRepository


@pytest.fixture
def repository():
    return MemoryProductRepository()


@pytest.fixture
def product():
    return Product(product_id=uuid4(), name="Test Product", price=100.0)


def test_add_product(repository, product):
    repository.add(product)
    assert repository.get(product.product_id) == product


def test_get_nonexistent_product(repository):
    with pytest.raises(KeyError):
        repository.get(uuid4())


def test_update_product(repository, product):
    repository.add(product)
    updated_product = Product(
        product_id=product.product_id, name="Updated Product", price=100.0
    )
    repository.update(updated_product)
    assert repository.get(product.product_id).name == "Updated Product"


def test_remove_product(repository, product):
    repository.add(product)
    repository.remove(product)
    with pytest.raises(KeyError):
        repository.get(product.product_id)


def test_find_product(repository, product):
    repository.add(product)
    results = repository.find({"name": "Test Product"})
    assert len(results) == 1
    assert results[0] == product
    assert results[0].name == "Test Product"


def test_find_one_product(repository, product):
    repository.add(product)
    result = repository.find_one(product.product_id)
    assert result == product


def test_all_products(repository, product):
    repository.add(product)
    all_products = list(repository.all(1, 10))
    assert len(all_products) == 1
    assert all_products[0] == product


def test_count_products(repository, product):
    repository.add(product)
    assert repository.count() == 1


def test_clear_repository(repository, product):
    repository.add(product)
    repository.clear()
    assert repository.count() == 0
