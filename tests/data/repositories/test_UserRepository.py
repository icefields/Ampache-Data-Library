# SPDX-FileCopyrightText: 2026 icefields
# SPDX-License-Identifier: GPL-3.0-only
"""UserRepository: upsert + getUser read-back against a scratch schema DB."""
from ampachedata.data.db.Database import Database
from ampachedata.data.db.mappers.UserMapper import mapUser
from ampachedata.data.db.repositories.UserRepository import UserRepository

PAYLOAD = {
    "id": "4",
    "username": "user",
    "email": "generic@gmail.com",
    "access": 100,
    "streamtoken": None,
    "fullname_public": True,
    "disabled": False,
    "create_date": 1670202701,
    "last_seen": 1751344281,
    "website": None,
    "state": None,
    "city": None,
    "art": "https://music.com.au/images/blankalbum_128x128.png",
    "has_art": False,
    "fullname": "Some Guy",
}


def _repository(dbPath):
    return UserRepository(Database(dbPath))


def testUpsertAndGetUserRoundtrip(dbPath):
    repository = _repository(dbPath)
    repository.upsertUsers([mapUser(PAYLOAD)])
    user = repository.getUser("4")
    assert user is not None
    assert user.id == "4"
    assert user.username == "user"
    assert user.fullNamePublic is True
    assert user.disabled is False
    assert user.artUrl == "https://music.com.au/images/blankalbum_128x128.png"
    assert user.fullName == "Some Guy"


def testGetUserUnknownIdIsNone(dbPath):
    repository = _repository(dbPath)
    assert repository.getUser("999") is None


def testUpsertReplacesById(dbPath):
    repository = _repository(dbPath)
    repository.upsertUsers([mapUser(PAYLOAD)])
    changed = dict(PAYLOAD, fullname="Renamed Guy", city="Rome")
    repository.upsertUsers([mapUser(changed)])
    user = repository.getUser("4")
    assert user.fullName == "Renamed Guy"
    assert user.city == "Rome"
