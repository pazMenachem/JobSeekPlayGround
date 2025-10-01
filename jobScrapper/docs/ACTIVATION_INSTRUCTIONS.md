# Virtual Environment Activation Instructions

## 🚨 **IMPORTANT: You MUST use `source` command!**

The virtual environment activation **will NOT work** if you run the script with `./activate.sh`. You must **source** it instead.

## ✅ **Correct Way to Activate:**

```bash
source ./activate.sh
# OR
. ./activate.sh
```

## ❌ **Wrong Way (Won't Work):**

```bash
./activate.sh  # This won't work!
```

## 🔍 **Why This Happens:**

- **`./activate.sh`** runs the script in a **subshell** - environment changes are lost when the script exits
- **`source ./activate.sh`** runs the script in the **current shell** - environment changes persist

## 🎯 **Quick Test:**

After activation, check if it worked:

```bash
# Check if virtual environment is active
echo $VIRTUAL_ENV

# Check which Python is being used
which python

# You should see paths pointing to your venv directory
```

## 🔧 **If It Still Doesn't Work:**

1. **Try manual activation:**
   ```bash
   source venv/Scripts/activate
   ```

2. **Check your environment:**
   ```bash
   ./check_venv.sh
   ```

3. **Reinstall if needed:**
   ```bash
   python install.py
   ```

## 📝 **Summary:**

- Always use `source` or `.` before the script name
- Never use `./` to run activation scripts
- The `source` command is essential for environment changes to persist
