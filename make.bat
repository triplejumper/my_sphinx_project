@ECHO OFF

pushd %~dp0

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=python -m sphinx
)
set SOURCEDIR=.
set BUILDDIR=_build

if "%1" == "" goto help

REM --- クリーン処理 ---
if "%1" == "clean" (
	if exist %BUILDDIR% rmdir /q /s %BUILDDIR%
	goto end
)

REM --- リビルド処理（クリーン後に html ビルドを実行）---
if "%1" == "rebuild" (
	if exist %BUILDDIR% rmdir /q /s %BUILDDIR%
	%SPHINXBUILD% -b html %SOURCEDIR% %BUILDDIR%/html %SPHINXOPTS% %O%
	goto end
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
