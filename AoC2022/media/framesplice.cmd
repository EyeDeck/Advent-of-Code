cd %1%
REM ffmpeg -y -f image2 -r 50 -i frame%%06d.png -vf fps=50 -r 50 -framerate 50 ..\d12.gif

REM set /A bitRate=(24000000/15)
REM set /A bitRateA=(24000000/150)
REM set outFile="%outputFolder%\%~n1.webm"
REM @echo on
REM "C:\Program Files\ffmpeg\bin\ffmpeg" -y -i %1 -c:a libvorbis -c:v libvpx -b:v %bitRate% -slices 1 -threads 4 -crf 6 -quality best -pass 1 -f rawvideo NUL
REM "C:\Program Files\ffmpeg\bin\ffmpeg" -y -i %1 -c:a libvorbis -c:v libvpx -b:v %bitRate% -slices 1 -threads 4 -crf 6 -quality best -pass 2 %outFile%
set fps=60
ffmpeg -y -f image2 -r %fps% -i %%05d.png -vf fps=%fps%,scale=-1:1016 -an -c:v vp9  -b:v 160k -quality best -pass 1 -f rawvideo NUL
ffmpeg -y -f image2 -r %fps% -i %%05d.png -vf fps=%fps%,scale=-1:1016 -an -c:v vp9  -b:v 160k -quality best -pass 2 ..\%1%.webm