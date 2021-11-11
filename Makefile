REF_SRC = $(wildcard reference/*.csv)
REF_OBJ = $(patsubst %.csv, %.pkl,$(REF_SRC))

reference: $(REF_OBJ)

%.pkl: %.csv
	echo $<
	python3 convert_annotations.py $<