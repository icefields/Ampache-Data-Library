# SPDX-FileCopyrightText: 2026 icefields
# SPDX-License-Identifier: GPL-3.0-only
"""getUser write-through: fetch -> map -> upsert -> read back from the DB.
username is forwarded only when passed (omitted = current api user, spec).
The response's `auth` field is a live session token — dropped by the
mapper, never persisted."""
import sqlite3

import pytest

from ampachedata import AmpacheClient, User


def testGetUserWriteThroughReadBack(makeClient, seedCredentials, seedSession, userPayload):
    client, transport = makeClient([userPayload])
    seedCredentials()
    seedSession()
    user = client.getUser()
    assert isinstance(user, User)
    assert user.id == "4"
    assert user.username == "user"
    assert user.email == "generic@gmail.com"
    assert user.access == 100
    assert user.fullNamePublic is False
    assert user.disabled is False
    assert user.fullName == "Some Guy"
    assert user.createDate == 1670202701
    assert user.lastSeen == 1751344281
    assert user.artUrl == "https://music.com.au/images/blankalbum_128x128.png"
    # The returned entity IS the DB read-back: a second call with no
    # queued payload must fail on transport, proving the first call
    # persisted (write-through, not pass-through).
    with pytest.raises(AssertionError):
        client.getUser()


def testGetUserOmitsUsernameWhenNotPassed(makeClient, seedCredentials, seedSession, userPayload):
    client, transport = makeClient([userPayload])
    seedCredentials()
    seedSession()
    client.getUser()
    params = transport.requests[0]["params"]
    assert params["action"] == "user"
    assert "username" not in params


def testGetUserForwardsUsername(makeClient, seedCredentials, seedSession, userPayload):
    client, transport = makeClient([userPayload])
    seedCredentials()
    seedSession()
    client.getUser("someone")
    assert transport.requests[0]["params"]["username"] == "someone"


def testGetUserNeverPersistsLiveSessionToken(makeClient, seedCredentials, seedSession, userPayload, dbPath):
    client, _ = makeClient([userPayload])
    seedCredentials()
    seedSession()
    client.getUser()
    connection = sqlite3.connect(dbPath)
    try:
        rows = connection.execute("SELECT * FROM UserEntity").fetchall()
        for row in rows:
            for value in row:
                assert value != userPayload["auth"]
    finally:
        connection.close()
