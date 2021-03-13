import json

import pytest
from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata

from src import app


@pytest.fixture
def kafka_conn_last_msg():
    def _method(topic):
        consumer = KafkaConsumer(bootstrap_servers=app.config['KAFKA_URL'], group_id='testing',
                                 key_deserializer=bytes.decode,
                                 value_deserializer=lambda v: json.loads(v.decode('utf-8')), auto_offset_reset='latest',
                                 enable_auto_commit=False)

        partition = TopicPartition(topic, 0)
        consumer.assign([partition])
        last_pos = consumer.end_offsets([partition])
        pos = last_pos[partition]
        offset = OffsetAndMetadata(pos - 1, b'')
        consumer.commit(offsets={partition: offset})
        msg = next(consumer)
        consumer.close()
        return msg

    return _method
