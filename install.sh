#!/bin/bash
#
# Linux AppLocker - Installation Script
# This script installs Linux AppLocker on Linux Mint and compatible systems
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

print_info "Starting Linux AppLocker installation..."

# Check Python version
print_info "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
print_info "Python version: $PYTHON_VERSION"

# Check for required system packages
print_info "Checking system dependencies..."
MISSING_PACKAGES=()

# Check for GTK4
if ! dpkg -l | grep -q libgtk-4-1; then
    MISSING_PACKAGES+=("libgtk-4-1")
fi

# Check for LibAdwaita
if ! dpkg -l | grep -q libadwaita-1-0; then
    MISSING_PACKAGES+=("libadwaita-1-0")
fi

# Check for GObject introspection
if ! dpkg -l | grep -q gir1.2-gtk-4.0; then
    MISSING_PACKAGES+=("gir1.2-gtk-4.0")
fi

if ! dpkg -l | grep -q gir1.2-adw-1; then
    MISSING_PACKAGES+=("gir1.2-adw-1")
fi

# Install missing packages if any
if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    print_warning "Missing packages: ${MISSING_PACKAGES[*]}"
    print_info "Installing missing packages..."
    sudo apt-get update
    sudo apt-get install -y "${MISSING_PACKAGES[@]}"
fi

# Create installation directory
print_info "Creating installation directory..."
sudo mkdir -p /opt/linux-applocker
sudo mkdir -p /opt/linux-applocker/assets
sudo mkdir -p /opt/linux-applocker/systemd

# Install Python dependencies
print_info "Installing Python dependencies..."
python3 -m pip install --user -r requirements.txt

# Copy application files
print_info "Copying application files..."
sudo cp -r src /opt/linux-applocker/
sudo cp -r assets /opt/linux-applocker/
sudo cp requirements.txt /opt/linux-applocker/

# Create wrapper script
print_info "Creating launcher script..."
sudo tee /usr/local/bin/linux-applocker > /dev/null << 'EOF'
#!/bin/bash
cd /opt/linux-applocker
python3 -m src.main "$@"
EOF
sudo chmod +x /usr/local/bin/linux-applocker

# Install desktop entry
print_info "Installing desktop entry..."
sudo cp linux-applocker.desktop /usr/share/applications/

# Copy icons
print_info "Installing icons..."
sudo mkdir -p /usr/share/icons/hicolor/scalable/apps
if [ -f "assets/icons/app-icon.svg" ]; then
    sudo cp assets/icons/app-icon.svg /usr/share/icons/hicolor/scalable/apps/linux-applocker.svg
fi
sudo gtk-update-icon-cache /usr/share/icons/hicolor/ 2>/dev/null || true

# Install systemd user service
print_info "Installing systemd service..."
mkdir -p ~/.config/systemd/user
cp systemd/linux-applocker.service ~/.config/systemd/user/
systemctl --user daemon-reload

# Create config directory
print_info "Creating configuration directory..."
mkdir -p ~/.config/linux-applocker
mkdir -p ~/.local/share/linux-applocker

# Set permissions
sudo chown -R root:root /opt/linux-applocker
sudo chmod -R 755 /opt/linux-applocker

print_info "Installation completed successfully!"
echo ""
print_info "To start Linux AppLocker:"
echo "  1. Run: linux-applocker"
echo "  2. Or search for 'Linux AppLocker' in your application menu"
echo ""
print_info "To enable autostart:"
echo "  systemctl --user enable linux-applocker.service"
echo "  systemctl --user start linux-applocker.service"
echo ""
print_info "Enjoy using Linux AppLocker! 🔒"
