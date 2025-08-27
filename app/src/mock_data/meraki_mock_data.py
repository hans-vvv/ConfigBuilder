from app.models.api_models.meraki_models import StaticRoute

reserved_ranges_1 = [
    {"start": "1.1.1.1", "end": "1.1.1.10"},
    {"start": "1.1.1.100", "end": "1.1.1.110"}
]

reserved_ranges_2 = [
    {"start": "2.2.2.1", "end": "2.2.2.10"}
]

fixed_ip_assignments_1 = {

    "04:42:1a:c9:99:9b": {
        "ip": "1.1.1.11",
        "name": "test1"
    },
    "04:42:1a:ee:99:9b": {
        "ip": "1.1.1.12",
        "name": "test2"
    }
}

fixed_ip_assignments_2 = {

    "04:42:1a:c9:99:aa": {
        "ip": "2.2.2.11",
        "name": "test3"
    },
    "04:42:1a:ee:99:9b": {
        "ip": "2.2.2.12",
        "name": "test4"
    }
}

static_1 = StaticRoute(
    network_name='BRUSSELS',
    subnet_name='sub-1',
    subnet='1.1.1.0/24',
    enabled=True,
    fixed_ip_assignments=fixed_ip_assignments_1,
    reserved_ip_ranges=reserved_ranges_1,
    comment=None,
)

static_2 = StaticRoute(
    network_name='BRUSSELS',
    subnet_name='sub-2',
    subnet='2.2.2.0/24',
    enabled=True,
    fixed_ip_assignments=fixed_ip_assignments_2,
    reserved_ip_ranges=reserved_ranges_2,
    comment=None,
)


def get_mocked_static_routes():
    return [static_1, static_2]
