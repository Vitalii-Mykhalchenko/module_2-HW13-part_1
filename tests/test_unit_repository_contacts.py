import unittest
from unittest.mock import MagicMock
from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

from hw11.database.models import Contact, User
from hw11.schemas import ContactModel, ContactResponse, UserModel, UserDb, UserResponse, TokenModel, RequestEmail
from hw11.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    update_contact,
    remove_contact,
    upcoming_birthdays,
)




class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.birthday = datetime.strptime("01.11.2011", "%d.%m.%Y")


    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)
    
    async def test_get_contact_firstname_found(self):
        contact = Contact(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            birthday=self.birthday,
            user=self.user
            )
        self.session.query().filter().first.return_value = contact
        result = await get_contact(first_name=contact.first_name,user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        contact = Contact(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            birthday=self.birthday,
            user=self.user
        )
        self.session.query().filter().first.return_value = None
        result = await get_contact(first_name=contact.first_name,user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            birthday=self.birthday,
            user=self.user
        )
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=contact.first_name, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=contact.first_name, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = ContactModel(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            birthday=self.birthday,
            user=self.user
        )
        self.session.query().filter().first.return_value = body
        self.session.commit.return_value = None
        result = await update_contact(contact_id=body.first_name, body=body, user=self.user, db=self.session)
        self.assertEqual(result, body)

    async def test_update_contact_not_found(self):
        body = ContactModel(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            birthday=self.birthday,
            user=self.user
        )
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=body.first_name, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_upcoming_birthdays(self):
        today = date.today()
        upcoming_birthdays_list = [
            Contact(birthday=today + timedelta(days=q)) for q in range(5)]
        self.session.query().filter().all.return_value = upcoming_birthdays_list
        result = await upcoming_birthdays( user=self.user, db=self.session)
        self.assertEqual(len(result), 5)
        for contact in result:
            self.assertTrue(contact.birthday >= today)
            self.assertTrue(contact.birthday <= today + timedelta(days=7))


if __name__ == '__main__':
    unittest.main()
