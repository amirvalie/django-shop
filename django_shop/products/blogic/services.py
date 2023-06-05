from ..models import IpAddress, Product


def add_user_to_product_visits(ip_address: str, product: Product) -> None:
    if not ip_address in product.visits.values_list('ip', flat=True):
        ip_object = IpAddress.objects.get_or_create(
            ip=ip_address
        )
        product.visits.add(
            ip_object[0]
        )

