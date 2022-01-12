!Fortran assignment 13 "Number Column Centering" (F13Lab6.f90)
!	creates 100,000 random numbers and saves to file
!	reads file of numbers and centers them around 0
!gfortran compile command: gfortran F13Lab6.f90 -o F13Lab6

program F13Lab6
	implicit none
	character (len=50) :: ifileN, ofileN
	integer :: ios = 0, i, ifid = 11, ofid = 12
	integer :: columns = 5, rows = 100000
	real :: mean
	real, dimension(:,:), allocatable :: centered
	allocate(centered(1:columns,1:rows), STAT = ios)
   	if (ios /= 0) then
   		print *,'Not enough memory to allocate matrix'
   		STOP
   	endif
	centered(:,:) = 0
	!call randomlist(columns, rows) !Can be commented if file already exists
	
	print '(a)', 'This program will center rows of numbers around 0', 'Enter input file name:'
	read "(a)", ifileN
	print *,'Input filename: ', trim(ifileN)
	open(ifid, file=ifileN, status='old')
	print *,'Enter output file name:'
	read "(a)", ofileN
	print *,'Output filename: ', trim(ofileN)
	open(ofid, file=ofileN)
	
	mean = 0
	ios = 0
	read(ifid, *, iostat = ios) centered(:,:)
	if (ios > 0) then
		print *, '***Possible error reading from file: ', trim(ifileN)
		print *, 'Outputting centered numbers up to the last line read.'
	endif
	i = 1
	do while(sum(centered(:,i)) /= 0 .and. i <= rows)
		mean = sum(centered(:,i))
		mean = mean/columns
		centered(:,i) = centered(:,i)-mean
		i = i+1
	enddo
	write(ofid, *) centered
	print *, 'Read', i-1,'lines from file', trim(ifileN)
	print *, '*Note: Max lines calculatable:', rows
	close(ifid)
	close(ofid)
end program F13Lab6

!subroutine randomlist creates columns of random numbers and outputs them to a file
!INPUT:
!	cols = number of columns to write to file
!	rows = number of rows to write to file
!OUTPUT:
!	NONE
!NOTES:
!	Can be easily altered to allow user to define random number range
!	Default is 0-500 with each row grouped within 100 
subroutine randomlist(cols, rows)
	integer, intent(in) :: cols, rows
	character (len=50) :: filename
	integer :: i = 1, irow = 1, fid = 15, error, mult = 100, add = 400
	real :: randadd
	real, dimension(:), allocatable :: randbase
	real, dimension(:,:), allocatable :: outputnums
	allocate(randbase(1:cols), STAT = error)
	allocate(outputnums(1:cols,1:rows), STAT = error)
	if (error /= 0) then
   		print *,'Not enough memory to allocate matrix'
   		STOP
   	endif
   
	print '(a)', 'This program will make a file with columns of numbers.', 'Enter file name: '
	read "(a)", filename
	print *,'Writing to filename: ', trim(filename)
	do i = 1, rows
		call random_number(randbase)
		call random_number(randadd)
		randbase = randbase*mult
		randadd = randadd*add
		outputnums(:,i) = randbase+randadd
	enddo
	open(fid, file=filename)
	write(fid, *) outputnums
	close(fid)
end subroutine randomlist