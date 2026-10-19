@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

echo ============================================================
echo WP16 FROZEN N15 WINDOWS RUNNER
echo Frozen protocol: 26 September 2026
echo ============================================================
echo.
echo This launcher does NOT change K36, thresholds, seed, or search schedule.
echo It resumes safely from the atomic N15 checkpoint if one exists.
echo.

if not exist "src\wp16_036_N15_cpu_continuation.py" (
  echo ERROR: Run this from the ROOT of navier-stokes-bridge-audit.
  pause
  exit /b 2
)

set "PY=python"
%PY% --version >nul 2>&1
if errorlevel 1 (
  set "PY=py -3"
  %PY% --version >nul 2>&1
  if errorlevel 1 (
    echo ERROR: Python 3 was not found.
    pause
    exit /b 3
  )
)

echo Python:
%PY% --version
%PY% -c "import numpy; print('NumPy', numpy.__version__)" >nul 2>&1
if errorlevel 1 (
  %PY% -m pip install -r requirements.txt
  if errorlevel 1 (
    echo ERROR: dependency installation failed.
    pause
    exit /b 4
  )
)
%PY% -c "import numpy; print('NumPy', numpy.__version__)"

set "N14=results\wp16_n14_holdout\wp16_phase_cutoff_escalation_N14.json"
set "SOURCE_GZ=results\wp16_n12_holdout\wp16_036_phase_velocity_rhs_sources.json.gz"
set "SOURCE=results\wp16_n15_holdout\wp16_036_phase_velocity_rhs_sources.json"
set "OUTDIR=results\wp16_n15_holdout"
set "CHECKPOINT=%OUTDIR%\wp16_N15_checkpoint.json"
set "N15=%OUTDIR%\wp16_phase_cutoff_escalation_N15.json"
set "TIMEOUT=%OUTDIR%\wp16_036_N15_frozen_time_gate.json"

if not exist "%N14%" (
  echo ERROR: completed frozen N14 continuation is missing:
  echo %N14%
  pause
  exit /b 5
)
if not exist "%SOURCE_GZ%" (
  echo ERROR: frozen K36 source archive is missing:
  echo %SOURCE_GZ%
  pause
  exit /b 6
)
if not exist "%OUTDIR%" mkdir "%OUTDIR%"

echo.
echo Verifying frozen N14 input hash...
%PY% -c "import hashlib,pathlib,sys; p=pathlib.Path(r'%N14%'); h=hashlib.sha256(p.read_bytes()).hexdigest(); print(h); sys.exit(0 if h=='747dfb0bd0ea12271bd53b39fae7a4e18f396656bed3084bd4c632a9f3e5a3d9' else 1)"
if errorlevel 1 (
  echo ERROR: N14 SHA-256 does not match the frozen predecessor.
  pause
  exit /b 7
)

if not exist "%SOURCE%" (
  echo.
  echo Decompressing frozen K36 source archive...
  %PY% -c "import gzip,shutil,pathlib; s=pathlib.Path(r'%SOURCE_GZ%'); d=pathlib.Path(r'%SOURCE%'); d.parent.mkdir(parents=True,exist_ok=True); f=gzip.open(s,'rb'); o=d.open('wb'); shutil.copyfileobj(f,o); o.close(); f.close(); print('Wrote',d)"
  if errorlevel 1 (
    echo ERROR: source decompression failed.
    pause
    exit /b 8
  )
)

echo Verifying frozen source JSON hash...
%PY% -c "import hashlib,pathlib,sys; p=pathlib.Path(r'%SOURCE%'); h=hashlib.sha256(p.read_bytes()).hexdigest(); print(h); sys.exit(0 if h=='193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e' else 1)"
if errorlevel 1 (
  echo ERROR: source JSON SHA-256 mismatch.
  pause
  exit /b 9
)

if /I "%~1"=="smoke" goto SMOKE
if /I "%~1"=="full" goto FULL
if /I "%~1"=="gate" goto GATE

echo Usage:
echo   RUN_N15_FROZEN.cmd smoke
echo   RUN_N15_FROZEN.cmd full
echo   RUN_N15_FROZEN.cmd gate
pause
exit /b 0

:SMOKE
echo.
echo ============================================================
echo N15 TRIAL-0 SMOKE
echo ============================================================
%PY% -u src\wp16_036_N15_cpu_continuation.py ^
  --n14-json "%N14%" ^
  --checkpoint "%CHECKPOINT%" ^
  --output "%N15%" ^
  --stop-after-trial 0
if errorlevel 1 goto FAIL
echo.
echo SMOKE COMPLETE.
echo Checkpoint: %CHECKPOINT%
goto DONE

:FULL
echo.
echo ============================================================
echo N15 FROZEN 520-PROPOSAL CONTINUATION
echo ============================================================
%PY% -u src\wp16_036_N15_cpu_continuation.py ^
  --n14-json "%N14%" ^
  --checkpoint "%CHECKPOINT%" ^
  --output "%N15%"
if errorlevel 1 goto FAIL
if not exist "%N15%" (
  echo ERROR: final N15 JSON is missing.
  goto FAIL
)
echo.
echo N15 CONTINUATION COMPLETE.
echo Output: %N15%
goto DONE

:GATE
if not exist "%N15%" (
  echo ERROR: N15 final continuation does not exist yet.
  echo Run the full continuation first.
  pause
  exit /b 10
)
echo.
echo ============================================================
echo N15 PROSPECTIVE FROZEN TIME GATE
echo ============================================================
%PY% -u src\wp16_036_N15_time_gate.py ^
  --n14-json "%N14%" ^
  --n15-json "%N15%" ^
  --source-json "%SOURCE%" ^
  --output "%TIMEOUT%"
if errorlevel 1 goto FAIL
echo.
echo N15 TIME GATE COMPLETE.
echo Output: %TIMEOUT%
goto DONE

:FAIL
echo.
echo RUN STOPPED WITH AN ERROR.
echo Do not delete the checkpoint.
pause
exit /b 11

:DONE
echo.
pause
exit /b 0
