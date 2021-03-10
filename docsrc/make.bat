@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=source
set BUILDDIR=build
set BUILDDIR_HTML=build/html

if "%1" == "" goto help

if "%1" == "docs" (
    %SPHINXBUILD% -M html %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
    DEL /F/Q/S "../docs/*.*" > nul
    RMDIR /Q/S "../docs/"
    MKDIR "../docs/"
    robocopy %BUILDDIR_HTML%/_images/ ../docs/_images /E > nul
    robocopy %BUILDDIR_HTML%/_static/ ../docs/_static /E > nul
    robocopy %BUILDDIR_HTML%/stubs/ ../docs/stubs /E > nul
    robocopy %BUILDDIR_HTML% ../docs/ *.html > nul
    robocopy %BUILDDIR_HTML% ../docs/ *.js > nul
    robocopy %SOURCEDIR%/ ../docs/ .nojekyll  > nul

    echo.Generated files copied to ../docs
    goto end
)

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
