from uuid import UUID

from peterpy.database.models.product import Product as ProductModel
from peterpy.entities import Product as ProductEntity


def product_model_to_entity(product_model: ProductModel) -> ProductEntity:
    return ProductEntity(
        product_id=UUID(str(product_model.product_id)),
        name=str(product_model.name),
        price=int(product_model.price),
    )


def product_entity_to_model(product_entity: ProductEntity) -> ProductModel:
    return ProductModel(
        product_id=str(product_entity.product_id),
        name=product_entity.name,
        price=int(product_entity.price),
    )
