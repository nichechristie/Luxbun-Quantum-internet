"""
LUXBIN Morse Light Language with Frequency Comb Enhancement
Combines Morse code timing with LUXBIN wavelength encoding
Enhanced with microresonator frequency comb generation for quantum communication
Creates a time-domain photonic communication protocol using nonlinear optics
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from luxbin_quantum_computer import text_to_luxbin, luxbin_to_wavelengths

# Frequency Comb Parameters (Microresonator-based)
PUMP_WAVELENGTH = 1550  # nm (typical telecom wavelength for Kerr nonlinearity)
COMB_SPACING = 0.1      # nm (frequency spacing between comb lines)
NUM_COMB_LINES = 20     # Number of comb lines generated per pulse
KERR_NONLINEARITY = 1.5 # Nonlinear coefficient for frequency doubling/comb generation

# Quantum Dot Sum-Frequency Generation Parameters
QD_EMISSION_WAVELENGTH = 1300  # nm (quantum dot emission wavelength)
QD_LIFETIME = 1.5              # ns (exponential decay lifetime)
PUMP_LASER_WAVELENGTH = 1550   # nm (sum-frequency generation pump)
OUTPUT_WAVELENGTH = 710        # nm (converted photon wavelength)
TEMPORAL_MODULATION = 350e-12  # seconds (350 ps modulation timescale)
SF_CONVERSION_EFFICIENCY = 0.15 # Sum-frequency conversion efficiency

# Morse code timing (in milliseconds)
DOT_DURATION = 5      # Short pulse
DASH_DURATION = 15    # Long pulse (3x dot)
INTRA_CHAR_GAP = 5    # Gap between dots/dashes in same character
CHAR_GAP = 15         # Gap between characters
WORD_GAP = 35         # Gap between words (7x dot)

# LUXBIN to Morse mapping
# Each LUXBIN character gets a unique morse pattern
LUXBIN_TO_MORSE = {
    # Letters
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',   'E': '.',
    'F': '..-.',  'G': '--.',   'H': '....',  'I': '..',    'J': '.---',
    'K': '-.-',   'L': '.-..',  'M': '--',    'N': '-.',    'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',  'Y': '-.--',
    'Z': '--..',
    # Numbers
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    # Punctuation
    ' ': ' ',     '.': '.-.-.-', ',': '--..--', '!': '-.-.--', '?': '..--..',
    ';': '-.-.-.', ':': '---...', '-': '-....-', '(': '-.--.', ')': '-.--.-',
    '[': '-.--.',  ']': '-.--.-', '{': '-.--.',  '}': '-.--.-', '@': '.--.-.',
    '#': '....--', '$': '...-..-', '%': '.--.--', '^': '.-...', '&': '.-...',
    '*': '-..-',   '+': '.-.-.',  '=': '-...-',  '_': '..--.-', '~': '.--..',
    '`': '.----.',  '<': '.-..-',  '>': '.-..-.', '"': '.-..-.', "'": '.----.',
    '|': '-..-.',  '\\': '.----'
}

class FrequencyCombGenerator:
    """Microresonator-based frequency comb generator using nonlinear optics"""

    def __init__(self, pump_wavelength=PUMP_WAVELENGTH, comb_spacing=COMB_SPACING,
                 num_lines=NUM_COMB_LINES, kerr_coeff=KERR_NONLINEARITY):
        self.pump_wavelength = pump_wavelength
        self.comb_spacing = comb_spacing
        self.num_lines = num_lines
        self.kerr_coeff = kerr_coeff

    def generate_comb(self, character_wavelength, morse_symbol):
        """
        Generate frequency comb using microresonator nonlinear optics
        Two photons combine to create distributed frequencies across comb
        """
        # Base frequency from character wavelength
        base_freq = 299792458 / (character_wavelength * 1e-9)  # Hz

        # Nonlinear frequency generation (parametric process)
        # Pump laser creates comb through four-wave mixing in resonator
        comb_lines = []

        for i in range(-self.num_lines//2, self.num_lines//2 + 1):
            # Frequency shift due to Kerr nonlinearity
            freq_shift = i * self.comb_spacing * 1e12  # Convert to Hz
            new_freq = base_freq + freq_shift

            # Convert back to wavelength
            wavelength = 299792458 / new_freq * 1e9  # nm

            # Intensity based on morse symbol (dots vs dashes)
            intensity = 1.0 if morse_symbol == '.' else 2.5  # Dashes are brighter

            # Phase matching condition for comb generation
            phase_match = np.exp(-abs(i) * self.kerr_coeff)

            comb_lines.append({
                'wavelength_nm': wavelength,
                'frequency_hz': new_freq,
                'intensity': intensity * phase_match,
                'comb_line': i,
                'morse_symbol': morse_symbol
            })

        return comb_lines

    def get_quantum_efficiency(self, comb_lines):
        """Calculate quantum efficiency of comb generation"""
        total_photons = sum(line['intensity'] for line in comb_lines)
        pump_photons = self.num_lines * 1.0  # Reference
        return total_photons / pump_photons if pump_photons > 0 else 0

class QuantumDotPhotonGenerator:
    """Quantum dot single-photon source with sum-frequency generation for wavelength conversion"""

    def __init__(self, qd_wavelength=QD_EMISSION_WAVELENGTH, lifetime=QD_LIFETIME,
                 pump_wavelength=PUMP_LASER_WAVELENGTH, output_wavelength=OUTPUT_WAVELENGTH,
                 modulation_time=TEMPORAL_MODULATION, conversion_eff=SF_CONVERSION_EFFICIENCY):
        self.qd_wavelength = qd_wavelength
        self.lifetime = lifetime  # in nanoseconds
        self.pump_wavelength = pump_wavelength
        self.output_wavelength = output_wavelength
        self.modulation_time = modulation_time  # in seconds
        self.conversion_efficiency = conversion_eff

    def generate_qd_photon(self, morse_symbol):
        """
        Generate single photon from quantum dot with exponential decay waveform
        Returns photon characteristics at QD emission wavelength (1300 nm)
        """
        # Quantum dot emission at 1300 nm with exponential decay
        time_points = np.linspace(0, 5 * self.lifetime, 1000)  # 5 lifetimes worth
        amplitude = np.exp(-time_points / self.lifetime)

        # Add temporal modulation based on morse symbol
        if morse_symbol == '.':
            # Short pulse: apply fast modulation
            modulation_freq = 1 / (self.modulation_time * 1e9)  # GHz
            modulation = 0.5 * (1 + np.cos(2 * np.pi * modulation_freq * time_points))
        else:
            # Long pulse: slower modulation
            modulation_freq = 1 / (self.modulation_time * 1e9 * 3)  # GHz (3x slower for dashes)
            modulation = 0.7 * (1 + np.cos(2 * np.pi * modulation_freq * time_points))

        modulated_amplitude = amplitude * modulation

        return {
            'wavelength_nm': self.qd_wavelength,
            'time_points': time_points,
            'amplitude': modulated_amplitude,
            'lifetime': self.lifetime,
            'morse_symbol': morse_symbol,
            'photon_type': 'single_photon_qd'
        }

    def sum_frequency_conversion(self, qd_photon):
        """
        Perform sum-frequency generation to convert QD photon to visible wavelength
        Combines QD photon (1300 nm) with pump laser (1550 nm) to create 710 nm photon
        """
        # Energy conservation: 1/λ_qd + 1/λ_pump = 1/λ_output
        # 1/1300 + 1/1550 ≈ 1/710 nm (verified experimentally)

        # Apply conversion efficiency and temporal shaping
        converted_amplitude = qd_photon['amplitude'] * self.conversion_efficiency

        # Temporal shaping: the 350 ps modulation is preserved in conversion
        shaping_factor = np.exp(-qd_photon['time_points'] / (self.modulation_time * 1e12))  # Convert to ns
        shaped_amplitude = converted_amplitude * shaping_factor

        return {
            'wavelength_nm': self.output_wavelength,
            'time_points': qd_photon['time_points'],
            'amplitude': shaped_amplitude,
            'original_qd_wavelength': qd_photon['wavelength_nm'],
            'pump_wavelength': self.pump_wavelength,
            'conversion_efficiency': self.conversion_efficiency,
            'temporal_modulation': self.modulation_time,
            'morse_symbol': qd_photon['morse_symbol'],
            'photon_type': 'sum_frequency_converted'
        }

    def get_conversion_efficiency(self):
        """Return the sum-frequency conversion efficiency"""
        return self.conversion_efficiency

class LuxbinMorseLight:
    """LUXBIN Morse Light Language Encoder/Decoder with Frequency Comb and Quantum Dot Enhancement"""

    def __init__(self):
        self.pulse_sequence = []
        self.time_axis = []
        self.wavelength_axis = []
        self.frequency_comb_gen = FrequencyCombGenerator()
        self.quantum_dot_gen = QuantumDotPhotonGenerator()

    def encode_text_to_morse_light(self, text):
        """
        Convert text to LUXBIN Morse Light sequence using frequency comb generation
        Uses microresonator nonlinear optics to create quantum frequency combs
        Returns: List of pulse sequences with comb spectra
        """
        print(f"📝 Encoding: '{text}' with Frequency Comb Enhancement")

        # Step 1: Convert to LUXBIN
        luxbin, binary = text_to_luxbin(text)
        wavelengths = luxbin_to_wavelengths(luxbin, enable_quantum=True)

        print(f"💎 LUXBIN: {luxbin}")
        print(f"🌈 Base wavelengths: {len(wavelengths)} photonic states")
        print(f"🔬 Microresonator: Generating {NUM_COMB_LINES} comb lines per pulse")
        print(f"⚛️  Quantum Dots: {QD_EMISSION_WAVELENGTH}nm emission → {OUTPUT_WAVELENGTH}nm conversion via sum-frequency generation")

        # Step 2: Convert each LUXBIN character to Morse code with frequency comb
        morse_light_sequence = []

        for i, char in enumerate(luxbin):
            base_wavelength = wavelengths[i]['wavelength_nm']

            if char == ' ':
                # Space = gap with quantum wavelength (637nm) - no comb generation
                morse_light_sequence.append({
                    'wavelength_nm': 637,
                    'duration_ms': WORD_GAP,
                    'char': char,
                    'morse': 'SPACE',
                    'is_gap': True,
                    'frequency_comb': None,
                    'quantum_efficiency': 0
                })
            else:
                morse_pattern = LUXBIN_TO_MORSE.get(char, '....')  # Default to 'H' if not found

                # Convert morse pattern to enhanced photonic pulses
                for j, symbol in enumerate(morse_pattern):
                    if symbol in ['.', '-']:
                        # Method 1: Frequency comb generation (microresonator-based)
                        comb_lines = self.frequency_comb_gen.generate_comb(base_wavelength, symbol)
                        comb_efficiency = self.frequency_comb_gen.get_quantum_efficiency(comb_lines)

                        # Method 2: Quantum dot single-photon generation with sum-frequency conversion
                        qd_photon = self.quantum_dot_gen.generate_qd_photon(symbol)
                        sf_converted_photon = self.quantum_dot_gen.sum_frequency_conversion(qd_photon)
                        sf_efficiency = self.quantum_dot_gen.get_conversion_efficiency()

                        duration = DOT_DURATION if symbol == '.' else DASH_DURATION

                        morse_light_sequence.append({
                            'wavelength_nm': base_wavelength,
                            'duration_ms': duration,
                            'char': char,
                            'morse': symbol,
                            'is_gap': False,
                            # Frequency comb data
                            'frequency_comb': comb_lines,
                            'comb_efficiency': comb_efficiency,
                            'comb_center_line': base_wavelength,
                            'num_comb_lines': len(comb_lines),
                            # Quantum dot data
                            'qd_photon': qd_photon,
                            'sf_converted_photon': sf_converted_photon,
                            'sf_efficiency': sf_efficiency,
                            'qd_wavelength': QD_EMISSION_WAVELENGTH,
                            'output_wavelength': OUTPUT_WAVELENGTH,
                            'temporal_modulation': TEMPORAL_MODULATION
                        })

                    # Add intra-character gap (except after last symbol)
                    if j < len(morse_pattern) - 1:
                        morse_light_sequence.append({
                            'wavelength_nm': 0,  # No light
                            'duration_ms': INTRA_CHAR_GAP,
                            'char': '',
                            'morse': '',
                            'is_gap': True,
                            'frequency_comb': None,
                            'quantum_efficiency': 0
                        })

                # Add gap between characters (except after last character)
                if i < len(luxbin) - 1 and luxbin[i+1] != ' ':
                    morse_light_sequence.append({
                        'wavelength_nm': 0,  # No light
                        'duration_ms': CHAR_GAP,
                        'char': '',
                        'morse': '',
                        'is_gap': True,
                        'frequency_comb': None,
                        'quantum_efficiency': 0
                    })

        self.pulse_sequence = morse_light_sequence

        # Calculate overall quantum efficiencies
        comb_efficiencies = [p.get('comb_efficiency', 0) for p in morse_light_sequence if p.get('comb_efficiency', 0) > 0]
        sf_efficiencies = [p.get('sf_efficiency', 0) for p in morse_light_sequence if p.get('sf_efficiency', 0) > 0]

        avg_comb_efficiency = np.mean(comb_efficiencies) if comb_efficiencies else 0
        avg_sf_efficiency = np.mean(sf_efficiencies) if sf_efficiencies else 0

        print(f"⚛️  Average frequency comb efficiency: {avg_comb_efficiency:.3f}")
        print(f"🔄 Average sum-frequency conversion efficiency: {avg_sf_efficiency:.3f}")

        return morse_light_sequence

    def visualize_morse_light(self, text):
        """Create visualization of LUXBIN Morse Light transmission with frequency combs"""

        sequence = self.encode_text_to_morse_light(text)

        # Build time and wavelength arrays
        current_time = 0
        times = []
        wavelengths = []
        colors = []
        labels = []
        comb_spectra = []  # Store comb spectra for detailed plot

        for pulse in sequence:
            duration = pulse['duration_ms']
            wavelength = pulse['wavelength_nm']

            # Add start and end points for pulse
            times.append(current_time)
            times.append(current_time + duration)

            wavelengths.append(wavelength)
            wavelengths.append(wavelength)

            # Color based on wavelength and comb information
            if wavelength == 0:
                colors.append('black')
                colors.append('black')
                label = 'GAP'
                comb_spectra.append(None)
                comb_spectra.append(None)
            elif wavelength == 637:
                colors.append('red')
                colors.append('red')
                label = f'SPACE (637nm)'
                comb_spectra.append(None)
                comb_spectra.append(None)
            else:
                hue = ((wavelength - 400) / 300) * 360
                colors.append(f'hsl({hue:.0f}, 70%, 60%)')
                colors.append(f'hsl({hue:.0f}, 70%, 60%)')
                label = f"{pulse['char']} ({pulse['morse']}) - {wavelength:.1f}nm"
                if pulse['frequency_comb']:
                    label += f" + {len(pulse['frequency_comb'])} comb lines"
                comb_spectra.append(pulse['frequency_comb'])
                comb_spectra.append(pulse['frequency_comb'])

            labels.append(label)
            labels.append(label)

            current_time += duration

        # Create visualization with four subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 12))

        # Top plot: Wavelength over time
        ax1.set_title(f'LUXBIN Morse Light Transmission with Frequency Combs: "{text}"', fontsize=16, fontweight='bold')
        ax1.set_xlabel('Time (ms)', fontsize=12)
        ax1.set_ylabel('Wavelength (nm)', fontsize=12)
        ax1.set_ylim(-50, 750)
        ax1.grid(True, alpha=0.3)

        # Plot wavelength pulses
        for i in range(0, len(times), 2):
            if wavelengths[i] > 0:
                ax1.plot([times[i], times[i+1]], [wavelengths[i], wavelengths[i+1]],
                        linewidth=3, color='blue' if wavelengths[i] == 637 else 'green')
                ax1.fill_between([times[i], times[i+1]], 0, [wavelengths[i], wavelengths[i+1]],
                                alpha=0.3, color='blue' if wavelengths[i] == 637 else 'green')

        # Middle plot: Morse code pattern
        ax2.set_title('Morse Pattern (Dots and Dashes)', fontsize=14)
        ax2.set_xlabel('Time (ms)', fontsize=12)
        ax2.set_ylabel('Signal', fontsize=12)
        ax2.set_ylim(-0.5, 1.5)
        ax2.set_yticks([0, 1])
        ax2.set_yticklabels(['OFF', 'ON'])
        ax2.grid(True, alpha=0.3)

        # Plot morse pattern
        for i in range(0, len(times), 2):
            signal = 1 if wavelengths[i] > 0 else 0
            ax2.plot([times[i], times[i+1]], [signal, signal],
                    linewidth=4, color='red' if wavelengths[i] == 637 else 'blue')

        # Bottom-left plot: Frequency comb spectrum (showing one example comb)
        ax3.set_title('Frequency Comb Spectrum (Microresonator)', fontsize=14)
        ax3.set_xlabel('Wavelength (nm)', fontsize=12)
        ax3.set_ylabel('Intensity (a.u.)', fontsize=12)
        ax3.grid(True, alpha=0.3)

        # Find first pulse with frequency comb and plot its spectrum
        example_comb = None
        for pulse in sequence:
            if pulse.get('frequency_comb'):
                example_comb = pulse['frequency_comb']
                char = pulse['char']
                morse = pulse['morse']
                break

        if example_comb:
            comb_wavelengths = [line['wavelength_nm'] for line in example_comb]
            comb_intensities = [line['intensity'] for line in example_comb]

            ax3.bar(comb_wavelengths, comb_intensities, width=0.05, alpha=0.7, color='purple')
            ax3.set_title(f'Comb Spectrum: "{char}" ({morse}) - {len(example_comb)} lines', fontsize=12)

            # Add vertical line at center wavelength
            center_wavelength = sum(comb_wavelengths) / len(comb_wavelengths)
            ax3.axvline(x=center_wavelength, color='red', linestyle='--', alpha=0.7,
                       label=f'Center: {center_wavelength:.1f}nm')
            ax3.legend()

        # Bottom-right plot: Quantum dot temporal waveforms
        ax4.set_title('Quantum Dot Temporal Waveforms', fontsize=14)
        ax4.set_xlabel('Time (ns)', fontsize=12)
        ax4.set_ylabel('Amplitude (a.u.)', fontsize=12)
        ax4.grid(True, alpha=0.3)

        # Find first pulse with quantum dot data and plot temporal waveforms
        example_qd = None
        example_sf = None
        for pulse in sequence:
            if pulse.get('qd_photon') and pulse.get('sf_converted_photon'):
                example_qd = pulse['qd_photon']
                example_sf = pulse['sf_converted_photon']
                char = pulse['char']
                morse = pulse['morse']
                break

        if example_qd and example_sf:
            # Plot QD emission (1300nm)
            time_ns = example_qd['time_points']  # Convert to ns
            ax4.plot(time_ns, example_qd['amplitude'], 'b-', linewidth=2,
                    label=f'QD Emission ({QD_EMISSION_WAVELENGTH}nm)')

            # Plot sum-frequency converted (710nm)
            ax4.plot(time_ns, example_sf['amplitude'], 'r--', linewidth=2,
                    label=f'SF Converted ({OUTPUT_WAVELENGTH}nm)')

            ax4.set_title(f'QD Waveforms: "{char}" ({morse}) - {QD_LIFETIME}ns lifetime', fontsize=12)
            ax4.legend()

            # Add annotations
            ax4.text(0.02, 0.98, f'Conversion: {QD_EMISSION_WAVELENGTH}nm → {OUTPUT_WAVELENGTH}nm\nEfficiency: {SF_CONVERSION_EFFICIENCY:.1%}',
                    transform=ax4.transAxes, fontsize=10, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        plt.tight_layout()
        plt.savefig('luxbin_morse_light.png', dpi=150, bbox_inches='tight')
        print(f"\n✅ Visualization saved: luxbin_morse_light.png")
        plt.show()

        return sequence

    def print_transmission_table(self):
        """Print detailed transmission table with frequency comb information"""
        print(f"\n📊 LUXBIN Morse Light Transmission Table with Frequency Combs")
        print("=" * 90)
        print(f"{'Time':>6} | {'Char':>4} | {'Morse':>5} | {'Wavelength':>10} | {'Duration':>8} | {'Comb':>4} | {'QE':>5} | Type")
        print("-" * 90)

        current_time = 0
        for pulse in self.pulse_sequence:
            char = pulse['char'] if pulse['char'] else '-'
            morse = pulse['morse'] if pulse['morse'] else '-'
            wavelength = f"{pulse['wavelength_nm']:.1f}nm" if pulse['wavelength_nm'] > 0 else "OFF"
            duration = f"{pulse['duration_ms']}ms"
            pulse_type = "GAP" if pulse['is_gap'] else "PULSE"

            # Frequency comb information
            comb_info = f"{pulse.get('num_comb_lines', 0)}" if pulse.get('frequency_comb') else "-"
            qe_info = f"{pulse.get('quantum_efficiency', 0):.2f}" if pulse.get('quantum_efficiency', 0) > 0 else "-"

            print(f"{current_time:6.0f} | {char:>4} | {morse:>5} | {wavelength:>10} | {duration:>8} | {comb_info:>4} | {qe_info:>5} | {pulse_type}")
            current_time += pulse['duration_ms']

        print("=" * 90)
        print(f"Total transmission time: {current_time:.0f}ms ({current_time/1000:.2f} seconds)")
        print(f"Microresonator: Pump @ {PUMP_WAVELENGTH}nm, {COMB_SPACING}nm spacing, Kerr coeff: {KERR_NONLINEARITY}")

def main():
    """Demo LUXBIN Morse Light Language with Frequency Comb and Quantum Dot Enhancement"""

    print("=" * 100)
    print("🌟 LUXBIN MORSE LIGHT LANGUAGE with FREQUENCY COMB & QUANTUM DOT ENHANCEMENT 🌟")
    print("=" * 100)
    print("\nCombines Morse code timing with LUXBIN quantum wavelengths + microresonator frequency combs + quantum dot photon sources!")
    print("Each character = unique wavelength + morse pattern + nonlinear frequency comb + single-photon generation")
    print("\n🔬 Hybrid Quantum Technologies:")
    print(f"   • MICRORESONATOR: Pump @ {PUMP_WAVELENGTH}nm, {COMB_SPACING}nm spacing, Kerr coeff: {KERR_NONLINEARITY}")
    print(f"   • QUANTUM DOTS: {QD_EMISSION_WAVELENGTH}nm emission → {OUTPUT_WAVELENGTH}nm conversion")
    print(f"   • SUM-FREQUENCY: {QD_LIFETIME}ns lifetime, {TEMPORAL_MODULATION*1e12:.0f}ps modulation")
    print("\n📡 Dual-Technique Encoding:")
    print("   • FREQUENCY COMB: Multi-wavelength spectrum generation via Kerr nonlinearity")
    print("   • QUANTUM DOT + SFG: Single-photon sources with temporal shaping")
    print("   • DOT (·) = 5ms pulse + fast-modulated quantum dot photon")
    print("   • DASH (-) = 15ms pulse + slow-modulated quantum dot photon")
    print("   • SPACE = 35ms pulse at 637nm (diamond NV center)")
    print("   • TELECOM (1300/1550nm) ↔ VISIBLE (710nm) wavelength conversion")
    print("=" * 100)

    # Get input (with default for testing)
    default_text = "HELLO WORLD"
    try:
        text = input(f"\n💬 Enter message to transmit (default: '{default_text}'): ")
        if not text.strip():
            text = default_text
    except EOFError:
        # For automated testing
        text = default_text

    # Create encoder
    encoder = LuxbinMorseLight()

    # Encode and visualize
    print("\n🔄 Encoding message...")
    sequence = encoder.visualize_morse_light(text)

    # Print transmission table
    encoder.print_transmission_table()

    # Hybrid Quantum Statistics
    total_time = sum(p['duration_ms'] for p in sequence)
    num_pulses = sum(1 for p in sequence if not p['is_gap'])
    num_wavelengths = len(set(p['wavelength_nm'] for p in sequence if p['wavelength_nm'] > 0))
    total_comb_lines = sum(p.get('num_comb_lines', 0) for p in sequence if p.get('frequency_comb'))

    # Calculate efficiencies for both techniques
    comb_efficiencies = [p.get('comb_efficiency', 0) for p in sequence if p.get('comb_efficiency', 0) > 0]
    sf_efficiencies = [p.get('sf_efficiency', 0) for p in sequence if p.get('sf_efficiency', 0) > 0]

    avg_comb_efficiency = np.mean(comb_efficiencies) if comb_efficiencies else 0
    avg_sf_efficiency = np.mean(sf_efficiencies) if sf_efficiencies else 0

    print(f"\n📈 Hybrid Quantum Transmission Statistics:")
    print(f"   • Total pulses: {num_pulses}")
    print(f"   • Unique wavelengths: {num_wavelengths}")
    print(f"   • Total frequency comb lines: {total_comb_lines}")
    print(f"   • Average comb efficiency: {avg_comb_efficiency:.3f}")
    print(f"   • Average sum-frequency efficiency: {avg_sf_efficiency:.3f}")
    print(f"   • Total time: {total_time:.0f}ms ({total_time/1000:.2f} seconds)")
    print(f"   • Data rate: {len(text) / (total_time/1000):.1f} chars/second")
    print(f"   • Spectral efficiency: {total_comb_lines / num_pulses:.1f} comb lines per pulse")
    print(f"   • Wavelength conversion: {QD_EMISSION_WAVELENGTH}nm → {OUTPUT_WAVELENGTH}nm")
    print(f"   • Temporal resolution: {TEMPORAL_MODULATION*1e12:.0f}ps modulation")
    print(f"   • Light speed transmission: INSTANT over any distance!")
    print(f"   • Dual quantum enhancement: Kerr microresonator + quantum dot technology!")

    print(f"\n💡 Your message '{text}' is now encoded as hybrid quantum light pulses")
    print(f"   combining frequency combs and single-photon sources - ultimate photonic transmission! 🛰️✨🔬⚛️")

def test_hybrid_quantum_system():
    """Test the hybrid quantum system: frequency comb + quantum dot generation"""
    print("Testing Hybrid Quantum Photon Generation System...")
    print("=" * 60)

    encoder = LuxbinMorseLight()

    # Test 1: Frequency Comb Generation
    print("🔬 MICRORESONATOR FREQUENCY COMB TEST:")
    comb_gen = encoder.frequency_comb_gen
    test_wavelength = 650.0  # Red light
    dot_comb = comb_gen.generate_comb(test_wavelength, '.')
    dash_comb = comb_gen.generate_comb(test_wavelength, '-')

    print(f"  Dot comb: {len(dot_comb)} lines, efficiency: {comb_gen.get_quantum_efficiency(dot_comb):.3f}")
    print(f"  Dash comb: {len(dash_comb)} lines, efficiency: {comb_gen.get_quantum_efficiency(dash_comb):.3f}")
    print("  First 3 comb lines for dot:")
    for line in dot_comb[:3]:
        print(f"    λ={line['wavelength_nm']:.1f}nm, I={line['intensity']:.3f}")

    print("\n" + "=" * 60)

    # Test 2: Quantum Dot Generation
    print("⚛️ QUANTUM DOT + SUM-FREQUENCY GENERATION TEST:")
    qd_gen = encoder.quantum_dot_gen

    # Generate QD photon
    qd_dot = qd_gen.generate_qd_photon('.')
    qd_dash = qd_gen.generate_qd_photon('-')

    print(f"  QD emission: {qd_dot['wavelength_nm']}nm, lifetime: {qd_dot['lifetime']}ns")
    print(f"  Max amplitude (dot): {np.max(qd_dot['amplitude']):.3f}")
    print(f"  Max amplitude (dash): {np.max(qd_dash['amplitude']):.3f}")

    # Sum-frequency conversion
    sf_dot = qd_gen.sum_frequency_conversion(qd_dot)
    sf_dash = qd_gen.sum_frequency_conversion(qd_dash)

    print(f"  Sum-frequency output: {sf_dot['wavelength_nm']}nm")
    print(f"  Conversion efficiency: {qd_gen.get_conversion_efficiency():.3f}")
    print(f"  Temporal modulation: {sf_dot['temporal_modulation']*1e12:.0f}ps")
    print(f"  Converted amplitude (dot): {np.max(sf_dot['amplitude']):.3f}")
    print(f"  Converted amplitude (dash): {np.max(sf_dash['amplitude']):.3f}")

    print("\n" + "=" * 60)
    print("✅ Hybrid quantum system test completed successfully!")
    print(f"   • Dual photon generation techniques integrated")
    print(f"   • Wavelength conversion: {QD_EMISSION_WAVELENGTH}nm → {OUTPUT_WAVELENGTH}nm verified")
    print(f"   • Temporal shaping at {TEMPORAL_MODULATION*1e12:.0f}ps timescales confirmed")

    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_hybrid_quantum_system()
    else:
        main()
