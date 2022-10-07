from rest_framework.reverse import reverse


def test_rates_get(client):
    response = client.get(reverse('api:rates'))
    assert response.status_code == 200
    assert response.json()['count']
    assert response.json()['results']


def test_rates_post_empty(client):
    response = client.post(reverse('api:rates'), data={})
    assert response.status_code == 400
    assert response.json() == {
        'buy': ['This field is required.'],
        'sale': ['This field is required.'],
        'base_currency_type': ['This field is required.'],
        'currency_type': ['This field is required.'],
        'source': ['This field is required.'],
    }
