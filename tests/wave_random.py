import math
import time
import random

def _random(min: float,
            max: float,
            x_scale: float = 1,
            noise: float = 0.05) -> float:
    """Generates a psuedo-random number following a time-based sine wave.

    Numbers are based on variations of a sine wave which is calculated
    from the last 2 seconds of the current time.

    The noise component of the wave is randomised

    Parameters
    ----------
    min: float
        Minimum value of the noiseless waveform (with noise the
        calculated value cannot go below 0)
    max: float
        Maximum number of the noiseless waveform
    x_scale: float
        The horizontal scale factor of the waveform
    noise: float
        The noise factor to apply to the waveform (should be between 0 and
        0.5, 0.1 is recommended as a sensible maximum)
    """
    seed = time.time() % 100
    rads = seed * 2 * 3.1415926535 / 100
    jitter = random.uniform(-noise, noise)
    # Produce a sine wave between 0 and 1 and add jitter
    wave = 0.5 * (math.sin(rads / x_scale) + 1) + jitter
    print(f"seed = {seed}")
    print(f"rads = {rads}")
    print(f"jitter = {jitter}")
    print(f"wave = {wave}")

    # Scale the sine wave from the user parameters
    result = min + (max - min) * wave
    if result < 0:
        result = 0
    return result

print(_random(5, 10))
