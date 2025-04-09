#!/bin/bash
# Setup script to install patched versions of dependencies for Python 3 compatibility

# Exit on error
set -e

echo "Installing patched versions of dependencies for Python 3 compatibility..."

# Install patched PyContracts
echo "Installing patched PyContracts..."
pip uninstall -y PyContracts || true
pip install -e vendor/pycontracts

# Install patched compmake
echo "Installing patched compmake..."
pip uninstall -y compmake || true
pip install -e vendor/compmake

echo "Patched dependencies installed successfully!"