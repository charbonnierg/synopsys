from synopsys.adapters.pubsub.redis import RedisMsg


class TestRedisMsg:
    def test_msg_creation(self):
        reply = {
            "type": b"pmessage",
            "pattern": b"$REPLY.be2bc5c6e138f19f.*",
            "channel": b"$REPLY.be2bc5c6e138f19f.39ad9320b9225583ee19cc50",
            "data": b"13",
        }
        msg = RedisMsg(reply)
        assert msg.get_headers() == {}
        assert msg.get_payload() == b"13"
        assert msg.get_subject() == "$REPLY.be2bc5c6e138f19f.39ad9320b9225583ee19cc50"
