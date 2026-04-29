import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor

from .. import CONF_PIPSOLAR_ID, PIPSOLAR_COMPONENT_SCHEMA

DEPENDENCIES = ["uart"]

pipsolar_ns = cg.esphome_ns.namespace("pipsolar")
Pipsolar = pipsolar_ns.class_("Pipsolar")
PipsolarSensor = pipsolar_ns.class_("PipsolarSensor", cg.Component)

# -------------------------------
# SENSOR KEYS (DEDUPED + CLEANED)
# -------------------------------
TYPES = [
    "grid_rating_voltage",
    "grid_rating_current",
    "ac_output_rating_voltage",
    "ac_output_rating_frequency",
    "ac_output_rating_current",
    "ac_output_rating_apparent_power",
    "ac_output_rating_active_power",
    "battery_rating_voltage",
    "battery_recharge_voltage",
    "battery_under_voltage",
    "battery_bulk_voltage",
    "battery_float_voltage",
    "battery_type",
    "current_max_ac_charging_current",
    "current_max_charging_current",
    "input_voltage_range",
    "output_source_priority",
    "charger_source_priority",
    "parallel_max_num",
    "machine_type",
    "topology",
    "output_mode",
    "battery_redischarge_voltage",
    "pv_ok_condition_for_parallel",
    "pv_power_balance",
    "grid_voltage",
    "grid_frequency",
    "ac_output_voltage",
    "ac_output_frequency",
    "ac_output_apparent_power",
    "ac_output_active_power",
    "output_load_percent",
    "bus_voltage",
    "battery_voltage",
    "battery_charging_current",
    "battery_capacity_percent",
    "inverter_heat_sink_temperature",
    "pv_input_current_for_battery",
    "pv_input_voltage",
    "battery_voltage_scc",
    "battery_discharge_current",
    "battery_voltage_offset_for_fans_on",
    "eeprom_version",
    "pv_charging_power",
]

# -------------------------------
# MODERN SAFE SCHEMA
# -------------------------------
CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(PipsolarSensor),
        cv.Required(CONF_PIPSOLAR_ID): cv.use_id(Pipsolar),
        cv.Optional("sensors", default=[]): cv.ensure_list(cv.one_of(*TYPES)),
    }
).extend(PIPSOLAR_COMPONENT_SCHEMA)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_PIPSOLAR_ID])

    var = cg.new_Pvariable(config[CONF_ID])
    cg.add(var.set_parent(parent))

    await cg.register_component(var, config)

    # enable only requested sensors
    for t in config.get("sensors", []):
        cg.add(getattr(var, f"enable_{t}")())
