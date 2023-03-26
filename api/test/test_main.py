import os
os.environ['DB_URL'] = 'sqlite:///test.db'
os.environ['INITIAL_DATA_FILE'] = 'nonexistent-file'

from fastapi.testclient import TestClient
from unittest import TestCase
import app.main as main
from app.data import ActivityData

class TestApi(TestCase):
    def setUp(self) -> None:
        main.repo.Base.metadata.create_all(bind=main.repo.engine)

    def tearDown(self) -> None:
        main.repo.Base.metadata.drop_all(bind=main.repo.engine)
        main.repo.engine.dispose()

    def test_activities__should_return_empty_list(self):
        client = TestClient(main.app)
        response = client.get("/activities")
        assert response.status_code == 200
        assert response.json() == []

    def test_activities__should_return_activities(self):
        client = TestClient(main.app)
        main.repo.add_activity(
            ActivityData('1', 12, 'date 1','5 km', [])
        )
        response = client.get("/activities")
        assert response.status_code == 200
        result = response.json()
        assert len(result) == 1
        assert result[0]['completed_streets'] == 12
        assert result[0]['date'] == 'date 1'
        assert result[0]['distance'] == '5 km'

    def test_streets__should_return_empty_list(self):
        client = TestClient(main.app)
        response = client.get("/streets")
        assert response.status_code == 200
        assert response.json() == []

    def test_streets__should_return_streets(self):
        client = TestClient(main.app)
        main.repo.add_activity(
            ActivityData(
                '1', 
                12, 
                'date 1',
                '5 km', 
                [{'name':'Street 1', 'city_name':'City 1'}, {'name':'Street 2', 'city_name':'City 1'}]
            )
        )
        response = client.get("/streets")
        assert response.status_code == 200
        result = response.json()
        assert len(result) == 2
        assert result[0]['name'] == 'Street 1'
        assert result[0]['city_name'] == 'City 1'
        assert result[1]['name'] == 'Street 2'
        assert result[1]['city_name'] == 'City 1'


    def test_activities__should_return_specific_pages(self):
        client = TestClient(main.app)
        main.repo.add_activity(ActivityData('1', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('2', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('3', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('4', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('5', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('6', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('7', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('8', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('9', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('10', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('11', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('12', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('13', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('14', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('15', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('16', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('17', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('18', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('19', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('20', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('21', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('22', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('23', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('24', 12, 'date 1','5 km', []))
        main.repo.add_activity(ActivityData('25', 12, 'date 1','5 km', []))
        response = client.get("/activities")
        assert response.status_code == 200
        result = response.json()
        assert len(result) == 20
        response = client.get("/activities?page=1")
        assert response.status_code == 200
        result = response.json()
        assert len(result) == 5
        response = client.get("/activities?page=2")
        assert response.status_code == 200
        result = response.json()
        assert len(result) == 0


    def test_streets__should_return_specific_pages(self):
        client = TestClient(main.app)
        main.repo.add_activity(ActivityData('1', 12, 'date 1','5 km', [
            {'name':'Street 1', 'city_name':'City 1'},
            {'name':'Street 2', 'city_name':'City 1'},
            {'name':'Street 3', 'city_name':'City 1'},
            {'name':'Street 4', 'city_name':'City 1'},
            {'name':'Street 5', 'city_name':'City 1'},
            {'name':'Street 6', 'city_name':'City 1'},
            {'name':'Street 7', 'city_name':'City 1'},
            {'name':'Street 8', 'city_name':'City 1'},
            {'name':'Street 9', 'city_name':'City 1'},
            {'name':'Street 10', 'city_name':'City 1'},
            {'name':'Street 11', 'city_name':'City 1'},
            {'name':'Street 12', 'city_name':'City 1'},
            {'name':'Street 13', 'city_name':'City 1'},
            {'name':'Street 14', 'city_name':'City 1'},
            {'name':'Street 15', 'city_name':'City 1'},
            {'name':'Street 16', 'city_name':'City 1'},
            {'name':'Street 17', 'city_name':'City 1'},
            {'name':'Street 18', 'city_name':'City 1'},
            {'name':'Street 19', 'city_name':'City 1'},
            {'name':'Street 20', 'city_name':'City 1'},
            {'name':'Street 21', 'city_name':'City 1'},
            {'name':'Street 22', 'city_name':'City 1'},
            {'name':'Street 23', 'city_name':'City 1'},
            {'name':'Street 24', 'city_name':'City 1'},
            {'name':'Street 25', 'city_name':'City 1'},
        ]))
        response = client.get("/streets")
        assert response.status_code == 200
        result = response.json()
        assert len(result) == 20
        response = client.get("/streets?page=1")
        assert response.status_code == 200
        result = response.json()
        assert len(result) == 5
        response = client.get("/streets?page=2")
        assert response.status_code == 200
        result = response.json()
        assert len(result) == 0
