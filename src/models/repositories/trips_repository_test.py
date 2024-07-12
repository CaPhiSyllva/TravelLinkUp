import pytest
import uuid
from datetime import datetime, timedelta

from src.models.repositories.trips_repository import TripsRepository
from src.models.settings.db_connection_handler import db_connection_handler

# Estabelece a conexão com o banco de dados
db_connection_handler.connect()

# Gera um ID de viagem único para ser usado nos testes
trip_id = str(uuid.uuid4())

@pytest.mark.skip(reason="Interação com banco de dados")
def test_create_trip():
    conn = db_connection_handler.get_connection()
    trips_repository = TripsRepository(conn)

    trips_info = {
        "id": trip_id,
        "destination": "Osasco",
        "start_date": datetime.strptime("2024-01-02", "%Y-%m-%d"),
        "end_date": (datetime.strptime("2024-01-02", "%Y-%m-%d") + timedelta(days=5)).strftime("%Y-%m-%d"),
        "owner_name": "Osvaldo",
        "owner_email": "osvaldo@email.com"
    }

    trips_repository.create_trip(trips_info)

@pytest.mark.skip(reason="Interação com banco de dados")
def test_find_trip_by_id():
    conn = db_connection_handler.get_connection()
    trips_repository = TripsRepository(conn)

    trip = trips_repository.find_trip_by_id(trip_id)
    assert trip is not None, "Trip not found"
    print(trip)

@pytest.mark.skip(reason="Interação com banco de dados")
def test_update_trip_status():
    conn = db_connection_handler.get_connection()
    trips_repository = TripsRepository(conn)

    # Atualiza o status da viagem
    trips_repository.update_trip_status(trip_id)

    # Verifica se o status foi atualizado corretamente (exemplo hipotético)
    # Isso pode variar dependendo da implementação real do método
    # cursor = conn.cursor()
    # cursor.execute("SELECT status FROM trips WHERE id = ?", (trip_id,))
    # updated_status = cursor.fetchone()[0]
    #
    # assert updated_status == 1, f"Expected status 1 but got {updated_status}"
    # print(f"Trip ID: {trip_id} status updated to {updated_status}")

# Executa os testes se este arquivo for o principal
if __name__ == "__main__":
    pytest.main()
