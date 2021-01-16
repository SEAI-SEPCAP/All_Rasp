
def alter(boundaries, color_name, rgb_values):

	new_boundaries = boundaries

	for i in range(len(boundaries)):
		
		
		
		blue = rgb_values[0]
		green = rgb_values[1]
		red = rgb_values[2]
		
		limit = 10
		
		if boundaries[i][2] == color_name:
			
			new_boundaries[i][0][0] = blue - limit
			new_boundaries[i][0][1] = green - limit
			new_boundaries[i][0][2] = red - limit
			
			new_boundaries[i][1][0] = blue + limit
			new_boundaries[i][1][1] = green + limit
			new_boundaries[i][1][2] = red + limit
			





	return new_boundaries
    

