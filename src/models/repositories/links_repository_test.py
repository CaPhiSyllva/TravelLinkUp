import uuid
import pytest
from sqlite3 import Connection
from src.models.repositories.links_repository import LinksRepository
from src.models.settings.db_connection_handler import db_connection_handler

@pytest.fixture(scope="module")
def connection() -> Connection:
    db_connection_handler.connect()
    return db_connection_handler.get_connection()

@pytest.mark.skip(reason="Interação com DB")
def test_registry_link(connection):
    links_repository = LinksRepository(connection)

    link_info = {
        "id": str(uuid.uuid4()),
        "trip_id": str(uuid.uuid4()),
        "link": "http://example.com",
        "title": "ExampleTitle"
    }

    links_repository.registry_link(link_info)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM links WHERE id = ?", (link_info["id"],))
    link_record = cursor.fetchone()

    assert link_record is not None, "Link not registered"
    assert link_record[2] == link_info["link"], f"Expected link {link_info['link']} but got {link_record[2]}"
    print(f"Link {link_record[2]} successfully registered")

    # Limpar dados criados pelo teste
    cursor.execute("DELETE FROM links WHERE id = ?", (link_info["id"],))
    connection.commit()

@pytest.mark.skip(reason="Interação com DB")
def test_find_links_from_trip(connection):
    links_repository = LinksRepository(connection)

    trip_id = str(uuid.uuid4())
    link_info = {
        "id": str(uuid.uuid4()),
        "trip_id": trip_id,
        "link": "http://example.com",
        "title": "ExampleTitle"
    }

    links_repository.registry_link(link_info)

    links = links_repository.find_links_from_trip(trip_id)
    assert len(links) > 0, "No links found for the trip"
    assert links[0][2] == link_info["link"], f"Expected link {link_info['link']} but got {links[0][2]}"
    print(f"Links for trip {trip_id} found: {links}")

    # Limpar dados criados pelo teste
    cursor = connection.cursor()
    cursor.execute("DELETE FROM links WHERE id = ?", (link_info["id"],))
    connection.commit()

# Executar os testes de integração
if __name__ == "__main__":
    pytest.main()
