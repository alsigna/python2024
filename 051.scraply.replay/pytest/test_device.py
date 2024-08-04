import pytest
from devices import CiscoDevice


@pytest.mark.parametrize(
    "host, expected_version",
    [
        ("192.168.122.101", "17.03.03"),
        ("192.168.122.113", "15.9(3)M3"),
        ("192.168.122.201", "15.2(CML_NIGHTLY_20190423)FLO_DSGS7"),
    ],
)
@pytest.mark.scrapli_replay
def test_cisco_get_version(host, expected_version):
    device = CiscoDevice(host)
    assert device.get_version() == expected_version
