from uuid import UUID
from peterpy.database.models.product import Product as ProductModel
from peterpy.entities import Product as ProductEntity


def product_model_to_entity(product_model: ProductModel) -> ProductEntity:
    return ProductEntity(
        id=UUID(product_model.id.__str__()),
        name=product_model.name.__str__(),
        price=product_model.price.__int__(),
    )


def product_entity_to_model(product_entity: ProductEntity) -> ProductModel:
    return ProductModel(
        id=product_entity.id.__str__(),
        name=product_entity.name,
        price=product_entity.price,
    )
