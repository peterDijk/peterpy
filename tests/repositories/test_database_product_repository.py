import pytest


from peterpy.database.connection import DatabaseConnection, DatabaseSession
from peterpy.database.models import Product as ProductModel, Base
from peterpy.entities.product import Product
from peterpy.repositories.database_product_repository import DatabaseProductRepository
from tests.helpers import create_uuid_from_string


@pytest.fixture
def session():
    connection = DatabaseConnection("sqlite:///:memory:")
    engine = connection.engine()
    if not engine.url.get_backend_name() == "sqlite":
        raise RuntimeError("Use SQLite backend to run tests")

    Base.metadata.create_all(
        engine
    )  # metadata stores all the tables created by the base model.
    try:
        with DatabaseSession(engine) as session:
            yield session  # how does yield work here?
    finally:
        Base.metadata.drop_all(engine)


@pytest.fixture
def seed(session):
    session.add_all(
        [
            ProductModel(
                product_id=str(create_uuid_from_string("p1")),
                name="product_1",
                price=10.0,
            ),
            ProductModel(
                product_id=str(create_uuid_from_string("p2")),
                name="product_2",
                price=10.0,
            ),
        ]
    )
    session.commit()


@pytest.fixture
def repository(session, seed):
    return DatabaseProductRepository(session)


def test_repository_get_product(repository):
    product = repository.get(str(create_uuid_from_string("p1")))
    assert product.name == "product_1"
    assert product.price == 10.0


def test_repository_get_product_not_found(repository):
    with pytest.raises(KeyError):
        repository.get(str(create_uuid_from_string("p3")))


def test_repository_add_product(repository):
    product = Product(name="product_3", price=30.0)
    repository.add(product)
    added_product = repository.get(product.product_id)
    assert added_product.name == "product_3"


def test_repository_find_product(repository):
    products = repository.find({"price": 10.0})
    assert len(products) == 2
    assert products[0].name == "product_1"
    assert products[1].name == "product_2"


def test_repository_find_product_not_found(repository):
    products = repository.find({"price": 20.0})
    assert len(products) == 0


def test_repository_all_products(repository):
    products = repository.all()
    assert len(list(products)) == 2
