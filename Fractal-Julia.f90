!Fractal assignment 1 "Julia Set Fractal" (Frac1Lab7.f90)
!	Creates data for a Julia set fractal
!gfortran compile command: gfortran Frac1Lab7.f90 -o Frac1Lab7

program Frac1Lab7
	implicit none
	real, dimension(:,:), allocatable :: dat
	real :: xmin, xmax, ymin, ymax, dx, dy, zr, zi, cr, ci
	integer :: ios, nx, ny, ix, iy, it, ofile = 12
	integer, dimension(2) :: nxny
	complex :: c, z
	real, dimension(4) :: wind

	cr = 0.4; ci = 0. !these values ar connected with iteration stop for detail of image

	print '(a)', "Enter: xmin, xmax, ymin, ymax, number of x's, number of y's.", &
		"NOTE: for undistorted image, window should be square and nx = ny."
	read(*, *, iostat = ios) xmin, xmax, ymin, ymax, nx, ny !see end of file for suggested values
	do while(ios /= 0 .or. xmin >= xmax .or. ymin >= ymax)
		print '(a)', "Coordinate minimums and maximums must be real numbers and maxes must be larger than mins.",&
			"Number of x's and y's must be integers.", "Please input the values again:"
		read(*, *, iostat = ios) xmin, xmax, ymin, ymax, nx, ny
	enddo
	dx = (xmax-xmin)/real(nx)
	dy = (ymax-ymin)/real(ny)
	allocate(dat(1:nx,1:ny))
	do ix = 1, nx
		do iy = 1, ny
			zr = xmin- dx/2.+ dx*real(ix)
			zi = ymin- dy/2.+ dy*real(iy)
			c = cmplx(cr, ci)
			z = cmplx(zr, zi)
			do it = 1, 1000
				z = c + z*z
				if (abs(z) > 2) exit
			enddo
			dat(ix,iy) = it
		enddo
	enddo
	print *, "Finished calculation"
	print *, "Number of calculations =", sum(dat)
	open (ofile, file='fractal.bin', form='unformatted')
	nxny(1) = nx
	nxny(2) = ny
	write (ofile) nxny
	wind(1) = xmin
	wind(2) = xmax
	wind(3) = ymin
	wind(4) = ymax
	write (ofile) wind
	write (ofile) dat
	close(ofile)
end program Frac1Lab7

!Suggested inputs:
! -1.5,1.5,-1.5,1.5,1000,1000