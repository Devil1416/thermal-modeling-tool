"""Simple resistor-capacitor nodal thermal network."""
from dataclasses import dataclass, field

@dataclass
class ThermalNode:
    node_id: str
    temperature: float       # K
    capacitance: float       # J/K
    power_input: float = 0.0 # W

@dataclass
class Conductor:
    node_a: str
    node_b: str
    conductance: float       # W/K

def step(nodes: dict[str, ThermalNode],
         conductors: list[Conductor],
         dt: float) -> None:
    """Forward-Euler time step of the nodal network."""
    dT: dict[str, float] = {nid: 0.0 for nid in nodes}
    for c in conductors:
        na, nb = nodes[c.node_a], nodes[c.node_b]
        heat_flow = c.conductance * (na.temperature - nb.temperature)
        dT[c.node_a] -= heat_flow
        dT[c.node_b] += heat_flow
    for nid, node in nodes.items():
        dT[nid] += node.power_input
        node.temperature += dt * dT[nid] / node.capacitance
