# GAPP

> GAPP IS NO LONGER MAINTAINED - PLEASE FEEL FREE TO FORK THIS APP AND TAKE IT OVER *

GPRO Setup and Strategy APP

## 🔔 Important Notice: Data Location Change

**GAPP now uses standard OS locations for storing data:**
- **Linux/macOS**: `~/.local/share/gapp/` and `~/.config/gapp/`
- **Windows**: `%APPDATA%\GAPP\`

**Existing users:** See [MIGRATION.md](MIGRATION.md) for migration instructions.

---

## Building a Distributable Executable

Want to share GAPP with users who don't have Python installed? See **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete instructions.

**Quick Start:**
- Linux/macOS: `./build.sh`
- Windows: `build.bat`

The standalone executable will be created in the `dist/` folder.

---

## Features

GAPP will let you calculate the optimal setup for your in each session, with differing weather conditions.
It also provides a strategy calculator, as well as a wear predictor, meaning you'll never get caught out again!

To get the latest version, simply head to the releases page and download GAPP.exe. When you run it, enter your GPRO credentials and hit calculate!
I recommend you set up a limited access login for any third party tool you use for GPRO! Look at your GPRO account settings for more information.

Current features:
* Setup Calculator - calculate the optimal setup for your car for every session
* Strategy Calculator - know which strategy is fastest for your car, and how best to achieve this strategy
* Wear Calculator - predictable car wear means you know whether or not your parts can last a race, no more money wasted
* PHA Calculator - know what effect changes to your car will have, making it easier to match track PHA

Planned changes:
* Integrate clear track risk into strategy calculator
* Account for tyre "wobble" and wear in the strategy calculator
* Automate data collection for long term analysis
