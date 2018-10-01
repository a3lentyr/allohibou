for /f %%i in ('python ./generate.py') do set source_svg=%%i
set INKSCAPE_PATH="C:\Program Files\Inkscape\inkscape.exe"
cmd /C "%INKSCAPE_PATH% -z -f %source_svg% -w 2160 -j -e %source_svg%.png"