"""
quantum_name_generator.py
Generate unique, futuristic, and quantum-inspired names.
Premium-level version with 300+ elements.
"""

import random
import string

# ------------------------------
# Prefixes (100+)
# ------------------------------
PREFIXES = [
    "Neo", "Quantum", "Hyper", "Nano", "Cyber", "Proto", "Meta", "Astro", "Electro", "Alpha",
    "Omega", "Sigma", "Delta", "Photon", "Lumi", "Vortex", "Stellar", "Chrono", "Galacto", "Plasma",
    "Cryo", "Magno", "Terra", "Aero", "Ion", "Cosmo", "Orbi", "Psycho", "Lux", "Xeno",
    "Nova", "Astra", "Solar", "Lunar", "Electra", "Volt", "Circuit", "Fusion", "Binary", "OmegaX",
    "Nebula", "Celesti", "QuantumX", "ProtoX", "NanoX", "HyperX", "CyberX", "AstroX", "NeoX", "MetaX",
    "Zeno", "CryoX", "PhotonX", "AlphaX", "OmegaPrime", "LumiX", "StellarX", "VortexX", "TerraX", "MagnoX",
    "Xylo", "Orion", "Pulsar", "Gamma", "Epsilon", "SigmaX", "DeltaX", "Omega2", "NanoPrime", "ProtoPrime",
    "ChronoX", "GalactoX", "CryoPrime", "PhotonPrime", "LuxPrime", "XenoPrime", "NeoPrime", "MetaPrime", "AstroPrime", "CyberPrime",
    "AeroX", "ElectroPrime", "SolarX", "LunarX", "VoltPrime", "FusionPrime", "CircuitPrime", "BinaryPrime", "NebulaX", "CelestiX",
    "QuantumPrime", "ProtoNeo", "NanoNeo", "HyperNeo", "CyberNeo", "AstroNeo", "NeoNeo", "MetaNeo", "ZenoNeo", "CryoNeo"
]

# ------------------------------
# Midfixes (100+)
# ------------------------------
MIDFIXES = [
    "tron", "plex", "nix", "core", "flux", "wave", "byte", "grid", "sphere", "pulse",
    "matrix", "vector", "phase", "cycle", "lattice", "node", "field", "quantum", "circuit", "link",
    "beam", "path", "loop", "stream", "network", "beamX", "nanoFlux", "cyberNet", "astroLink", "metaWave",
    "plasmaX", "photonix", "lumiCore", "chronoGrid", "stellarNode", "vortexSphere", "ionCycle", "cosmoPath", "psychoBeam", "voltStream",
    "fusionMatrix", "binaryLoop", "nebulaLink", "celestiField", "quantumStream", "protoNode", "nanoBeam", "hyperWave", "cyberFlux", "astroCircuit",
    "neoVector", "metaLoop", "zenoPhase", "cryoPath", "photonGrid", "alphaSphere", "omegaPulse", "lumiMatrix", "stellarLink", "vortexField",
    "terraNode", "magnoBeam", "xenoCycle", "novaStream", "astraWave", "solarMatrix", "lunarNode", "electraLoop", "voltBeam", "circuitX",
    "fusionPath", "binarySphere", "nebulaBeam", "celestiPulse", "quantumFlux", "protoLoop", "nanoNode", "hyperCycle", "cyberBeam", "astroStream",
    "neoCircuit", "metaGrid", "zenoLink", "cryoNode", "photonPath", "alphaLoop", "omegaBeam", "lumiSphere", "stellarMatrix", "vortexPulse",
    "terraFlux", "magnoLoop", "xenoBeam", "novaCycle", "astraNode", "solarPath", "lunarFlux", "electraSphere", "voltLoop", "circuitPrime"
]

# ------------------------------
# Suffixes (100+)
# ------------------------------
SUFFIXES = [
    "on", "ium", "ara", "os", "ex", "ix", "el", "ar", "is", "or",
    "eus", "ion", "ixPrime", "ax", "isX", "orX", "iumX", "araX", "exPrime", "elX",
    "arPrime", "osX", "ius", "osPrime", "ixNeo", "elNeo", "arNeo", "isNeo", "onNeo",
    "ionNeo", "eusNeo", "axNeo", "orNeo", "iumNeo", "araNeo", "exNeo", "elPrime", "arPrimeX", "isPrime",
    "onPrime", "ionPrime", "eusPrime", "ixPrimeNeo", "axPrime", "orPrime", "iumPrime", "araPrime", "exPrimeNeo", "elPrimeNeo",
    "arNeoPrime", "osNeo", "iusNeo", "osPrimeNeo", "ixNeoPrime", "elNeoPrime", "arNeoX", "isNeoX", "onNeoX", "ionNeoX",
    "eusNeoX", "axNeoX", "orNeoX", "iumNeoX", "araNeoX", "exNeoX", "elXPrime", "arXPrime", "isXPrime", "onXPrime",
    "ionXPrime", "eusXPrime", "ixXPrime", "axXPrime", "orXPrime", "iumXPrime", "araXPrime", "exXPrime", "elXNeo", "arXNeo",
    "isXNeo", "onXNeo", "ionXNeo", "eusXNeo", "ixXNeo", "axXNeo", "orXNeo", "iumXNeo", "araXNeo", "exXNeo",
    "elXNeoPrime", "arXNeoPrime", "isXNeoPrime", "onXNeoPrime", "ionXNeoPrime", "eusXNeoPrime", "ixXNeoPrime", "axXNeoPrime", "orXNeoPrime", "iumXNeoPrime"
]

def generate_name(seed: str = None) -> str:
    """Generate a single premium quantum-inspired name."""
    if seed:
        random.seed(seed)
    prefix = random.choice(PREFIXES)
    midfix = random.choice(MIDFIXES)
    suffix = random.choice(SUFFIXES)
    number_suffix = str(random.randint(0, 999))
    return f"{prefix}{midfix}{suffix}{number_suffix}"

def batch_generate(n: int = 10) -> list:
    """Generate a batch of unique premium names."""
    names = set()
    while len(names) < n:
        name = generate_name()
        names.add(name)
    return list(names)

def random_seed_name() -> str:
    """Generate a name using a random string seed for uniqueness."""
    seed = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    return generate_name(seed=seed)

# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    print("Single Premium Quantum Name:")
    print(generate_name())
    
    print("\nBatch of 15 Premium Names:")
    for n in batch_generate(15):
        print(f" - {n}")
    
    print("\nRandom Seed Premium Name:")
    print(random_seed_name())