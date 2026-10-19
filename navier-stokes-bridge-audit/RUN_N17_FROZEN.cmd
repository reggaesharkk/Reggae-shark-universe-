@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

echo ============================================================
echo WP16 FROZEN N17 WINDOWS RUNNER
echo Frozen protocol: 27 September 2026
echo ============================================================
echo.
echo This launcher does NOT change K36, thresholds, seed, or search schedule.
echo It resumes safely from the atomic N17 checkpoint if one exists.
echo.

if not exist "src\wp16_036_N17_cpu_continuation.py" (
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

set "N16=results\wp16_n16_holdout\wp16_phase_cutoff_escalation_N16.json"
set "SOURCE_GZ=results\wp16_n12_holdout\wp16_036_phase_velocity_rhs_sources.json.gz"
set "SOURCE=results\wp16_n17_holdout\wp16_036_phase_velocity_rhs_sources.json"
set "OUTDIR=results\wp16_n17_holdout"
set "CHECKPOINT=%OUTDIR%\wp16_N17_checkpoint.json"
set "N17=%OUTDIR%\wp16_phase_cutoff_escalation_N17.json"
set "TIMEOUT=%OUTDIR%\wp16_036_N17_frozen_time_gate.json"
set "MECHOUT=%OUTDIR%\wp16_036_N17_mechanism_gate.json"
set "KEYS=results\wp16_n12_holdout\frozen_K36_ordered_source_orbits.json"

if not exist "%N16%" (
  echo ERROR: completed frozen N16 continuation is missing:
  echo %N16%
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
echo Verifying frozen N16 input hash...
%PY% -c "import hashlib,pathlib,sys; p=pathlib.Path(r'%N16%'); h=hashlib.sha256(p.read_bytes()).hexdigest(); print(h); sys.exit(0 if h=='53b0cc0a70de0d1a858e9d0c9d98feafcd5fea678c85adfe4d6253f6cf53b0ca' else 1)"
if errorlevel 1 (
  echo ERROR: N16 SHA-256 does not match the frozen predecessor.
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
if /I "%~1"=="mechanism" goto MECHANISM

echo Usage:
echo   RUN_N17_FROZEN.cmd smoke
echo   RUN_N17_FROZEN.cmd full
echo   RUN_N17_FROZEN.cmd gate
echo   RUN_N17_FROZEN.cmd mechanism
pause
exit /b 0

:SMOKE
echo.
echo ============================================================
echo N17 TRIAL-0 SMOKE
echo ============================================================
%PY% -u src\wp16_036_N17_cpu_continuation.py ^
  --n16-json "%N16%" ^
  --checkpoint "%CHECKPOINT%" ^
  --output "%N17%" ^
  --stop-after-trial 0
if errorlevel 1 goto FAIL
echo.
echo SMOKE COMPLETE.
echo Checkpoint: %CHECKPOINT%
goto DONE

:FULL
if not exist "%CHECKPOINT%" (
  echo ERROR: trial-0 checkpoint is missing. Run 01_N17_SMOKE.cmd first.
  goto FAIL
)
echo.
echo ============================================================
echo N17 FROZEN 520-PROPOSAL CONTINUATION
echo ============================================================
%PY% -u src\wp16_036_N17_cpu_continuation.py ^
  --n16-json "%N16%" ^
  --checkpoint "%CHECKPOINT%" ^
  --output "%N17%"
if errorlevel 1 goto FAIL
if not exist "%N17%" (
  echo ERROR: final N17 JSON is missing.
  goto FAIL
)
echo.
echo N17 CONTINUATION COMPLETE.
echo Output: %N17%
goto DONE

:GATE
if not exist "%N17%" (
  echo ERROR: N17 final continuation does not exist yet.
  echo Run the full continuation first.
  pause
  exit /b 10
)
echo.
echo ============================================================
echo N17 PROSPECTIVE FROZEN TIME GATE
echo ============================================================
%PY% -u src\wp16_036_N17_time_gate.py ^
  --n16-json "%N16%" ^
  --n17-json "%N17%" ^
  --source-json "%SOURCE%" ^
  --output "%TIMEOUT%"
if errorlevel 1 goto FAIL
echo.
echo N17 TIME GATE COMPLETE.
echo Output: %TIMEOUT%
goto DONE

:MECHANISM
if not exist "%N17%" (
  echo ERROR: N17 final continuation does not exist yet.
  pause
  exit /b 10
)
if not exist "%TIMEOUT%" (
  echo ERROR: run 03_N17_TIME_GATE.cmd first to check the frozen schedule.
  goto FAIL
)
if not exist "%KEYS%" (
  echo ERROR: frozen compact K36 keys are missing: %KEYS%
  goto FAIL
)
echo.
echo ============================================================
echo N17 FROZEN SOURCE AND NORMALIZER MECHANISM GATE
echo ============================================================
%PY% -u src\wp16_036_N17_mechanism_gate.py ^
  --n16 "%N16%" ^
  --n17 "%N17%" ^
  --keys "%KEYS%" ^
  --output "%MECHOUT%"
if errorlevel 1 (
  echo MECHANISM GATE FAILED OR WAS UNEVALUABLE.
  echo Preserve its JSON: %MECHOUT%
  goto FAIL
)
echo N17 MECHANISM GATE COMPLETE.
echo Output: %MECHOUT%
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
