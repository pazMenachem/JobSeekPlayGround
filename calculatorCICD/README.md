# 🧮 calculatorCICD - CI/CD Learning Project

[![calculatorCICD CI Pipeline](https://github.com/pazMenachem/JobSeekPlayGround/actions/workflows/calculatorCICD-ci.yml/badge.svg)](https://github.com/pazMenachem/JobSeekPlayGround/actions/workflows/calculatorCICD-ci.yml)

A comprehensive **CI/CD learning project** built to master modern software development practices. This simple calculator serves as the foundation for exploring advanced DevOps concepts, automation, and professional development workflows.

## 🎯 Project Purpose

This project demonstrates **real-world CI/CD practices** through a simple Python calculator, covering everything from basic testing to advanced deployment strategies. Perfect for learning how professional software teams build, test, and deploy code.

## 🏗️ Architecture

```
calculatorCICD/
├── src/                     # Source code
│   ├── calc.py             # Calculator functions with type hints
│   ├── __main__.py         # CLI entry point  
│   └── __init__.py         # Package initialization
├── tests/                  # Test suite
│   └── test_calc.py        # Comprehensive test coverage
├── .github/workflows/      # CI/CD automation
│   └── calculatorCICD-ci.yml  # GitHub Actions pipeline
├── pyproject.toml          # Modern Python packaging
├── .flake8                 # Linting configuration
├── Dockerfile              # Container configuration
└── README.md               # This file
```

## 🚀 Features

- **🧮 Simple Calculator**: Add, subtract, multiply, divide operations
- **🔧 Type Safety**: Full type hints with mypy checking
- **🧪 Comprehensive Testing**: Complete test coverage with pytest
- **🎨 Code Quality**: Automated linting (flake8) and formatting (black)
- **🔒 Security Scanning**: Vulnerability detection with bandit and safety
- **📦 Containerization**: Docker support for consistent environments
- **⚡ CI/CD Pipeline**: Automated testing, quality checks, and deployment
- **📊 Reporting**: Test results, coverage reports, and build artifacts

## 🗺️ Learning Stages

### **Stage 1: Foundation & Code Quality**
**Goal**: Establish professional code quality standards
- Add type hints and comprehensive documentation
- Set up development tools (pytest, flake8, black, mypy)
- Create local quality automation scripts
- Implement proper test coverage and exclusions

### **Stage 2: Basic CI Pipeline**
**Goal**: Automate quality checks on every code change
- Create GitHub Actions workflow
- Set up path-specific triggers for monorepo structure
- Implement multi-Python version testing
- Add automated linting, formatting, and type checking

### **Stage 3: Advanced CI Features**
**Goal**: Professional-grade pipeline with comprehensive reporting
- Build artifacts for test results and coverage reports
- Security scanning with bandit and safety
- Parallel job execution for faster builds
- Job dependencies and conditional execution

### **Stage 4: Docker Integration**
**Goal**: Containerize application for consistent deployment
- Multi-stage Docker builds for optimization
- Docker builds integrated into CI pipeline
- Container security scanning
- Image optimization and layer caching

### **Stage 5: CD (Continuous Deployment)**
**Goal**: Automate releases and deployments
- Automated semantic versioning and tagging
- Release automation with changelog generation
- Package publishing to PyPI
- Docker image publishing to registries

### **Stage 6: Monitoring & Observability**
**Goal**: Monitor and maintain the CI/CD pipeline
- Build status badges and notifications
- Performance monitoring and benchmarks
- Dependency update automation (Dependabot)
- Slack/email notifications for failures

### **Stage 7: Advanced Deployment Patterns**
**Goal**: Enterprise-grade deployment strategies
- Blue/Green deployments
- Feature flags and environment promotion
- Rollback strategies and disaster recovery
- Infrastructure as Code

### **Stage 8: Enterprise Features**
**Goal**: Large-scale enterprise CI/CD practices
- Multi-environment pipelines (dev/staging/prod)
- Approval workflows for production deployments
- Compliance reporting and audit trails
- Integration with external tools

## 🛠️ Local Development

### Prerequisites
- Python 3.10+ 
- Git
- Docker (for containerization stages)

### Setup
```bash
# Clone the repository
git clone https://github.com/pazMenachem/JobSeekPlayGround.git
cd JobSeekPlayGround/calculatorCICD

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Development Workflow
```bash
# Run the calculator
python src/__main__.py

# Run all quality checks (mimics CI pipeline)
pytest                              # Run tests with coverage
flake8 src tests                    # Linting
black --check src tests             # Format checking  
mypy src --ignore-missing-imports   # Type checking

# Auto-format code
black src tests
```

## 🧪 Testing

```bash
# Run tests with coverage
pytest -v

# Generate HTML coverage report
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

## 🔒 Security

This project includes automated security scanning:
- **Safety**: Scans dependencies for known vulnerabilities
- **Bandit**: Static analysis for security anti-patterns
- **Regular Updates**: Dependabot keeps dependencies current

## 📊 CI/CD Pipeline

The GitHub Actions pipeline runs on every push to `main` and includes:

1. **🧪 Testing**: Multi-version Python testing (3.11, 3.12)
2. **🔍 Quality Checks**: Linting, formatting, type checking
3. **🔒 Security Scanning**: Vulnerability and code analysis
4. **📦 Artifacts**: Test results, coverage reports, security reports
5. **📋 Reporting**: Build summaries and status updates

**Pipeline Triggers**:
- Push to `main` branch (only for calculatorCICD folder changes)
- Manual workflow dispatch
- Pull requests targeting `main`