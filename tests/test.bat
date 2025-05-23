@echo off

REM Clean up any existing container using the same port
FOR /F %%i IN ('docker ps -q --filter "ancestor=jenkin:latest"') DO docker stop %%i > NUL

REM Run the container in detached mode with a published port.
FOR /F %%i IN ('docker run -d -p 8081:80 jenkin:latest') DO SET container_id=%%i

REM Allow some time for the container to start.
timeout /t 5 > NUL

REM Fetch the response from the local server.
curl http://localhost:8081 > response.txt 2>NUL

REM Search for the expected text.
findstr /C:"Hello, welcome to my test website!" response.txt > NUL

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
