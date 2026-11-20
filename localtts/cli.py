"""Interactive launcher (questionary prompts). Any option left out is prompted for."""
from pathlib import Path
from typing import Optional

import questionary
import typer

from .core import DEFAULT_INPUT, OUTPUT_DIR, read_text, write_wav
from .engines import ENGINES

app = typer.Typer(add_completion=False, help="Local TTS launcher: pick engine, voice and speed.")

CUSTOM_VOICE = "Custom WAV path (voice cloning)..."


def ask(question: questionary.Question):
    """Run a questionary prompt; exit cleanly on Ctrl+C."""
    answer = question.ask()
    if answer is None:
        raise typer.Abort()
    return answer


def valid_speed(value: str) -> bool | str:
    try:
        return 0.25 <= float(value) <= 4.0 or "Enter a number between 0.25 and 4.0"
    except ValueError:
        return "Enter a number between 0.25 and 4.0"


def valid_file(value: str) -> bool | str:
    return Path(value.strip().strip('"')).is_file() or "File not found"


@app.command()
def main(
    input_file: Optional[Path] = typer.Argument(None, help=f"Text file to read (default: {DEFAULT_INPUT})"),
    engine: Optional[str] = typer.Option(None, "--engine", "-e", help="kitten | pocket | kokoro"),
    voice: Optional[str] = typer.Option(None, "--voice", "-v", help="Voice name (pocket: name or WAV path)"),
    speed: Optional[float] = typer.Option(None, "--speed", "-s", help="Speed (kitten, kokoro)"),
    output_file: Optional[Path] = typer.Option(None, "--output", "-o", help="Output WAV path"),
    list_voices: bool = typer.Option(False, "--list-voices", help="Print engines and voices, then exit"),
):
    if list_voices:
        for e in ENGINES.values():
            typer.echo(f"{e.name}: {', '.join(e.voices)}")
        raise typer.Exit()

    if engine is None:
        engine = ask(questionary.select(
            "Select a TTS engine:",
            choices=[questionary.Choice(f"{e.name:7s} {e.label}", value=e.name) for e in ENGINES.values()],
        ))
    if engine not in ENGINES:
        typer.echo(f"Unknown engine '{engine}'. Choose from: {', '.join(ENGINES)}", err=True)
        raise typer.Exit(1)
    eng = ENGINES[engine]

    if voice is None:
        choices = list(eng.voices) + ([CUSTOM_VOICE] if eng.accepts_custom_voice else [])
        voice = ask(questionary.select(f"Select a voice for {eng.name}:", choices=choices, default=eng.default_voice))
        if voice == CUSTOM_VOICE:
            voice = ask(questionary.path("Path to reference WAV:", validate=valid_file)).strip().strip('"')

    if speed is None:
        speed = float(ask(questionary.text("Speed:", default="1.0", validate=valid_speed))) if eng.supports_speed else 1.0
    elif not eng.supports_speed:
        typer.echo(f"Note: {eng.name} does not support --speed; ignoring.")
        speed = 1.0

    if input_file is None:
        input_file = Path(ask(questionary.path("Input text file:", default=str(DEFAULT_INPUT), validate=valid_file)).strip().strip('"'))
    if output_file is None:
        output_file = Path(ask(questionary.text("Output WAV file:", default=str(OUTPUT_DIR / eng.default_output))))

    try:
        text = read_text(input_file)
    except (OSError, ValueError) as err:
        typer.echo(f"Error: {err}", err=True)
        raise typer.Exit(1)

    typer.echo(f"Generating with {eng.name} (voice={voice}, speed={speed})...")
    audio, sample_rate = eng.synthesize(text, voice, speed)
    seconds = write_wav(output_file, audio, sample_rate)
    typer.echo(f"Generated: {output_file} ({seconds:.1f}s @ {sample_rate} Hz)")
