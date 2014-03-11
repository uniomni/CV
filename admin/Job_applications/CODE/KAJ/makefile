# Makefile for test of tri-diagonal solver

# Compiler options:
FLAGS  = 
FC     = gcc

default: run
	
tri.o:		tri.C tri.h
		$(FC) -c tri.C $(FLAGS)
		
tritest:	tritest.C tri.o
		rm -f $@ 
		$(FC) -o $@ $@.C tri.o -lm 

run:       	tritest makefile
	        tritest
		
clean:		
	        /bin/rm -f *.o *.lst *.T
		/bin/rm -f tritest
		/bin/rm -f *~ #*#
		/bin/rm -f core a.out

