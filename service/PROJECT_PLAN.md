# Windows Service Learning Project - Progress & Plan

## 📋 Project Overview

**Goal**: Learn how to create a Windows service in Python that runs applications in the background.

**Final Purpose**: Create a service that starts a CLI application. The service will be used as a component in other projects.

**Learning Approach**: Step-by-step with theory, explanation, and implementation in small increments.

---

## ✅ Completed Phases

### **Phase 1: Environment Setup** ✅ COMPLETE

**What was done:**
1. Created project structure:
   - `logs/` directory for service logs
   - `requirements.txt` with `pywin32==306`
   - `README.md` with project documentation
   
2. Created Python virtual environment:
   ```cmd
   python -m venv venv
   ```

3. Installed dependencies:
   ```cmd
   venv\Scripts\pip.exe install -r requirements.txt
   venv\Scripts\python.exe venv\Scripts\pywin32_postinstall.py -install
   ```

**Important**: Always use `venv\Scripts\python.exe` for service operations!

---

### **Phase 2: Simple CLI Application** ✅ COMPLETE

**Created**: `hello_app.py`

**Features**:
- Accepts optional command-line arguments
- Prints timestamped messages
- Logs to `logs/hello_app.log`
- Uses Google-style docstrings
- Type hints on function parameters
- Flake8 compliant

**Testing**:
```cmd
venv\Scripts\python.exe hello_app.py
venv\Scripts\python.exe hello_app.py "Custom message"
```

**Results**: ✅ Works correctly, creates log file with timestamps

---

## 🎓 Theory Covered

### **1. Service Fundamentals**
- What is a service vs regular application
- Service lifecycle: Install → Start → Run → Stop → Uninstall
- Service characteristics: background execution, no UI, persistent
- Common use cases: monitoring, network services, scheduled tasks

### **2. Windows Service Architecture**
- **Service Control Manager (SCM)**: Windows component that manages services
- **Service States**: STOPPED, START_PENDING, RUNNING, STOP_PENDING, PAUSED
- **Service Accounts**: Local System, Network Service, Custom accounts
- **Session 0 Isolation**: Services can't display UI to users (security)
- **Signal Handling**: Services must respond to STOP, PAUSE, CONTINUE signals within ~30 seconds
- **Checkpoints**: Progress indicators for long start/stop operations

### **3. Service Recovery**
- Windows can automatically restart crashed services
- Recovery actions configurable (restart, run program, reboot)
- Best practice: Handle errors gracefully in code, use recovery as safety net
- For API timeouts: Implement retry logic with exponential backoff

### **4. Implementation Approach**
**Chosen**: `pywin32` (win32serviceutil)

**Why**:
- ✅ Native Windows integration
- ✅ Full control over service behavior
- ✅ Professional, production-ready
- ✅ Educational value - learn how services actually work

**Alternatives considered**:
- NSSM (simpler but less control)
- Task Scheduler (not a true service)
- pythonw.exe with startup (no service management)

### **5. Process vs Thread Architecture**
**Service Structure**:
```
Service Process (my_service.py)
├── Main Service Thread (handles Windows SCM signals)
└── Worker Thread (executes business logic)
    └── Spawns Subprocess → hello_app.py runs in NEW PROCESS
                              with its own main thread
```

**Key Point**: Worker thread and hello_app.py are SEPARATE PROCESSES with separate memory spaces.

### **6. Character Encoding Deep Dive**
- **UTF-8**: Variable-width (1-4 bytes per character), supports all languages
  - 1 byte: ASCII (A-Z, 0-9)
  - 2 bytes: Accented Latin, Greek, Hebrew, Arabic
  - 3 bytes: Chinese, Japanese, Korean
  - 4 bytes: Emojis, rare characters
- **Always use `encoding='utf-8'`** for portability and Unicode support
- Without explicit encoding, get platform-dependent behavior (Windows: cp1252, Linux: utf-8)

---

## 🚀 Current Status: Ready for Phase 3

**Next Step**: Create the Windows Service implementation

---

## 📝 Phase 3: Create Basic Windows Service (NEXT)

### **What We'll Create**: `my_service.py`

### **Service Components to Implement**:

1. **Service Class** (inherits from `win32serviceutil.ServiceFramework`)
   - Service name, display name, description
   - Service configuration

2. **SvcDoRun() Method** - Main entry point
   - Called when service starts
   - Logs startup
   - Starts worker thread
   - Waits for stop signal

3. **SvcStop() Method** - Stop signal handler
   - Called when Windows sends STOP signal
   - Sets stop flag
   - Reports SERVICE_STOP_PENDING to SCM
   - Waits for worker thread to exit cleanly

4. **Worker Thread** - Business logic
   - Runs in background loop
   - Checks stop flag regularly
   - Executes hello_app.py periodically
   - Handles errors without crashing

5. **Logging System**
   - Logs to file (no console output - services have no console)
   - Timestamps all operations
   - Records: start, stop, execution, errors
   - Location: `logs/service.log`

6. **Entry Point** - Command-line interface
   - `python my_service.py install` - Register with Windows
   - `python my_service.py start` - Start the service
   - `python my_service.py stop` - Stop the service
   - `python my_service.py remove` - Uninstall from Windows
   - `python my_service.py debug` - Run in console for testing

### **Key Implementation Details**:

#### **Signal Handling Pattern**:
```python
def SvcDoRun(self):
    while not self.stop_flag.is_set():
        # Do work
        if self.stop_flag.wait(timeout=60):  # Check flag every 60s
            break
    # Clean exit
```

#### **Graceful Shutdown**:
- Main thread receives STOP signal
- Sets `stop_flag` (threading.Event)
- Worker thread checks flag and exits loop
- Service reports SERVICE_STOPPED to SCM

#### **Error Handling**:
- Try/except around subprocess calls
- Log errors, don't crash
- Continue running even if one execution fails

---

## 📝 Phase 4: Add CLI Execution (AFTER PHASE 3)

### **What We'll Add**:
1. Execute `hello_app.py` using `subprocess.run()`
2. Capture output and log it
3. Handle execution errors
4. Configure execution interval (e.g., every 60 seconds)

---

## 📝 Phase 5: Signal Handling & Polish (AFTER PHASE 4)

### **What We'll Add**:
1. Proper SERVICE_STOP_PENDING with checkpoints
2. Optional PAUSE/CONTINUE support
3. Enhanced error recovery
4. Configuration file support

---

## 📝 Phase 6: Final Review & Documentation (AFTER PHASE 5)

### **What We'll Do**:
1. Test all scenarios (start, stop, crash recovery)
2. Review all components
3. Discuss reusability in other projects
4. Create installation batch file
5. Document lessons learned

---

## 🔧 Technical Requirements

### **Environment**:
- Python 3.7+ (currently using 3.12)
- Windows OS
- Administrator privileges (required for service installation)

### **Dependencies**:
- `pywin32==306`

### **Important Paths**:
- **Python executable**: `venv\Scripts\python.exe` (MUST use venv's Python!)
- **Service script**: `my_service.py` (to be created)
- **CLI app**: `hello_app.py` (completed)
- **Logs directory**: `logs/`

---

## 📚 Important Concepts to Remember

### **Service Control Manager (SCM)**:
- Must respond to SCM within 30 seconds or service is considered hung
- Service must report state changes (STOPPED, RUNNING, etc.)
- Communication is via Windows API (handled by pywin32)

### **Service Accounts & Permissions**:
- **Local System**: Full privileges, no network identity
- **Network Service**: Reduced privileges, has network identity
- **Custom Account**: Specific user, needs "Log on as a service" right

**For our service**:
- Writing to `C:\ProgramData\` → Local System account OK
- Accessing network shares → Need Network Service or custom account

### **Why Services Can't Show UI**:
- Session 0 isolation (security feature since Windows Vista)
- Services run in Session 0
- User apps run in Session 1+
- Services can't interact with user desktop

**Solutions for user notification**:
- Write to file that user app monitors
- Use named pipes/sockets between service and user app
- Send external notifications (email, Telegram, etc.)
- Write to Windows Event Log

### **Crash Prevention**:
- Services run unattended - crashes might go unnoticed
- Always use try/except around risky operations
- Log errors instead of crashing
- Use Windows recovery options as last resort

---

## 🎯 Next Session Checklist

When continuing on another PC:

1. ✅ Ensure same environment:
   ```cmd
   cd C:\path\to\service
   python -m venv venv
   venv\Scripts\pip.exe install -r requirements.txt
   venv\Scripts\python.exe venv\Scripts\pywin32_postinstall.py -install
   ```

2. ✅ Verify hello_app.py works:
   ```cmd
   venv\Scripts\python.exe hello_app.py
   ```

3. ✅ Ready to create `my_service.py` (Phase 3)

4. ✅ Remember: User wants step-by-step approach - ASK BEFORE PROCEEDING to each step

---

## 🤔 Questions Discussed & Answered

### **Q1: What happens if service crashes?**
- Service stops immediately
- Error logged to Windows Event Log
- Service stays stopped unless recovery configured
- Can configure automatic restart with delays

### **Q2: How does signal handling work?**
- Windows sends control codes (STOP, PAUSE, CONTINUE)
- Service must check flags regularly in main loop
- Must respond within ~30 seconds
- Override `SvcStop()`, `SvcPause()`, `SvcContinue()` methods

### **Q3: What else to know about Windows service architecture?**
- Service states and checkpoints
- Service entry point registration with SCM
- Service account context and permissions
- Session 0 isolation for security
- Service dependencies

### **Q4: What is a .bat file?**
- Batch file for Windows command interpreter (cmd.exe)
- Contains sequence of commands to execute
- Used for convenience (install service with double-click)
- Alternative: PowerShell scripts (.ps1)

### **Q5: How to use venv with services?**
- Use venv's Python when installing: `venv\Scripts\python.exe my_service.py install`
- Service will use venv's Python and installed packages
- Alternative: PyInstaller (standalone .exe)

### **Q6: Worker thread vs main thread in called app?**
- Service has worker thread (runs in service process)
- Worker calls `subprocess.run()` which creates NEW PROCESS
- hello_app.py runs in separate process with own main thread
- They don't share memory - completely isolated

### **Q7: What does encoding='utf-8' do?**
- Tells Python how to convert between bytes and Unicode characters
- UTF-8 is variable-width: 1-4 bytes per character
- Supports all languages, emojis, special characters
- Without it, get platform-dependent default (Windows: cp1252)
- Always use `encoding='utf-8'` for portability

---

## 📝 Code Style Guidelines (User Requirements)

- ✅ Flake8 compliant
- ✅ Type hints on function parameters only (not variables)
- ✅ Google-style docstrings for documentation
- ✅ Use `encoding='utf-8'` for all file operations

---

## 🗂️ Current Project Structure

```
service/
├── logs/
│   └── hello_app.log        # CLI app logs
├── venv/                     # Virtual environment
│   ├── Scripts/
│   │   ├── python.exe       # Use this for all operations!
│   │   └── pip.exe
│   └── Lib/
│       └── site-packages/
│           └── win32/       # pywin32 installed here
├── hello_app.py             # ✅ COMPLETE - CLI application
├── my_service.py            # ⏳ NEXT - Service implementation
├── requirements.txt         # ✅ COMPLETE
├── README.md                # ✅ COMPLETE
└── PROJECT_PLAN.md          # ✅ THIS FILE
```

---

## 🎓 Learning Progress

**Understanding Level**: GOOD ✅

User has demonstrated understanding of:
- ✅ Service vs regular application differences
- ✅ Service recovery strategies
- ✅ Basic service account concepts
- ⚠️ Signal handling (will solidify during implementation)
- ⚠️ Session 0 isolation (creative solutions, needs technical details)
- ✅ Character encoding (UTF-8 variable-width)
- ✅ Process vs thread architecture

**Ready to proceed**: YES ✅

---

## 📞 Contact Points for Questions

When resuming work, review:
1. This plan file (PROJECT_PLAN.md)
2. hello_app.py (completed CLI app)
3. Theory sections above
4. Remember: Step-by-step approach, ask before each phase

---

**Last Updated**: 2025-11-05 22:38 (local time)
**Current Phase**: Beginning Phase 3 (Create Windows Service)
**Next Action**: Create `my_service.py` with service implementation

