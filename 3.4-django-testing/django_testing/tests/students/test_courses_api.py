import pytest
from django.core.exceptions import ValidationError
from students.models import Course


@pytest.mark.django_db
def test_retrieve_course(client, course_factory):
    course = course_factory()
    response = client.get(f"/api/v1/courses/{course.id}/")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == course.id
    assert data["name"] == course.name


@pytest.mark.django_db
def test_list_courses(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get("/api/v1/courses/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 10

    for index, course in enumerate(courses):
        assert data[index]["id"] == course.id
        assert data[index]["name"] == course.name


@pytest.mark.django_db
def test_filter_courses_by_id(client, course_factory):
    courses = course_factory(_quantity=5)
    target_course = courses[3]

    response = client.get(f"/api/v1/courses/?id={target_course.id}")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1

    assert data[0]["id"] == target_course.id
    assert data[0]["name"] == target_course.name


@pytest.mark.django_db
def test_filter_courses_by_name(client, course_factory):
    courses = course_factory(_quantity=5)
    target_course = courses[2]

    response = client.get(f"/api/v1/courses/?name={target_course.name}")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1

    assert data[0]["id"] == target_course.id
    assert data[0]["name"] == target_course.name


@pytest.mark.django_db
def test_create_course(client):
    new_course = {"name": "New course", "students": []}

    response = client.post("/api/v1/courses/", data=new_course)

    assert response.status_code == 201
    assert Course.objects.count() == 1

    created_course = Course.objects.first()
    assert created_course.name == new_course["name"]  # type: ignore


@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory()
    update_course = {"name": "New name course"}

    response = client.patch(f"/api/v1/courses/{course.id}/", data=update_course)

    assert response.status_code == 200

    course.refresh_from_db()
    assert course.name == update_course["name"]


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory()

    assert Course.objects.count() == 1

    response = client.delete(f"/api/v1/courses/{course.id}/")

    assert response.status_code == 204
    assert Course.objects.count() == 0


@pytest.mark.django_db
def test_create_course_invalid_data(client):
    bad_data = {"description": "Noname"}

    response = client.post("/api/v1/courses/", data=bad_data)

    assert response.status_code == 400
    assert Course.objects.count() == 0


@pytest.mark.django_db
def test_delete_non_existent_course(client):
    response = client.delete("/api/v1/courses/111/")

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize(
    "students_count, should_raise_error",
    [
        (3, False),
        (4, True),
    ],
)
def test_course_students_limit(
    settings, course_factory, student_factory, students_count, should_raise_error
):
    settings.MAX_STUDENTS_PER_COURSE = 3
    course = course_factory()
    students = student_factory(_quantity=students_count)

    course.students.add(*students)

    if should_raise_error:
        with pytest.raises(ValidationError):
            course.save()

    else:
        course.save()

    assert course.students.count() == students_count
