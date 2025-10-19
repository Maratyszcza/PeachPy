# NervaPy

[![Test NervaPy](https://github.com/username/NervaPy/actions/workflows/test.yml/badge.svg)](https://github.com/username/NervaPy/actions/workflows/test.yml)
[![Code Quality](https://github.com/username/NervaPy/actions/workflows/code-quality.yml/badge.svg)](https://github.com/username/NervaPy/actions/workflows/code-quality.yml)
[![Build and Release](https://github.com/username/NervaPy/actions/workflows/release.yml/badge.svg)](https://github.com/username/NervaPy/actions/workflows/release.yml)

**An experimental Python framework for exploring advanced program synthesis and transformation techniques**

NervaPy is an experimental Python framework based on [PeachPy](https://github.com/Maratyszcza/PeachPy) that explores advanced program synthesis and transformation techniques. It provides a foundation for research into automated code generation, optimization, and program analysis.

## About

This project builds upon the solid foundation provided by PeachPy's assembly generation capabilities to explore:

- Advanced program synthesis techniques
- Code transformation and optimization strategies
- Meta-programming approaches for high-performance code generation
- Research into automated assembly kernel generation

## Origin

NervaPy is based on PeachPy by Marat Dukhan. PeachPy was originally designed as a Python framework for writing high-performance assembly kernels with features like:

- Universal assembly syntax for multiple platforms
- Automatic register allocation
- Cross-platform ABI compatibility
- Support for x86-64 instructions up to AVX-512

## Installation

```bash
git clone <repository-url>
cd NervaPy
python setup.py develop
```

## Usage

The basic API remains similar to PeachPy while providing additional experimental features:

```python
from nervapy import *
from nervapy.x86_64 import *

# Example usage similar to original PeachPy
x = Argument(ptr(const_float_), name="x")
y = Argument(ptr(const_float_))

with Function("DotProduct", (x, y), float_,
              target=uarch.default + isa.sse4_2):
    
    reg_x, reg_y = GeneralPurposeRegister64(), GeneralPurposeRegister64()
    
    LOAD.ARGUMENT(reg_x, x)
    LOAD.ARGUMENT(reg_y, y)
    
    xmm_x = XMMRegister()
    MOVAPS(xmm_x, [reg_x])
    MOVAPS(xmm2, [reg_y])
    
    DPPS(xmm_x, xmm2, 0xF1)
    
    RETURN(xmm_x)
```

## License

This project maintains the same Simplified BSD License as the original PeachPy.

## Development

### Running Tests Locally

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run all tests
pytest tests/ -v

# Run specific test modules
pytest tests/test_literal.py -v
pytest tests/x86_64/encoding/ -v
```

### Continuous Integration

This project uses GitHub Actions for continuous integration:

- **Test Suite**: Runs on Python 3.8-3.12 across Ubuntu, Windows, and macOS
- **Code Quality**: Security scanning, type checking, formatting, and complexity analysis
- **Release Builds**: Automated wheel building and PyPI publishing

All tests run automatically on every push and pull request to ensure code quality and compatibility.

## Acknowledgements

This work is based on PeachPy by Marat Dukhan and the research conducted at the HPC Garage lab in the Georgia Institute of Technology.