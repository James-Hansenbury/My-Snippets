!Fortran assignment 15 "Data Processor" (F15Lab6.f90)
!	Extracts data from station information for earthquake events
!	Input format has headers of event info followed by station readings
!	See scsn.phase.dat
!	gfortran compile command: gfortran F15Lab6.f90 -o F15Lab6

program F15Lab6
	implicit none
	character (len=15), dimension(4) :: trash
	character (len=50) :: ifileN, ofileN
	character (len=100) :: readchar, writechar
	integer :: ios = 0, iosalt = 0, i, ifid = 11, ofid = 12, mindepth = 3, maxdepth = 8
	logical :: deep = .false.
	
	print '(a)', 'This program will process data from a file.', 'Enter input file name:'
	read '(a)', ifileN
	print *,'Input filename: ', trim(ifileN)
	open(ifid, file=ifileN, status='old')
	print *,'Enter output file name:'
	read '(a)', ofileN
	print *,'Output filename: ', trim(ofileN)
	open(ofid, file=ofileN)
	
	ios = 0
	do while (ios == 0)
		read(11,'(a)', iostat = ios) readchar
		if (ios > 0) then
			print *, "Error reading file, stopping at error line."
			exit
		endif
		if (index(readchar, achar(9)) /= 1 .and. index(readchar, achar(32)) /= 1) then
			deep = .false.
			call WRITE_EVENT
		else if (deep .eqv. .false.) then  !has starting tab or space, must be station measurement
			cycle
		else
			call WRITE_DATA
		endif
	enddo 

	close(ifid)
	close(ofid)
	print *, "Finished processing, file name: ", ofileN

contains

subroutine WRITE_EVENT
	character (len=15) :: date, time, magstr, latstr, lonstr, depstr, idstr
	real :: magnitude, lat, lon, depth
	integer :: id, iter
	do iter = 1, 100
		if (readchar(iter:iter) == '/') readchar(iter:iter) = '-'
	enddo
	read(readchar, *)&
		 date, time, trash(1), magnitude, trash(2), lat, lon, depth, trash(3), id
	if (depth <= maxdepth .and. depth >= mindepth) then
		do iter = 1, 15
			if (date(iter:iter) == '-') date(iter:iter) = '/'
		enddo
		write(magstr, '(f0.2)') magnitude
		write(latstr, '(f0.3)') lat
		write(lonstr, '(f0.3)') lon
		write(depstr, '(f0.2)') depth
		write(idstr, '(i0)') id
		writechar = trim(idstr) //' '//  trim(date) //' '// trim(time) //' '// trim(latstr)&
		//'/'// trim(lonstr) // ' Mag: ' // trim(magstr) // ' Depth: ' // trim(depstr)
		write(ofid, *) writechar
		deep = .true.
	endif
end subroutine WRITE_EVENT

subroutine WRITE_DATA
	real :: distance, time, calibration
	character :: phase
	read(readchar( :24), *) trash(1:3), phase
	if (scan(trash(1)(2:2), '(0,1,2,3,4,5,6,7,8,9)') /= 1 .and.&
		 (scan(phase, 'P') == 1 .or. scan(phase, 'p') == 1)) then
		read(readchar(28: ), *) time, distance
		write(writechar, '(x, f0.3, t15, f0.3)') time, distance
		write(ofid, *) writechar
	endif
end subroutine WRITE_DATA

end program F15Lab6