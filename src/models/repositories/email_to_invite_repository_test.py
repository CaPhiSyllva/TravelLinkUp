import uuid
import pytest
from sqlite3 import Connection
from typing import Dict, Tuple, List

from src.models.repositories.email_to_invite_repository import EmailsToInviteRepository
from src.models.settings.db_connection_handler import db_connection_handler

@pytest.fixture(scope="module")
def connection() -> Connection:
    db_connection_handler.connect()
    return db_connection_handler.get_connection()

@pytest.mark.skip(reason="Int. com Banco")
def test_registry_email(connection):
    emails_repository = EmailsToInviteRepository(connection)

    email_info = {
        "id": str(uuid.uuid4()),
        "trip_id": str(uuid.uuid4()),
        "email": "test@example.com"
    }

    emails_repository.registry_email(email_info)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM emails_to_invite WHERE id = ?", (email_info["id"],))
    email_record = cursor.fetchone()

    assert email_record is not None, "Email not registered"
    assert email_record[2] == email_info["email"], f"Expected email {email_info['email']} but got {email_record[2]}"
    print(f"Email {email_record[2]} successfully registered")

    # Limpar dados criados pelo teste
    cursor.execute("DELETE FROM emails_to_invite WHERE id = ?", (email_info["id"],))
    connection.commit()

@pytest.mark.skip(reason="Int. com Banco")
def test_find_emails_from_trip(connection):
    emails_repository = EmailsToInviteRepository(connection)

    trip_id = str(uuid.uuid4())
    email_info = {
        "id": str(uuid.uuid4()),
        "trip_id": trip_id,
        "email": "test@example.com"
    }

    emails_repository.registry_email(email_info)

    emails = emails_repository.find_emails_from_trip(trip_id)
    assert len(emails) > 0, "No emails found for the trip"
    assert emails[0][2] == email_info["email"], f"Expected email {email_info['email']} but got {emails[0][2]}"
    print(f"Emails for trip {trip_id} found: {emails}")

    # Limpar dados criados pelo teste
    cursor = connection.cursor()
    cursor.execute("DELETE FROM emails_to_invite WHERE id = ?", (email_info["id"],))
    connection.commit()

# Execute os testes
if __name__ == "__main__":
    pytest.main()
