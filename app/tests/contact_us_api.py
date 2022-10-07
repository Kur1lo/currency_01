from rest_framework.reverse import reverse
import pytest


def test_contact_get(client):
    response = client.get(reverse('api:contacts'))
    assert response.status_code == 200


def test_contactus_api_post_empty(client):
    response = client.post(reverse('api:contacts'), data={})
    # breakpoint()
    assert response.status_code == 400  # error
    assert response.json() == {
        'email_from': ['This field is required.'],
        'subject': ['This field is required.'],
        'email_to': ['This field is required.'],
        'massage': ['This field is required.'],
    }


def test_contactus_api_post_valid(client, mailoutbox):
    data = {
        'email_to': 'example1@mail.com',
        'email_from': 'example@mail.com',
        'subject': 'subject example',
        'massage': 'Body Example',
    }
    response = client.post(reverse('api:contacts'), data=data)

    assert response.status_code == 201  # success
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == 'ContactUs From Currency Project'


@pytest.mark.parametrize('email_from', ('examplemail.com', '12312', 'WAFASEFS'))
def test_contactus_post_invalid_email(client, email_from):
    data = {
        'email_to': 'example1@mail.com',
        'email_from': email_from,
        'subject': 'subject example',
        'massage': 'Body Example',
    }
    response = client.post(reverse('api:contacts'), data=data)
    assert response.status_code == 400
    assert response.json() == {'email_from': ['Enter a valid email address.']}
