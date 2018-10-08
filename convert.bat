:loop

for /f %%i in ('python ./generate.py') do set source_svg=%%i
set INKSCAPE_PATH="C:\Program Files\ImageMagick-7.0.7-Q16\convert.exe"
cmd /C "%INKSCAPE_PATH% -density 1200 %source_svg% %source_svg%.png"

goto loop