#include <algorithm>
#include <iostream>
#include <set>
#include <tuple>
#include <vector>
#include <random>
#include <chrono>


typedef std::tuple<int,int,int,int> quad;

extern "C"
{
	void drainage_simulation(int* inputGreyscale, int* outputGreyscale, int width, int height, int pathCount, int perPath, int pixelMax)
	{
		static std::mt19937 mt{static_cast<unsigned int>(std::chrono::steady_clock::now().time_since_epoch().count())};
		static std::uniform_int_distribution<> posRng{ 0, (width*height)-1 };

		int prevDx;
		int prevDy;
		int value;
		int pixelpos;
		int pos;
		int dx;
		int dy;
		int angle;

		for (int i{0}; i < pathCount; ++i)
		{
			while(true)
			{
				pixelpos = posRng(mt);
				if (inputGreyscale[pixelpos] > 0)
					break;
			}

			prevDx = 0;
			prevDy = 0;

			std::set<int> visited;
			while(true)
			{
				visited.insert(pixelpos);
				outputGreyscale[pixelpos] = std::min((outputGreyscale[pixelpos] + perPath), pixelMax);

				if(inputGreyscale[pixelpos] == 0)
					break;

				std::vector<quad> neighbours;
				for (int dx{-1}; dx <= 1; ++dx)
				{
					for (int dy{-1}; dy <= 1; ++dy)
					{
						int neighbourPos = pixelpos+dy+dx*width;
						if (visited.find(neighbourPos) == visited.end())
							neighbours.push_back({inputGreyscale[neighbourPos], neighbourPos, dx, dy});
					}
				}

				std::sort(neighbours.begin(), neighbours.end());

				if (neighbours.size() == 0)
					break;
				int minElev = std::get<0>(neighbours[0]);

				std::vector<quad> angles;
				for (quad q : neighbours)
				{
					std::tie(value, pos, dx, dy) = q;
					if(value == minElev)
					{
						int angle = abs(prevDx-dx) + abs(prevDy-dy);
						angles.push_back({angle, pos, dx, dy});
					}
				}

				std::sort(angles.begin(), angles.end());
				bool validNeighbour = false;
				for(quad q : angles)
				{
					std::tie(angle, pos, dx, dy) = q;
					if (visited.find(pos) == visited.end())
					{
						pixelpos = pos;
						prevDx = dx;
						prevDy = dy;
						validNeighbour = true;
						break;
					}
				}
				if (!validNeighbour)
					break;
			}
		}
	}
}

/*int main()
{
	int arr[100];
	int arrB[100];
	for(int i{0}; i < 100; ++i)
	{
		arr[i] = i;
		arrB[i] = 0;

		if(i % 10 == 0)
			arr[i] = 0;
		if(i % 10 == 9)
			arr[i] = 0;
		if(i < 10)
			arr[i] = 0;
		if(i > 89)
			arr[i] = 0;
	}
	drainage_simulation(arr,arrB, 10, 10, 100, 8, 255);
}*/
