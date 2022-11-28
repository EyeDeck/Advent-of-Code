cd %1%
REM ffmpeg -y -f image2 -r 50 -i frame%%06d.png -vf fps=50 -r 50 -framerate 50 ..\d12.gif

REM set /A bitRate=(24000000/15)
REM set /A bitRateA=(24000000/150)
REM set outFile="%outputFolder%\%~n1.webm"
REM @echo on
REM "C:\Program Files\ffmpeg\bin\ffmpeg" -y -i %1 -c:a libvorbis -c:v libvpx -b:v %bitRate% -slices 1 -threads 4 -crf 6 -quality best -pass 1 -f rawvideo NUL
REM "C:\Program Files\ffmpeg\bin\ffmpeg" -y -i %1 -c:a libvorbis -c:v libvpx -b:v %bitRate% -slices 1 -threads 4 -crf 6 -quality best -pass 2 %outFile%
set fps=120
REM ffmpeg -y -f image2 -r %fps% -i frame%%06d.png -vf fps=%fps% -an -c:v libvpx -b:v 200k -qmin 0 -qmax 10 -keyint_min 10000 -quality best -pass 1 -f rawvideo NUL
REM ffmpeg -y -f image2 -r %fps% -i frame%%06d.png -vf fps=%fps% -an -c:v libvpx -b:v 200k -qmin 0 -qmax 10 -keyint_min 10000 -quality best -pass 2 ..\%1%.webm
REM ffmpeg -y -f image2 -r %fps% -i frame%%06d.png -vf fps=%fps% -an -c:v libvpx -b:v 200k -qmin 0 -qmax 10 -keyint_min 10000 -quality best -pass 1 -f rawvideo NUL
ffmpeg -y -f image2 -r %fps% -i frame%%06d.png -vf fps=%fps% -an -c:v libvpx -b:v 200k -crf 20 -qmin 0 -qmax 50 -keyint_min 10000 -quality best -pass 1 -f rawvideo NUL
ffmpeg -y -f image2 -r %fps% -i frame%%06d.png -vf fps=%fps% -an -c:v libvpx -b:v 200k -crf 20 -qmin 0 -qmax 50 -keyint_min 10000 -quality best -pass 2 ..\%1%.webm