# GitHub Actions Workflows for NervaPy

This document describes the GitHub Actions workflows set up for the NervaPy project.

## Workflows Overview

### 1. Test Workflow (`test.yml`)
**Triggers:** Push/PR to main branches, daily at 6 AM UTC, manual dispatch

**Purpose:** Comprehensive testing across multiple Python versions and operating systems

**Matrix Testing:**
- **OS:** Ubuntu, Windows, macOS 
- **Python:** 3.8, 3.9, 3.10, 3.11, 3.12
- **Exclusions:** Some combinations excluded to optimize CI resources

**Test Steps:**
1. **Environment Setup**: Python installation, dependency caching
2. **System Dependencies**: Build tools for Linux
3. **Python Dependencies**: Install requirements and NervaPy in development mode
4. **Import Tests**: Verify basic and full imports work
5. **Functionality Tests**: Test core assembly generation features
6. **Unit Tests**: Run pytest on the test suite
7. **Architecture Tests**: x86_64 encoding tests (Linux/macOS only)
8. **CLI Tests**: Verify command-line interface works

**Lint Job:**
- **flake8**: Syntax and style checking
- **Import Structure**: Verify all modules can be imported

### 2. Code Quality Workflow (`code-quality.yml`)
**Triggers:** Push/PR to main branches

**Purpose:** Automated code quality analysis and security scanning

**Jobs:**
1. **Security Scan**
   - **bandit**: Security vulnerability scanning
   - **safety**: Dependency vulnerability checking

2. **Type Checking**
   - **mypy**: Static type analysis

3. **Code Formatting**
   - **black**: Code formatting verification
   - **isort**: Import sorting verification

4. **Complexity Analysis**
   - **radon**: Cyclomatic complexity and maintainability index
   - **xenon**: Complexity threshold enforcement

### 3. Release Workflow (`release.yml`)
**Triggers:** GitHub releases, manual dispatch

**Purpose:** Automated building and publishing of releases

**Jobs:**
1. **Build Wheels**
   - Cross-platform wheel building (Ubuntu, Windows, macOS)
   - Source distribution building (Linux only)
   - Built package testing

2. **Publish**
   - Automatic PyPI publishing for releases
   - Artifact collection from all build jobs

## Configuration Files

### `pytest.ini`
Pytest configuration for consistent test execution:
- Test discovery patterns
- Verbose output with short tracebacks
- Warning filters
- Test markers for categorization

### Badge Integration
README.md includes status badges for:
- Test workflow status
- Code quality checks
- Release build status

## Benefits

1. **Quality Assurance**: Every commit is tested across multiple environments
2. **Early Detection**: Issues caught before they reach main branches
3. **Cross-Platform**: Ensures compatibility across OS and Python versions
4. **Security**: Automated vulnerability scanning
5. **Automation**: Reduces manual testing and release overhead
6. **Documentation**: Clear test results and code quality metrics

## Usage

### For Contributors
- All tests run automatically on push/PR
- Check workflow status before merging
- Address any failing tests or quality issues

### For Maintainers
- Monitor daily test runs for environment changes
- Review security and quality reports
- Use manual workflow dispatch for testing
- Releases trigger automatic PyPI publishing

### Local Testing
Before pushing, run tests locally:
```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run tests
pytest tests/ -v

# Check imports
python -c "from nervapy import *; from nervapy.x86_64 import *"
```

## Maintenance

### Updating Dependencies
- Update Python versions in matrix as needed
- Keep action versions current (@v4, etc.)
- Monitor for deprecated GitHub Actions features

### Adding Tests
- Follow existing test patterns
- Use appropriate pytest markers
- Consider cross-platform compatibility

### Security
- Regularly review security scan results
- Update vulnerable dependencies promptly
- Monitor GitHub security advisories