---
name: "Environment Setup Guide"
tags: ["antigravity", "c:", "debian", "environment", "frontend", "gemini", "guide", "<YOUR_USERNAME>", "macos", "overview", "rules", "setup", "specialized", "system", "tools", "ubuntu", "users", "windows"]
tier: 2
risk: "medium"
estimated_tokens: 1630
tools_needed: ["docker", "git", "markdown", "sql", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.91
---
# Environment Setup Guide

> **Tier:** 1-2  
> **Tags:** `setup`, `environment`, `dev-tools`, `onboarding`, `configuration`  
> **When to use:** Setting up development environment, onboarding new developers, troubleshooting setup issues

---

## Overview

Comprehensive guide for setting up development environments across platforms (macOS, Linux, Windows). Covers essential tools (Node.js, Python, Docker), configuration, verification, and troubleshooting.

---

## Rules

**RULE-001: Platform-Specific Instructions**
Provide separate instructions for macOS, Linux, and Windows. Don't assume cross-platform compatibility. Test commands on target platform before documenting.

```bash
❌ Bad: Generic instructions
"Install Node.js from the website"

✅ Good: Platform-specific
# macOS
brew install node

# Ubuntu/Debian
sudo apt update && sudo apt install nodejs npm

# Windows
winget install OpenJS.NodeJS
# or download from nodejs.org
```

**RULE-002: Version Pinning**
Specify exact or minimum versions for critical dependencies. Use version managers (nvm, pyenv) to avoid conflicts. Document version requirements clearly.

```bash
❌ Bad: No version specified
npm install

✅ Good: Version requirements documented
# Node.js >= 18.0.0 required
node --version  # Should show v18.x or higher

# Use nvm to install specific version
nvm install 18
nvm use 18
```

**RULE-003: Verification Steps**
Include verification commands after each installation step. Confirm tools are accessible and working before proceeding.

```bash
# Install Node.js
brew install node

# Verify installation
node --version    # Should show v18.x.x or higher
npm --version     # Should show 9.x.x or higher

# Test basic functionality
node -e "console.log('Node.js works!')"
```

**RULE-004: Environment Variables**
Document required environment variables. Provide examples for different shells (.bashrc, .zshrc, PowerShell profile). Include instructions for permanent vs temporary variables.

```bash
❌ Bad: Unclear variable setup
"Set API_KEY environment variable"

✅ Good: Shell-specific instructions
# Bash/Zsh (add to ~/.bashrc or ~/.zshrc)
export API_KEY="your-key-here"
export DATABASE_URL="postgresql://localhost/mydb"

# PowerShell (add to $PROFILE)
$env:API_KEY = "your-key-here"
$env:DATABASE_URL = "postgresql://localhost/mydb"

# Verify
echo $API_KEY  # Bash/Zsh
echo $env:API_KEY  # PowerShell
```

**RULE-005: Dependency Installation Order**
Install dependencies in correct order. System packages first, then language runtimes, then project dependencies. Document why order matters.

```bash
# 1. System packages (required by later steps)
sudo apt install build-essential libssl-dev

# 2. Language runtime
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18

# 3. Project dependencies
npm install
```

**RULE-006: Troubleshooting Section**
Include common issues and solutions. Provide diagnostic commands. Link to detailed troubleshooting resources.

```markdown
## Common Issues

### Issue: "command not found: node"
**Cause:** Node.js not in PATH or not installed
**Solution:**
1. Verify installation: `which node` (Unix) or `where node` (Windows)
2. Restart terminal to reload PATH
3. Reinstall if necessary

### Issue: "EACCES: permission denied"
**Cause:** npm trying to write to system directories
**Solution:**
```bash
# Fix npm permissions (Unix)
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```
```

**RULE-007: Configuration Files**
Provide template configuration files (.env.example, config.example.json). Document all configuration options. Never commit secrets.

```bash
# Create .env.example (commit this)
API_KEY=your-api-key-here
DATABASE_URL=postgresql://localhost:5432/mydb
NODE_ENV=development

# Create .env from example (don't commit this)
cp .env.example .env
# Edit .env with actual values

# Add to .gitignore
echo ".env" >> .gitignore
```

**RULE-008: Docker Alternative**
Provide Docker setup as alternative to local installation. Include docker-compose.yml for complex setups. Document when to use Docker vs local.

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://db:5432/mydb
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_PASSWORD=password

# Start with Docker
docker-compose up -d

# Verify
docker-compose ps
```

---

## Quick Reference

### Essential Tools Checklist

- [ ] **Node.js** (v18+) - JavaScript runtime
- [ ] **npm/yarn** - Package manager
- [ ] **Git** (v2.30+) - Version control
- [ ] **Docker** (optional) - Containerization
- [ ] **Python** (v3.9+) - If needed
- [ ] **Code editor** (VS Code, etc.)

### Installation Commands

#### macOS (Homebrew)
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install tools
brew install node git python docker
```

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install tools
sudo apt install nodejs npm git python3 python3-pip docker.io

# Add user to docker group
sudo usermod -aG docker $USER
```

#### Windows (winget)
```powershell
# Install tools
winget install OpenJS.NodeJS
winget install Git.Git
winget install Python.Python.3.11
winget install Docker.DockerDesktop
```

### Verification Commands

```bash
# Check versions
node --version
npm --version
git --version
python --version
docker --version

# Test functionality
node -e "console.log('Node works')"
git --help
python -c "print('Python works')"
docker run hello-world
```

### Environment Variables

```bash
# View all environment variables
env  # Unix
Get-ChildItem Env:  # PowerShell

# Set temporary variable (current session only)
export VAR=value  # Bash/Zsh
$env:VAR = "value"  # PowerShell

# Set permanent variable
# Add to ~/.bashrc, ~/.zshrc, or $PROFILE
```

### Troubleshooting Checklist

- [ ] Restart terminal after installation
- [ ] Check PATH includes tool directories
- [ ] Verify no conflicting versions installed
- [ ] Check file permissions (Unix)
- [ ] Run as administrator if needed (Windows)
- [ ] Clear npm cache: `npm cache clean --force`
- [ ] Reinstall if all else fails

---

## Metadata

- **Related Skills:** [bash-linux.md], [powershell-windows.md], [docker-patterns.md]
- **Dependencies:** None
- **Version:** 1.0.0
- **Last Updated:** 2024-03-26
