import os
import sys
import pytest
import aiosqlite

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_service import DbService
from db_service_interface import DbServiceI
from controller import Controller

@pytest.fixture(autouse=True)
async def setup_database():

    db: DbServiceI = DbService("test_db.db")
    async with aiosqlite.connect("test_db.db") as conn:
        await conn.execute("""CREATE TABLE IF NOT EXISTS users(
                            id INTEGER PRIMARY KEY,
                            first_name TEXT NOT NULL,
                            last_name TEXT NOT NULL,
                            password TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE)     
                            """)
        await conn.commit()
    yield db

    import os
    os.remove("test_db.db")

@pytest.mark.asyncio
async def test_email_not_valid():
    controller = Controller(setup_database)
    errors = controller.is_valid_register_info("first_name", "last_name", "INVALID_EMAIL", "123456", "123456")
    assert("Email must contain @" in errors)

@pytest.mark.asyncio
async def test_passwords_and_password_confirm_match():
    controller = Controller(setup_database)
    errors = controller.is_valid_register_info("first_name", "last_name", "john@doe.com", "654321", "123456")
    assert("Password and Confirm Password do not match" in errors)

@pytest.mark.asyncio
async def test_passwords_at_least_5_symbols():
    controller = Controller(setup_database)
    errors = controller.is_valid_register_info("first_name", "last_name", "john@doe.com", "1234", "1234")
    assert("Password cannot be empty and it must be at least 5 symbols" in errors)

@pytest.mark.asyncio
async def test_empty_password():
    controller = Controller(setup_database)
    errors = controller.is_valid_register_info("first_name", "last_name", "john@doe.com", "", "12345")
    assert("Password cannot be empty and it must be at least 5 symbols" in errors)

@pytest.mark.asyncio
async def test_empty_confirm_password():
    controller = Controller(setup_database)
    errors = controller.is_valid_register_info("first_name", "last_name", "john@doe.com", "12345", "0")
    assert("Password and Confirm Password do not match" in errors)

@pytest.mark.asyncio
async def test_empty_first_name():
    controller = Controller(setup_database)
    errors = controller.is_valid_register_info("", "last_name", "john@doe.com", "12345", "12345")
    assert("First name cannot be empty" in errors)

@pytest.mark.asyncio
async def test_empty_last_name():
    controller = Controller(setup_database)
    errors = controller.is_valid_register_info("first_name", "", "john@doe.com", "12345", "12345")
    assert("Last name cannot be empty" in errors)


@pytest.mark.asyncio
async def test_used_email_name():
    db: DbServiceI = setup_database
    (status, output) = await db.register_user("john", "doe", "john@doe.com", "12345")
    (status_2, output_2) = await db.register_user("john", "doe", "john@doe.com", "12345")
    assert("Email already exists" in output_2)