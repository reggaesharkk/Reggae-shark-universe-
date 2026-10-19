@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

echo ============================================================
echo WP16 FROZEN N14 WINDOWS RUNNER
echo Frozen protocol: 26 September 2026
echo ============================================================
echo.
echo This launcher does NOT change K36, thresholds, seed, or search schedule.
echo It resumes safely from the atomic N14 checkpoint if one exists.
echo.

if not exist "src\wp16_036_N14_cpu_continuation.py" (
  echo ERROR: Put these launcher files in the ROOT of navier-stokes-bridge-audit.
  echo The folder must contain src\ and results\.
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
    echo Install Python 3.12 or newer, then rerun this file.
    pause
    exit /b 3
  )
)

echo Python:
%PY% --version

%PY% -c "import numpy; print('NumPy', numpy.__version__)" >nul 2>&1
if errorlevel 1 (
  echo NumPy not found. Installing repository requirements...
  %PY% -m pip install -r requirements.txt
  if errorlevel 1 (
    echo ERROR: dependency installation failed.
    pause
    exit /b 4
  )
)
%PY% -c "import numpy; print('NumPy', numpy.__version__)"

set "N13=results\wp16_n13_holdout\wp16_phase_cutoff_escalation_N13.json"
set "SOURCE_GZ=results\wp16_n12_holdout\wp16_036_phase_velocity_rhs_sources.json.gz"
set "SOURCE=results\wp16_n14_holdout\wp16_036_phase_velocity_rhs_sources.json"
set "OUTDIR=results\wp16_n14_holdout"
set "CHECKPOINT=%OUTDIR%\wp16_N14_checkpoint.json"
set "N14=%OUTDIR%\wp16_phase_cutoff_escalation_N14.json"
set "TIMEOUT=%OUTDIR%\wp16_036_N14_frozen_time_gate.json"

if not exist "%N13%" (
  echo ERROR: canonical N13 input is missing:
  echo %N13%
  pause
  exit /b 5
)
if not exist "%SOURCE_GZ%" (
  echo ERROR: canonical K36 source archive is missing:
  echo %SOURCE_GZ%
  pause
  exit /b 6
)

if not exist "%OUTDIR%" mkdir "%OUTDIR%"

echo.
echo Verifying frozen N13 input hash...
%PY% -c "import hashlib,pathlib,sys; p=pathlib.Path(r'%N13%'); h=hashlib.sha256(p.read_bytes()).hexdigest(); print(h); sys.exit(0 if h=='13e5e56676b9398e7c7ec32f55e32a4d07dec5a3830c67787c6cd6fb5c8e59cd' else 1)"
if errorlevel 1 (
  echo ERROR: N13 SHA-256 does not match the frozen continuation.
  echo Do not continue with this input.
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

if /I "%~1"=="smoke" goto SMOKE
if /I "%~1"=="full" goto FULL
if /I "%~1"=="gate" goto GATE
if /I "%~1"=="all" goto ALL

echo.
echo Usage:
echo   RUN_N14_FROZEN.cmd smoke   - baseline/inherited trial-0 smoke only
echo   RUN_N14_FROZEN.cmd full    - resume/complete frozen 520 proposals
echo   RUN_N14_FROZEN.cmd gate    - run frozen N14 time gate after completion
echo   RUN_N14_FROZEN.cmd all     - smoke, full continuation, then time gate
echo.
pause
exit /b 0

:SMOKE
echo.
echo ============================================================
echo N14 TRIAL-0 SMOKE
echo ============================================================
%PY% -u src\wp16_036_N14_cpu_continuation.py ^
  --n13-json "%N13%" ^
  --checkpoint "%CHECKPOINT%" ^
  --output "%N14%" ^
  --stop-after-trial 0
if errorlevel 1 goto FAIL
echo.
echo SMOKE COMPLETE.
echo Checkpoint: %CHECKPOINT%
goto DONE

:FULL
echo.
echo ============================================================
echo N14 FROZEN 520-PROPOSAL CONTINUATION
echo ============================================================
echo Safe to rerun after interruption: it resumes from %CHECKPOINT%
echo.
%PY% -u src\wp16_036_N14_cpu_continuation.py ^
  --n13-json "%N13%" ^
  --checkpoint "%CHECKPOINT%" ^
  --output "%N14%"
if errorlevel 1 goto FAIL
if not exist "%N14%" (
  echo ERROR: continuation returned without producing the final N14 JSON.
  goto FAIL
)
echo.
echo N14 CONTINUATION COMPLETE.
echo Output: %N14%
goto DONE

:GATE
if not exist "%N14%" (
  echo ERROR: N14 final continuation does not exist yet.
  echo Run: RUN_N14_FROZEN.cmd full
  pause
  exit /b 9
)
echo.
echo ============================================================
echo N14 PROSPECTIVE FROZEN TIME GATE
echo ============================================================
%PY% -u src\wp16_036_N14_time_gate.py ^
  --n13-json "%N13%" ^
  --n14-json "%N14%" ^
  --source-json "%SOURCE%" ^
  --output "%TIMEOUT%"
if errorlevel 1 goto FAIL
echo.
echo N14 TIME GATE COMPLETE.
echo Output: %TIMEOUT%
goto DONE

:ALL
echo.
echo ============================================================
echo STEP 1/3 - TRIAL-0 SMOKE / CHECKPOINT VERIFY
echo ============================================================
%PY% -u src\wp16_036_N14_cpu_continuation.py ^
  --n13-json "%N13%" ^
  --checkpoint "%CHECKPOINT%" ^
  --output "%N14%" ^
  --stop-after-trial 0
if errorlevel 1 goto FAIL

echo.
echo ============================================================
echo STEP 2/3 - RESUME/COMPLETE FROZEN 520-PROPOSAL N14 SEARCH
echo ============================================================
%PY% -u src\wp16_036_N14_cpu_continuation.py ^
  --n13-json "%N13%" ^
  --checkpoint "%CHECKPOINT%" ^
  --output "%N14%"
if errorlevel 1 goto FAIL
if not exist "%N14%" (
  echo ERROR: final N14 JSON is missing after continuation.
  goto FAIL
)

echo.
echo ============================================================
echo STEP 3/3 - FROZEN N14 TIME GATE
echo ============================================================
%PY% -u src\wp16_036_N14_time_gate.py ^
  --n13-json "%N13%" ^
  --n14-json "%N14%" ^
  --source-json "%SOURCE%" ^
  --output "%TIMEOUT%"
if errorlevel 1 goto FAIL

echo.
echo ============================================================
echo ALL FROZEN N14 STEPS COMPLETE
echo ============================================================
echo Send these two files back to ChatGPT:
echo   %N14%
echo   %TIMEOUT%
echo.
echo Keep this checkpoint too:
echo   %CHECKPOINT%
goto DONE

:FAIL
echo.
echo ============================================================
echo RUN STOPPED WITH AN ERROR
echo ============================================================
echo Do NOT delete the checkpoint.
echo If the full run had already started, rerun the same command; completed
echo proposals are preserved atomically.
pause
exit /b 10

:DONE
echo.
pause
exit /b 0
