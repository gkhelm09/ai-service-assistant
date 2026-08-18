"""Simulated AI assistant for field service troubleshooting.

This module generates sample responses without calling an external AI API.
Replace `generate_response` with a real API call when you are ready.
"""

EQUIPMENT_TYPES = (
    "X-ray",
    "CT",
    "MRI",
    "Ultrasound",
    "General Medical Equipment",
)

IMAGING_TERMS = (
    "x-ray",
    "xray",
    "x ray",
    "imaging",
    "fluoro",
    "c-arm",
    "c arm",
    "dr panel",
    "flat panel",
    "receptor",
    "acquisition",
    "exam",
    "scan",
)

DETECTOR_TERMS = (
    "detector",
    "dr panel",
    "flat panel",
    "wireless panel",
    "receptor",
    "image receptor",
)

CONNECTIVITY_TERMS = (
    "connectivity",
    "connection",
    "disconnect",
    "disconnected",
    "disconnects",
    "loses connection",
    "lose connection",
    "lost connection",
    "connection lost",
    "drops out",
    "drop out",
    "dropout",
    "communication",
    "communication error",
    "comm error",
    "link down",
    "timeout",
    "handshake",
    "not detected",
    "not communicating",
    "intermittent",
    "intermittently",
    "goes offline",
    "offline",
    "unavailable",
    "cuts out",
    "cut out",
)

SYMPTOM_TERMS = (
    "fails",
    "failed",
    "failure",
    "fault",
    "error",
    "freeze",
    "freezes",
    "stops working",
    "not working",
    "unstable",
)

POWER_TERMS = (
    "won't turn on",
    "wont turn on",
    "will not turn on",
    "won't start",
    "wont start",
    "will not start",
    "doesn't start",
    "does not start",
    "no power",
    "lost power",
    "power loss",
    "power failure",
    "power outage",
    "dead",
    "startup failure",
    "startup",
    "electrical fault",
)

SUCCESSFUL_STARTUP_TERMS = (
    "powers on",
    "powered on",
    "powers up",
    "powered up",
    "turns on",
    "turned on",
    "boots up",
    "boots fine",
    "starts up",
    "started up",
    "will power on",
)

IMAGE_QUALITY_TERMS = (
    "image quality",
    "degraded image",
    "poor image",
    "bad image",
    "blurry",
    "blurred",
    "artifact",
    "artifacting",
    "artefact",
    "artefacting",
    "streaking",
    "banding",
    "ghosting",
    "grainy",
    "noise on image",
    "image noise",
    "ringing",
    "calibration drift",
    "fuzzy image",
    "distorted image",
    "image distortion",
)

MODALITY_COMPONENT_TERMS = {
    "X-ray": DETECTOR_TERMS,
    "CT": (
        "detector",
        "das",
        "data acquisition",
        "collimator",
        "slip ring",
        "gantry",
        "tube",
    ),
    "MRI": (
        "coil",
        "phased array",
        "interface box",
        "receiver",
        "table coil",
    ),
    "Ultrasound": (
        "probe",
        "transducer",
        "connector",
        "cable",
        "tgc",
    ),
    "General Medical Equipment": (),
}

DETECTOR_RESPONSES = {
    "X-ray": {
        "category": "Detector / connectivity (X-ray)",
        "possible_cause": (
            "An intermittent X-ray detector communication fault is likely. Common causes include "
            "a loose or damaged detector cable, failing wireless link, outdated or mismatched "
            "firmware, EMI interference, worn flex circuitry in the panel, or a network issue "
            "between the detector and acquisition workstation."
        ),
        "troubleshooting_steps": (
            "1. Review system logs, event history, and error codes at the exact time of dropout.\n"
            "2. Inspect the detector cable, connectors, strain relief, and tray docking contacts.\n"
            "3. Reseat all detector and interface connections; test with a known-good cable if available.\n"
            "4. For wireless detectors, check battery level, pairing status, and wireless signal strength.\n"
            "5. Verify firmware and software versions are compatible across the detector, console, and host.\n"
            "6. Reproduce the issue during an exam and note whether tube movement, orientation, or exam type triggers it.\n"
            "7. Escalate with captured logs if the fault remains intermittent after cabling and firmware checks."
        ),
        "safety_considerations": (
            "Follow radiation safety and ALARA protocols during live imaging tests. "
            "Do not use damaged detector cables during patient exams. "
            "Coordinate with clinical staff before interrupting workflow or repeating exposures."
        ),
    },
    "CT": {
        "category": "Detector / connectivity (CT)",
        "possible_cause": (
            "An intermittent CT data path or detector communication fault is likely. Common causes include "
            "a failing detector module connection, slip ring communication errors, DAS interface issues, "
            "collimator controller faults, or gantry network interruptions during rotation."
        ),
        "troubleshooting_steps": (
            "1. Review CT console logs, gantry event history, and error codes at the time of the failed scan.\n"
            "2. Inspect detector module, DAS, and collimator cabling through the gantry slip ring path.\n"
            "3. Verify gantry communication links and reseat accessible connectors on the rotating side.\n"
            "4. Check for scan-specific patterns such as failures only at certain rotation speeds or collimation settings.\n"
            "5. Confirm firmware versions for the gantry, DAS, and workstation are compatible.\n"
            "6. Run a low-dose calibration or air scan if supported by the service manual.\n"
            "7. Escalate with saved raw data logs if the fault remains intermittent."
        ),
        "safety_considerations": (
            "Follow radiation and mechanical safety procedures around rotating gantry components. "
            "Do not bypass interlocks. Coordinate with staff before repeating patient scans."
        ),
    },
    "MRI": {
        "category": "Coil / connectivity (MRI)",
        "possible_cause": (
            "An intermittent MRI coil or communication fault is likely. Common causes include "
            "a damaged coil cable, loose connector at the interface box, failing phased-array element, "
            "RF path interruption, or table/coils not recognized by the host during exam setup."
        ),
        "troubleshooting_steps": (
            "1. Review MRI system logs and coil recognition errors at the time of failure.\n"
            "2. Inspect coil cables, connectors, and strain relief at the patient table interface.\n"
            "3. Reseat coil connections and test with a known-good coil of the same type.\n"
            "4. Verify coil selection, routing, and interface box status before the exam starts.\n"
            "5. Check for failures tied to specific coil types, table positions, or scan sequences.\n"
            "6. Confirm compatible firmware between coils, interface hardware, and the scanner host.\n"
            "7. Escalate with service logs if coil dropout remains intermittent."
        ),
        "safety_considerations": (
            "Follow MRI safety zones and ferromagnetic restrictions in Zone III/IV. "
            "Do not introduce unauthorized tools or devices near the magnet. "
            "Coordinate with staff before repeating scans on a patient."
        ),
    },
    "Ultrasound": {
        "category": "Probe / connectivity (Ultrasound)",
        "possible_cause": (
            "An intermittent ultrasound probe or transducer communication fault is likely. Common causes include "
            "a worn probe connector, internal cable break, damaged transducer elements, loose port connection, "
            "or overheating at the probe head during extended use."
        ),
        "troubleshooting_steps": (
            "1. Review system error messages and note whether the fault occurs on one probe port or all ports.\n"
            "2. Inspect the probe connector, cable, and strain relief for cracks, bends, or loose pins.\n"
            "3. Reseat the probe and test on another port or with a known-good probe.\n"
            "4. Check whether image dropout happens with certain presets, depths, or exam durations.\n"
            "5. Verify probe software options and firmware are licensed and compatible with the system.\n"
            "6. Document whether physical probe movement reproduces the fault.\n"
            "7. Escalate for probe repair or replacement if internal cable or element failure is suspected."
        ),
        "safety_considerations": (
            "Follow electrical safety and infection control procedures for probes used on patients. "
            "Do not use damaged probe cables during exams. "
            "Use appropriate probe covers and handle disinfection requirements after testing."
        ),
    },
    "General Medical Equipment": {
        "category": "Device / connectivity (general)",
        "possible_cause": (
            "An intermittent device communication fault is likely. Common causes include "
            "a loose or damaged cable, failing wireless link, outdated or mismatched firmware, "
            "EMI interference, or a network issue between the device and host system."
        ),
        "troubleshooting_steps": (
            "1. Review system logs, event history, and error codes at the exact time of dropout.\n"
            "2. Inspect cables, connectors, strain relief, and docking contacts.\n"
            "3. Reseat all device and interface connections; test with a known-good cable if available.\n"
            "4. For wireless devices, check battery level, pairing status, and signal strength.\n"
            "5. Verify firmware and software versions are compatible across connected components.\n"
            "6. Reproduce the issue during normal use and note operating conditions when it occurs.\n"
            "7. Escalate with captured logs if the fault remains intermittent."
        ),
        "safety_considerations": (
            "Follow site-specific safety procedures and manufacturer service guidance. "
            "Do not use damaged cables during patient care. "
            "Coordinate with clinical staff before interrupting workflow."
        ),
    },
}

EQUIPMENT_ADJUSTMENTS = {
    "Overheating": {
        "X-ray": (
            "On X-ray systems, also check tube housing cooling, anode heat units, and collimator fan operation.",
            "Review tube heat management records and recent high-load exam history.",
            "Monitor tube thermal indicators before repeating exposures.",
        ),
        "CT": (
            "On CT systems, also inspect gantry tube cooling, heat exchangers, and air circulation through the bore.",
            "Review tube scan seconds and heat storage values before additional testing.",
            "Allow adequate tube cooling time between test scans.",
        ),
        "MRI": (
            "On MRI systems, verify chiller performance, gradient coil cooling, and room HVAC supplying the equipment area.",
            "Review cryogen/helium levels and recent compressor or chiller alarms.",
            "Do not disable cooling interlocks during troubleshooting.",
        ),
        "Ultrasound": (
            "On ultrasound systems, check probe head temperature during extended scanning and console ventilation.",
            "Allow the probe to cool and retest with a shorter exam duration.",
            "Inspect cooling fans and cabinet airflow on the main unit.",
        ),
    },
    "Power / startup": {
        "X-ray": (
            "Verify generator, collimator, and workstation power circuits separately on X-ray systems.",
            "Check exposure hand switch and room door interlock circuits.",
            "Confirm generator ready indicators before testing exposures.",
        ),
        "CT": (
            "Verify gantry, console, and uninterruptible power supplies separately on CT systems.",
            "Check gantry rotation enable circuits and emergency stop status.",
            "Review UPS or power conditioning alarms in the equipment room.",
        ),
        "MRI": (
            "Verify scanner, gradient amplifier, and chiller power feeds separately on MRI systems.",
            "Check quench circuit status and emergency stop inputs before energizing subsystems.",
            "Allow adequate time for system boot and cold-head recovery after power events.",
        ),
        "Ultrasound": (
            "Verify main console and optional cart power supplies on ultrasound systems.",
            "Check probe port power and connector seating after startup.",
            "Confirm software licensing and probe initialization complete successfully.",
        ),
    },
    "General equipment": {
        "X-ray": (
            "Confirm generator, collimator, and image processing subsystems on this X-ray unit.",
            "Review recent exposure errors and detector calibration status.",
        ),
        "CT": (
            "Confirm gantry, DAS, and reconstruction workstation status on this CT scanner.",
            "Review recent scan abort codes and calibration due dates.",
        ),
        "MRI": (
            "Confirm magnet, gradient, RF, and workstation subsystems on this MRI scanner.",
            "Review recent coil errors, table interlocks, and scheduled maintenance items.",
        ),
        "Ultrasound": (
            "Confirm probe ports, beamformer, and software presets on this ultrasound system.",
            "Review recent probe-related service messages and exam presets in use.",
        ),
    },
}


def _contains_any(text: str, phrases: tuple[str, ...]) -> bool:
    return any(phrase in text for phrase in phrases)


def _normalize_equipment_type(equipment_type: str) -> str:
    if equipment_type in EQUIPMENT_TYPES:
        return equipment_type
    return "General Medical Equipment"


def _is_detector_connectivity_issue(text: str, equipment_type: str) -> bool:
    equipment_type = _normalize_equipment_type(equipment_type)
    has_detector = _contains_any(text, DETECTOR_TERMS)
    has_connectivity = _contains_any(text, CONNECTIVITY_TERMS)
    has_imaging = _contains_any(text, IMAGING_TERMS)
    has_symptom = _contains_any(text, SYMPTOM_TERMS)
    modality_terms = MODALITY_COMPONENT_TERMS.get(equipment_type, ())

    if has_detector and (has_connectivity or has_symptom or has_imaging):
        return True

    if has_connectivity and has_imaging:
        return True

    if _contains_any(
        text,
        (
            "detector cable",
            "wireless detector",
            "panel connection",
            "panel disconnect",
            "detector timeout",
            "detector communication",
            "dr system",
            "digital radiography",
        ),
    ):
        return True

    if equipment_type == "General Medical Equipment":
        return False

    modality_terms = MODALITY_COMPONENT_TERMS.get(equipment_type, ())
    if has_connectivity and (
        _contains_any(text, modality_terms) or has_symptom or has_imaging
    ):
        return True

    return _contains_any(text, modality_terms) and has_connectivity


def _is_power_issue(text: str, equipment_type: str) -> bool:
    if _is_detector_connectivity_issue(text, equipment_type):
        return False

    if _contains_any(text, POWER_TERMS):
        return True

    if "power" in text and not _contains_any(
        text,
        ("power cord", "power cable", "battery power", "detector power"),
    ):
        return True

    return False


def _apply_equipment_adjustments(
    response: dict[str, str],
    equipment_type: str,
    issue_category: str,
) -> dict[str, str]:
    equipment_type = _normalize_equipment_type(equipment_type)
    adjustments = EQUIPMENT_ADJUSTMENTS.get(issue_category, {}).get(equipment_type)
    if not adjustments:
        return response

    cause_extra, *step_extras = adjustments
    updated_steps = response["troubleshooting_steps"]
    next_number = updated_steps.count("\n") + 2
    for step in step_extras:
        updated_steps += f"\n{next_number}. {step.rstrip('.')}."
        next_number += 1

    return {
        **response,
        "equipment_type": equipment_type,
        "possible_cause": f"{response['possible_cause']} {cause_extra}",
        "troubleshooting_steps": updated_steps,
    }


def _build_response(
    category: str,
    possible_cause: str,
    troubleshooting_steps: str,
    safety_considerations: str,
    equipment_type: str,
) -> dict[str, str]:
    response = {
        "category": category,
        "equipment_type": _normalize_equipment_type(equipment_type),
        "possible_cause": possible_cause,
        "troubleshooting_steps": troubleshooting_steps,
        "safety_considerations": safety_considerations,
    }
    return _apply_equipment_adjustments(response, equipment_type, category)


def generate_response(
    problem_description: str,
    equipment_type: str = "General Medical Equipment",
) -> dict[str, str]:
    """Return a simulated troubleshooting response for the given problem."""
    problem = problem_description.strip().lower()
    equipment_type = _normalize_equipment_type(equipment_type)

    if not problem:
        return {
            "category": "Input required",
            "equipment_type": equipment_type,
            "possible_cause": "No problem description was provided.",
            "troubleshooting_steps": "Enter a description of the equipment issue and submit again.",
            "safety_considerations": "Always follow your site safety procedures before inspecting equipment.",
        }

    if _is_detector_connectivity_issue(problem, equipment_type):
        response = {
            **DETECTOR_RESPONSES[equipment_type],
            "equipment_type": equipment_type,
        }
        return response

    if any(word in problem for word in ("overheat", "hot", "temperature", "thermal")):
        return _build_response(
            "Overheating",
            (
                "Restricted airflow, a failing cooling fan, or blocked heat exchangers "
                "may be causing the equipment to overheat."
            ),
            (
                "1. Power down the unit and allow it to cool.\n"
                "2. Inspect air filters, vents, and fans for blockage or damage.\n"
                "3. Verify ambient temperature is within the manufacturer's limits.\n"
                "4. Check that all cooling components are running when the unit is powered on.\n"
                "5. Review recent maintenance logs for recurring overheating events."
            ),
            (
                "Allow hot surfaces to cool before touching them. "
                "Use appropriate PPE and lock out / tag out the equipment before internal inspection."
            ),
            equipment_type,
        )

    if any(word in problem for word in ("leak", "drip", "fluid", "oil", "water")):
        return _build_response(
            "Fluid leak",
            (
                "A worn seal, loose fitting, cracked hose, or overfilled reservoir "
                "may be causing fluid leakage."
            ),
            (
                "1. Identify the fluid type and trace the leak to its source.\n"
                "2. Tighten accessible fittings and inspect seals and hoses.\n"
                "3. Check fluid levels and look for signs of contamination.\n"
                "4. Replace damaged components and verify the leak has stopped.\n"
                "5. Monitor the system under normal operating conditions."
            ),
            (
                "Wear chemical-resistant gloves and eye protection. "
                "Contain spills, ventilate the area, and follow SDS guidance for the leaked fluid."
            ),
            equipment_type,
        )

    if any(word in problem for word in ("noise", "vibration", "rattle", "grinding", "hum")):
        return _build_response(
            "Noise / vibration",
            (
                "Loose mounting hardware, worn bearings, misalignment, or a failing motor "
                "may be causing unusual noise or vibration."
            ),
            (
                "1. Record when the noise occurs (startup, under load, idle).\n"
                "2. Inspect mounts, bolts, and coupling alignment.\n"
                "3. Check rotating components for wear or obstruction.\n"
                "4. Compare vibration or sound levels to baseline readings if available.\n"
                "5. Schedule replacement of worn bearings or belts if damage is confirmed."
            ),
            (
                "Do not reach into moving parts. "
                "Use lock out / tag out before inspecting belts, fans, or drive components."
            ),
            equipment_type,
        )

    if _is_power_issue(problem, equipment_type):
        return _build_response(
            "Power / startup",
            (
                "A tripped breaker, blown fuse, loose wiring, or a failed control module "
                "may be preventing the equipment from starting."
            ),
            (
                "1. Verify supply voltage at the disconnect or main input.\n"
                "2. Check breakers, fuses, and emergency stop circuits.\n"
                "3. Inspect control panel indicators and error codes.\n"
                "4. Confirm all safety interlocks are satisfied.\n"
                "5. Test the control relay or starter if power is present but the unit will not run."
            ),
            (
                "Only qualified personnel should work on live electrical systems. "
                "Follow LOTO procedures and use a multimeter rated for the circuit voltage."
            ),
            equipment_type,
        )

    return _build_response(
        "General equipment",
        (
            "The reported symptoms may be caused by normal wear, an intermittent fault, "
            "or a component that requires further inspection on site."
        ),
        (
            "1. Gather equipment model, serial number, and recent maintenance history.\n"
            "2. Reproduce the issue and note operating conditions when it occurs.\n"
            "3. Perform a visual inspection for obvious damage, leaks, or loose connections.\n"
            "4. Check error codes, alarms, and sensor readings against the service manual.\n"
            "5. Escalate to technical support if the root cause is not identified."
        ),
        (
            "Follow site-specific safety procedures, wear required PPE, "
            "and de-energize equipment before hands-on troubleshooting."
        ),
        equipment_type,
    )
