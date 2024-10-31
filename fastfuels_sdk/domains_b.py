from client_library.models.domain import Domain as DomainModel
from client_library.api.domains.create_domain

class Domain(DomainModel):
    inventories: Inventories
    features: Features
    grids: Grids

    @classmethod
    def create_domain(cls, request_body: dict) -> 'Domain':
        create_domain_request = CreateDomainRequest(**request_body)
        return create_domain()

    @classmethod
    def from_geodataframe(cls, gdf, name, horizontal_resolution, vertical_resoltion) -> 'Domain':
        domain_request = create_domain_request_from_geodataframe(gdf, name, horizontal_resolution, vertical_resolution)
        return DomainModel.from_geodataframe(gdf)


if __name__ == "__main__":
    domain = Domain.create_domain(CreateDomainRequest)
    inventories = domain.inventories
    tree_inventory = inventories.create_tree_inventory(CreateTreeInventoryRequest)