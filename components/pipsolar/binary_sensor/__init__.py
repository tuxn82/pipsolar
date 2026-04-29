import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor

from .. import PIPSOLAR_COMPONENT_SCHEMA, CONF_PIPSOLAR_ID

DEPENDENCIES = ["uart"]

CONF_TYPES = "types"

pipsolar_ns = cg.esphome_ns.namespace("pipsolar")
Pipsolar = pipsolar_ns.class_("Pipsolar")
PipsolarBinarySensor = pipsolar_ns.class_("PipsolarBinarySensor", cg.Component)

# ---- ALL AVAILABLE TYPES ----
TYPES = [
    "add_sbu_priority_version",
    "configuration_status",
    "scc_firmware_version",
    "load_status",
    "battery_voltage_to_steady_while_charging",
    "charging_status",
    "scc_charging_status",
    "ac_charging_status",
    "charging_to_floating_mode",
    "switch_on",
    "dustproof_installed",
    "silence_buzzer_open_buzzer",
    "overload_bypass_function",
    "lcd_escape_to_default",
    "overload_restart_function",
    "over_temperature_restart_function",
    "backlight_on",
    "alarm_on_when_primary_source_interrupt",
    "fault_code_record",
    "power_saving",
    "warnings_present",
    "faults_present",
    "warning_power_loss",
    "fault_inverter_fault",
    "fault_bus_over",
    "fault_bus_under",
    "fault_bus_soft_fail",
    "warning_line_fail",
    "fault_opvshort",
    "fault_inverter_voltage_too_low",
    "fault_inverter_voltage_too_high",
    "warning_over_temperature",
    "warning_fan_lock",
    "warning_battery_voltage_high",
    "warning_battery_low_alarm",
    "warning_battery_under_shutdown",
    "warning_battery_derating",
    "warning_over_load",
    "warning_eeprom_failed",
    "fault_inverter_over_current",
    "fault_inverter_soft_failed",
    "fault_self_test_failed",
    "fault_op_dc_voltage_over",
    "fault_battery_open",
    "fault_current_sensor_failed",
    "fault_battery_short",
    "warning_power_limit",
    "warning_pv_voltage_high",
    "fault_mppt_overload",
    "warning_mppt_overload",
    "warning_battery_too_low_to_charge",
    "fault_dc_dc_over_current",
    "fault_code",
    "warnung_low_pv_energy",
    "warning_high_ac_input_during_bus_soft_start",
    "warning_battery_equalization",
    "discharge_onoff",
    "discharge_with_standby_onoff",
    "charge_onoff",
]

# ---- NEW SAFE SCHEMA (ESPHome 2026 COMPATIBLE) ----
CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(PipsolarBinarySensor),
        cv.Required(CONF_PIPSOLAR_ID): cv.use_id(Pipsolar),
        cv.Optional(CONF_TYPES, default=[]): cv.ensure_list(cv.one_of(*TYPES)),
    }
).extend(PIPSOLAR_COMPONENT_SCHEMA)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_PIPSOLAR_ID])

    # create container component
    var = cg.new_Pvariable(config[CONF_ID])
    cg.add(var.set_parent(parent))

    # register component properly
    await cg.register_component(var, config)

    # dynamically enable only selected sensors
    for t in config.get(CONF_TYPES, []):
        cg.add(getattr(var, f"enable_{t}")())
