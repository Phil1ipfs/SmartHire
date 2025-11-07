#!/bin/bash
# SmartHire Environment Setup Script
# This script helps you create the .env file with proper configuration

echo "================================================"
echo "   SmartHire Environment Setup"
echo "================================================"
echo ""

# Check if .env already exists
if [ -f .env ]; then
    read -p ".env file already exists. Overwrite? (y/n): " overwrite
    if [ "$overwrite" != "y" ]; then
        echo "Setup cancelled."
        exit 0
    fi
fi

echo "Creating .env file..."
echo ""

# Generate SECRET_KEY
echo "Generating SECRET_KEY..."
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# Ask for DATABASE_URL
echo ""
echo "Enter your Render PostgreSQL Database URL:"
echo "(Format: postgresql://user:password@host:5432/database)"
read -p "DATABASE_URL: " DATABASE_URL

# Ask for email credentials
echo ""
echo "Enter your Gmail address for sending emails:"
read -p "MAIL_USERNAME: " MAIL_USERNAME

echo ""
echo "Enter your Gmail App Password:"
echo "(Generate at: https://myaccount.google.com/apppasswords)"
read -s -p "MAIL_PASSWORD: " MAIL_PASSWORD
echo ""

# Create .env file
cat > .env << EOF
# SmartHire Environment Variables
# Generated on: $(date)

# Application Secret Key
SECRET_KEY=$SECRET_KEY

# Database Connection (Render PostgreSQL)
DATABASE_URL=$DATABASE_URL

# Email Configuration (Gmail)
MAIL_USERNAME=$MAIL_USERNAME
MAIL_PASSWORD=$MAIL_PASSWORD

# Flask Environment
FLASK_ENV=production
EOF

echo ""
echo "================================================"
echo "✅ .env file created successfully!"
echo "================================================"
echo ""
echo "Environment variables configured:"
echo "  ✓ SECRET_KEY (generated)"
echo "  ✓ DATABASE_URL"
echo "  ✓ MAIL_USERNAME"
echo "  ✓ MAIL_PASSWORD"
echo ""
echo "Next steps:"
echo "1. Review .env file: cat .env"
echo "2. Test database connection"
echo "3. Continue with deployment steps"
echo ""
