terraingen: terraingen.cpp
	g++ -O3 -shared -o terraingen.so -fPIC terraingen.cpp
	x86_64-w64-mingw32-g++ -static -static-libgcc -static-libstdc++ -O3 -shared -o terraingen.dll -fPIC terraingen.cpp
