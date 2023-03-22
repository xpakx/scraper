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
