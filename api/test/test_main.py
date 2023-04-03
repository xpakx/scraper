import os
os.environ['DB_URL'] = 'sqlite:///test.db'
os.environ['INITIAL_DATA_FILE'] = 'nonexistent-file'

from fastapi.testclient import TestClient
from unittest import TestCase
import app.main as main
from app.data import ActivityData
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
            {'id': '1', 'completed_streets': 12, 'date': 'date 1', 'distance': 5.00, 'streets': []}
        )
        response = client.get("/activities")
        assert response.status_code == 200
        result = response.json()
        assert len(result) == 1
        assert result[0]['completed_streets'] == 12
        assert result[0]['date'] == 'date 1'
        assert result[0]['distance'] ==  5.00

    def test_streets__should_return_empty_list(self):
        client = TestClient(main.app)
        response = client.get("/streets")
        assert response.status_code == 200
        assert response.json() == []

    def test_streets__should_return_streets(self):
        client = TestClient(main.app)
        main.repo.add_activity(
            {
              'id': '1', 
              'completed_streets': 12, 
              'date': 'date 1', 
              'distance': 5.00, 
              'streets': [{'name':'Street 1', 'city_name':'City 1'}, {'name':'Street 2', 'city_name':'City 1'}]
            }
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
        for i in range(1, 26):
            main.repo.add_activity(
                {'id': str(i), 'completed_streets': 12, 'date': 'date 1', 'distance': 5.00, 'streets': []}
            )
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
        streets = [{'name': f'Street {i}', 'city_name': 'City 1'} for i in range(1,26)]
        main.repo.add_activity(
            {'id': '1', 'completed_streets': 12, 'date': 'date 1', 'distance': 5.00, 'streets': streets}
        )
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

    def test_streets__should_return_empty_list_for_area(self):
        client = TestClient(main.app)
        response = client.get("/streets?area=Area")
        assert response.status_code == 200
        assert response.json() == []

    def test_streets__should_return_streets_for_area(self):
        client = TestClient(main.app)
        main.repo.add_street_data([{'name': 'Street 1', 'areas': ['Area']}])
        main.repo.add_activity(
            {
              'id': '1', 
              'completed_streets': 12, 
              'date': 'date 1', 
              'distance': 5.00, 
              'streets': [{'name':'Street 1', 'city_name':'City 1'}, {'name':'Street 2', 'city_name':'City 1'}]
            }
        )
        response = client.get("/streets?area=Area")
        assert response.status_code == 200
        result = response.json()
        print(result)
        assert len(result) == 1
        assert result[0]['name'] == 'Street 1'
        assert result[0]['city_name'] == 'City 1'

    def test_progress__should_return_progress_for_city(self):
        client = TestClient(main.app)
        main.repo.add_area_data([{'area': 'Wrocław', 'street_count': 3}])
        main.repo.add_activity(
            {
              'id': '1', 
              'completed_streets': 12, 
              'date': 'date 1', 
              'distance': 5.00, 
              'streets': [{'name':'Street 1', 'city_name':'Wrocław'}, {'name':'Street 2', 'city_name':'Wrocław'}]
            }
        )
        response = client.get("/streets/progress")
        assert response.status_code == 200
        result = response.json()
        assert result['total'] == 3
        assert result['completed'] == 2   
        assert result['city_completed'] == False  

    def test_progress__should_return_progress_for_completed_city(self):
        client = TestClient(main.app)
        main.repo.add_area_data([{'area': 'Wrocław', 'street_count': 2}])
        main.repo.add_activity(
            {
              'id': '1', 
              'completed_streets': 12, 
              'date': 'date 1', 
              'distance': 5.00, 
              'streets': [{'name':'Street 1', 'city_name':'Wrocław'}, {'name':'Street 2', 'city_name':'Wrocław'}]
            }
        )
        response = client.get("/streets/progress")
        assert response.status_code == 200
        result = response.json()
        assert result['total'] == 2
        assert result['completed'] == 2   
        assert result['city_completed'] == True  

    def test_progress__should_return_progress_for_area(self):
        client = TestClient(main.app)
        main.repo.add_area_data([{'area': 'Area', 'street_count': 3}])       
        main.repo.add_street_data([{'name': 'Street 1', 'areas': ['Area']}, {'name': 'Street 2', 'areas': ['Area']}])
        main.repo.add_activity(
            {
              'id': '1', 
              'completed_streets': 12, 
              'date': 'date 1', 
              'distance': 5.00, 
              'streets': [{'name':'Street 1', 'city_name':'City'}, {'name':'Street 2', 'city_name':'City'}]
            }
        )
        response = client.get("/streets/progress?area=Area")
        assert response.status_code == 200
        result = response.json()
        assert result['total'] == 3
        assert result['completed'] == 2   
        assert result['city_completed'] == False  

    def test_progress__should_return_progress_for_completed_area(self):
        client = TestClient(main.app)
        main.repo.add_area_data([{'area': 'Area', 'street_count': 2}])
        main.repo.add_street_data([{'name': 'Street 1', 'areas': ['Area']}, {'name': 'Street 2', 'areas': ['Area']}])
        main.repo.add_activity(
            {
              'id': '1', 
              'completed_streets': 12, 
              'date': 'date 1', 
              'distance': 5.00, 
              'streets': [{'name':'Street 1', 'city_name':'City'}, {'name':'Street 2', 'city_name':'City'}]
            }
        )
        response = client.get("/streets/progress?area=Area")
        assert response.status_code == 200
        result = response.json()
        assert result['total'] == 2
        assert result['completed'] == 2   
        assert result['city_completed'] == True  


    def test_map__should_return_progress(self) -> None:
        client = TestClient(main.app)
        main.repo.add_area_data([{'area': 'Area', 'street_count': 3}])   
        main.repo.add_area_data([{'area': 'Area 2', 'street_count': 2}])   
        main.repo.add_street_data([{'name': 'Street 1', 'areas': ['Area']}, {'name': 'Street 2', 'areas': ['Area']}, {'name': 'Street 3', 'areas': ['Area 2']}])
        main.repo.add_activity(
            {
              'id': '1', 
              'completed_streets': 12, 
              'date': 'date 1', 
              'distance': 5.00, 
              'streets': [{'name':'Street 1', 'city_name':'City'}, {'name':'Street 2', 'city_name':'City'}]
            }
        )
        response = client.get("/map")
        assert response.status_code == 200
        result = response.json()
        assert result[0]['name'] == 'Area'
        assert result[0]['total'] == 3
        assert result[0]['completed'] == 2   
        assert result[0]['area_completed'] == False  