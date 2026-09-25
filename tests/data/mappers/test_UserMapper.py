# SPDX-FileCopyrightText: 2026 icefields
# SPDX-License-Identifier: GPL-3.0-only
"""mapUser: JSON booleans -> 0/1 INTEGERs, epoch ints, or-defaults;
auth (live session token) / has_art / validation / link dropped;
serverUrl/multiUserId written as '' (DB-layer columns)."""
from ampachedata.data.db.mappers.UserMapper import mapUser

FULL = {
    "id": "4",
    "username": "user",
    "auth": "demodemo",
    "email": "generic@gmail.com",
    "access": 100,
    "streamtoken": None,
    "fullname_public": False,
    "validation": None,
    "disabled": False,
    "create_date": 1670202701,
    "last_seen": 1751344281,
    "link": "https://music.com.au/stats.php?action=show_user&user_id=4",
    "website": None,
    "state": None,
    "city": None,
    "art": "https://music.com.au/images/blankalbum_128x128.png",
    "has_art": False,
    "fullname": "Some Guy",
}


def testMapUserFullFixture():
    row = mapUser(FULL)
    assert row["id"] == "4"
    assert row["username"] == "user"
    assert row["email"] == "generic@gmail.com"
    assert row["access"] == 100
    assert row["streamToken"] == ""
    assert row["fullNamePublic"] == 0
    assert row["disabled"] == 0
    assert row["fullName"] == "Some Guy"
    assert row["createDate"] == 1670202701
    assert row["lastSeen"] == 1751344281
    assert row["website"] == ""
    assert row["state"] == ""
    assert row["city"] == ""
    assert row["art"] == "https://music.com.au/images/blankalbum_128x128.png"
    assert row["serverUrl"] == ""
    assert row["multiUserId"] == ""


def testMapUserDropsLiveSessionToken():
    row = mapUser(FULL)
    # The mapper's row feeds UserEntity only; the live token must not
    # appear in ANY column value.
    assert "demodemo" not in row.values()


def testMapUserTrueBooleansStoredAsOne():
    row = mapUser(dict(FULL, fullname_public=True, disabled=True))
    assert row["fullNamePublic"] == 1
    assert row["disabled"] == 1


def testMapUserEmptyPayloadDefaults():
    row = mapUser({})
    assert row["id"] == ""
    assert row["username"] == ""
    assert row["access"] == 0
    assert row["fullNamePublic"] == 0
    assert row["disabled"] == 0
    assert row["createDate"] == 0
    assert row["lastSeen"] == 0
    assert row["art"] == ""
