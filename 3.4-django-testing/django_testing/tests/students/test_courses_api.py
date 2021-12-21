import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make(Course, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return baker.make(Student,**kwargs)
    return factory


@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    course_factory(_quantity=10)
    course_first = Course.objects.first()
    url = reverse('courses-detail', args=(course_first.id, ))
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['id'] == course_first.id
    assert response.data['name'] == course_first.name

@pytest.mark.django_db
def test_list_course(client, course_factory):
    course = course_factory(_quantity=10)
    url = reverse('courses-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == len(course)


@pytest.mark.django_db
def test_id_filter_course(client, course_factory):
    course_factory(_quantity=10)
    course_last = Course.objects.last()
    url = reverse("courses-list") + f'?id={course_last.id}'
    response = client.get(url)
    assert response.status_code == 200
    assert response.data[-1].get('id') == course_last.id


@pytest.mark.django_db
def test_name_filter_course(client, course_factory):
    course_factory(_quantity=10)
    course_last = Course.objects.last()
    url = reverse("courses-list") + f'?id={course_last.id}'
    response = client.get(url)
    assert response.status_code == 200
    assert response.data[-1].get('name') == course_last.name


@pytest.mark.django_db
def test_create_course(client):

    Course.objects.create(name='Biology')

    url = reverse("courses-list")
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == 'Biology'


@pytest.mark.django_db
def test_update_course(client, course_factory):
    course_factory(_quantity=10)
    course_update = Course.objects.first()
    url = reverse("courses-detail", args=(course_update.id, ))
    data_update = {'name': 'Geography'}
    response = client.patch(url, data_update)
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course_factory(_quantity=10)
    course_up = Course.objects.first()
    url = reverse("courses-detail", args=(course_up.id, ))
    data_update = {'name': 'Physics'}
    response = client.delete(url, data_update)
    assert response.status_code == 204