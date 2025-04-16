@echo off
REM Run the container in detached mode with a published port.
FOR /F %%i IN ('docker run -d -p 8080:80 jenkin:latest') DO SET container_id=%%i

REM Allow some time for the container to start.
timeout /t 5 > NUL

REM Fetch the response from the local server.
curl -s http://localhost:8080 > response.txt

REM Search for the expected text.
findstr /C:"welcome to my test website" response.txt > NUL

IF %ERRORLEVEL% EQU 0 (
    echo Test passed: Site content is correct.
    SET ret=0
) ELSE (
    echo Test failed: Site content is not correct.
    SET ret=1
)

REM Stop the container.
docker stop %container_id% > NUL

exit /b %ret%
