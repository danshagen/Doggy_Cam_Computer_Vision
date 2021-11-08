SRC = $(wildcard *.mov)
OBJ = $(patsubst %.mov, %.mp4,$(SRC))

convert: $(OBJ)

%.mp4: %.mov
	ffmpeg -i $< -vcodec libx264 -pix_fmt yuv420p $@
