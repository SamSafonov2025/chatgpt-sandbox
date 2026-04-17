"""Simple Betaflight project generator for amateur FPV drones.

Usage:
    python betaflight_project.py --profile beginner_6s --output cli.txt
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DroneProfile:
    name: str
    frame_size: str
    battery: str
    motor_kv: int
    esc_protocol: str
    rx_protocol: str
    has_gps: bool


PROFILES: dict[str, DroneProfile] = {
    "beginner_6s": DroneProfile(
        name="Beginner 5-inch 6S",
        frame_size="5inch",
        battery="6S 1100mAh",
        motor_kv=1800,
        esc_protocol="DSHOT600",
        rx_protocol="CRSF",
        has_gps=False,
    ),
    "freestyle_6s_gps": DroneProfile(
        name="Freestyle 5-inch 6S + GPS",
        frame_size="5inch",
        battery="6S 1300mAh",
        motor_kv=1750,
        esc_protocol="DSHOT600",
        rx_protocol="CRSF",
        has_gps=True,
    ),
}


def generate_betaflight_cli(profile: DroneProfile) -> str:
    """Generate a safe baseline Betaflight CLI preset for a profile."""
    lines = [
        f"# Profile: {profile.name}",
        f"# Frame: {profile.frame_size}",
        f"# Battery: {profile.battery}",
        "",
        "defaults nosave",
        "feature -AIRMODE",
        "set motor_pwm_protocol = DSHOT600" if profile.esc_protocol == "DSHOT600" else "set motor_pwm_protocol = DSHOT300",
        "set dshot_bidir = ON",
        "set serialrx_provider = CRSF" if profile.rx_protocol == "CRSF" else "set serialrx_provider = SBUS",
        "set failsafe_procedure = DROP",
        "set osd_warn_batt_not_full = ON",
        "set osd_vbat_pos = 2459",
        "set osd_rssi_pos = 2082",
        "set osd_tim_1_pos = 2433",
    ]

    if profile.has_gps:
        lines.extend(
            [
                "feature GPS",
                "set gps_provider = UBLOX",
                "set gps_rescue_allow_arming_without_fix = OFF",
                "set failsafe_procedure = GPS-RESCUE",
            ]
        )

    lines.extend(
        [
            "profile 0",
            "set p_pitch = 48",
            "set i_pitch = 68",
            "set d_pitch = 38",
            "set p_roll = 45",
            "set i_roll = 65",
            "set d_roll = 35",
            "rateprofile 0",
            "set roll_rc_rate = 1.1",
            "set pitch_rc_rate = 1.1",
            "set yaw_rc_rate = 1.0",
            "save",
        ]
    )

    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Betaflight CLI preset.")
    parser.add_argument("--profile", choices=sorted(PROFILES), required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    cli = generate_betaflight_cli(PROFILES[args.profile])
    args.output.write_text(cli, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
