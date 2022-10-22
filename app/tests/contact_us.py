from django.urls import reverse
import pytest


def test_contactus_get(client):
    response = client.get(reverse('currency:base_create'))
    assert response.status_code == 200


def test_contactus_post_empty(client):
    response = client.post(reverse('currency:base_create'), data={})
    assert response.status_code == 200  # error
    assert response.context_data['form'].errors == {
        'email_from': ['This field is required.'],
        'subject': ['This field is required.'],
        'email_to': ['This field is required.'],
        'massage': ['This field is required.'],
    }


def test_contactus_post_valid(client, mailoutbox):
    data = {
        'email_to': 'example1@mail.com',
        'email_from': 'example@mail.com',
        'subject': 'subject example',
        'massage': 'Body Example',
    }
    response = client.post(reverse('currency:base_create'), data=data)
    assert response.status_code == 302  # success
    assert response.headers['Location'] == '/currency/contact_base/'

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
    response = client.post(reverse('currency:base_create'), data=data)
    assert response.status_code == 200
    assert response.context_data['form'].errors == {'email_from': ['Enter a valid email address.']}
