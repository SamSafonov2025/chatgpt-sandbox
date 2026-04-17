from betaflight_project import PROFILES, generate_betaflight_cli


def test_beginner_profile_has_drop_failsafe() -> None:
    cli = generate_betaflight_cli(PROFILES["beginner_6s"])
    assert "set failsafe_procedure = DROP" in cli
    assert "feature GPS" not in cli


def test_gps_profile_enables_gps_rescue() -> None:
    cli = generate_betaflight_cli(PROFILES["freestyle_6s_gps"])
    assert "feature GPS" in cli
    assert "set failsafe_procedure = GPS-RESCUE" in cli
