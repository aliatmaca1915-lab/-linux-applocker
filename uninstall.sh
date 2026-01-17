#!/bin/bash
#
# Linux AppLocker - Uninstallation Script
# This script removes Linux AppLocker from the system
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    print_error "Please do not run this script as root. It will ask for sudo when needed."
    exit 1
fi

print_warning "This will completely remove Linux AppLocker from your system."
read -p "Are you sure you want to continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Uninstallation cancelled."
    exit 0
fi

print_info "Starting Linux AppLocker uninstallation..."

# Stop and disable systemd service
print_info "Stopping systemd service..."
systemctl --user stop linux-applocker.service 2>/dev/null || true
systemctl --user disable linux-applocker.service 2>/dev/null || true

# Remove systemd service file
print_info "Removing systemd service..."
rm -f ~/.config/systemd/user/linux-applocker.service
systemctl --user daemon-reload

# Remove application files
print_info "Removing application files..."
sudo rm -rf /opt/linux-applocker

# Remove launcher script
print_info "Removing launcher script..."
sudo rm -f /usr/local/bin/linux-applocker

# Remove desktop entry
print_info "Removing desktop entry..."
sudo rm -f /usr/share/applications/linux-applocker.desktop

# Remove icons
print_info "Removing icons..."
sudo rm -f /usr/share/icons/hicolor/scalable/apps/linux-applocker.svg
sudo gtk-update-icon-cache /usr/share/icons/hicolor/ 2>/dev/null || true

# Ask about user data
read -p "Do you want to remove user configuration and data? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Removing user data..."
    rm -rf ~/.config/linux-applocker
    rm -rf ~/.local/share/linux-applocker
else
    print_info "User data preserved at:"
    echo "  ~/.config/linux-applocker"
    echo "  ~/.local/share/linux-applocker"
fi

print_info "Uninstallation completed successfully!"
print_info "Thank you for using Linux AppLocker! 🔒"
