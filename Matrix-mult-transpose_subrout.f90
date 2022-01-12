!Fortran assignment 14 "Matrix Multiplier and Transposer" (F14Lab6.f90)
!	calculates the cross product of two matrices and finds the transpose of the result
!gfortran compile command: gfortran F14Lab6.f90 -o F14Lab6

program F14Lab6
	implicit none
	real, dimension(3,3) :: a, b, c

	a(1,1:3) = (/ -5.1,  3.8,  4.2 /)
	a(2,1:3) = (/  9.7,  1.3, -1.3 /)
	a(3,1:3) = (/ -8.0, -7.3,  2.2 /)
	b(1,1:3) = (/  9.4, -6.2,  0.5 /)
	b(2,1:3) = (/ -5.1,  3.3, -2.2 /)
	b(3,1:3) = (/ -1.1, -1.8,  3.0 /)
	c = 0.

	call MULTMAT
	print *, "Matrix a follows:"
	call PRINTMAT(a)
	print *, "Matrix b follows:"
	call PRINTMAT(b)
	print *, "Matrix c = a*b follows:"
	call PRINTMAT(c)
	call TRANSMAT(c)
	print *, "Matrix c = transpose(c) follows:"
	call PRINTMAT(c)

contains

subroutine PRINTMAT(x)
	real, dimension(3,3) :: x
	integer :: i, j
	do i = 1, 3
		print "(3f8.3)", (x(i,j), j=1,3)
	enddo
end subroutine PRINTMAT

subroutine MULTMAT
	integer :: i, j, k
	do i = 1, 3
		do j = 1, 3
			do k = 1, 3
				c(i,j) = c(i,j) + a(i,k) * b(k,j)
			enddo
		enddo
	enddo
end subroutine MULTMAT

subroutine TRANSMAT(x)
	real, dimension(3,3), intent (inout) :: x
	real, dimension(3,3) :: y
	integer :: i, j
	y = x
	do i = 1, 3
		do j = 1, 3
			if (i /= j) x(i,j) = y(j,i)
		enddo
	enddo
	return
end subroutine TRANSMAT

end program F14Lab6