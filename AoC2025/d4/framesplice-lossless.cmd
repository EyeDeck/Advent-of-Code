cd %1%

set /A fps = %2%
if %fps%==0 (set fps=60)

ffmpeg -y -f image2 -r %fps% -i %%05d.png -vf fps=%fps%,scale=-1:-1 -an -c:v vp9 -lossless 1 -b:v 160k -quality best -pass 1 -f rawvideo NUL
ffmpeg -y -f image2 -r %fps% -i %%05d.png -vf fps=%fps%,scale=-1:-1 -an -c:v vp9 -lossless 1 -b:v 160k -quality best -pass 2 ..\%1%.webm