!TicTacToe Assignment 7 "TicTacToe Smart Computer" (TTT7Lab9.f90)
! finishing the TicTacToe program, making the computer smart about its moves
!	gfortran compile command: gfortran TTT7Lab9.f90 -o TTT7Lab9

!NOTE: The program will assign each player a number, and the number will be connected to X or O.
!	For example, if the player chooses X, they will be assigned the number 1 for the purpose of keeping track of the board.
program TTT7Lab9
	implicit none
	integer, dimension(1:9) :: board
	integer, external :: CHECKWINNER, FINDMOVE, READMOVE, FINDMOVE_DANBURY
	logical, external :: CHECKMOVE
	integer :: spot, ios, human, computer, win = 0
	character :: humarker, answer
	board = 0

	print *, "Would you like to be X's or O's?"
	read(*,*, iostat = ios) humarker
	do while (ios /= 0 .or. (humarker /= 'o' .and.&
		humarker /= 'x' .and. humarker /= 'O' .and. humarker /= 'X'))
		print *, "Please enter either 'x' or 'o'"
		read(*,*, iostat = ios) humarker
	enddo
	if (humarker == 'x' .or. humarker == 'X') then
		humarker = 'X'
	else
		humarker = 'O'
	endif
	print *, "Would you like to go first? Y/N"
	read(*,*, iostat = ios) answer
	do while (ios /= 0 .or. (answer /= 'y' .and.&
		answer /= 'n' .and. answer /= 'Y' .and. answer /= 'N'))
		print *, "Please enter either 'Y' or 'N'"
		read(*,*, iostat = ios) answer
	enddo
	if (answer == 'y' .or. answer == 'Y') then
		human = 1
		computer = 4
	else
		human = 2
		computer = 3
		print *, "Computer goes first!"
		board(5) = computer
		call PRINTBOARD(board, humarker)
	endif
	do
		board(READMOVE(board)) = human
		call PRINTBOARD(board, humarker)
		win = CHECKWINNER(board)
		if (win /= 0) call ENDGAME(win, human)
		board(FINDMOVE_DANBURY(board)) = computer
		call PRINTBOARD(board, humarker)
		win = CHECKWINNER(board)
		if (win /= 0) call ENDGAME(win, human)
	enddo
end program TTT7Lab9

!Shows the current board
subroutine PRINTBOARD(boardstat, humark)
	integer, dimension(1:9), intent(in) :: boardstat
	character, intent(in) :: humark
	integer :: i, j
	character, dimension(1:9) :: boardxo
	character :: compmark
	if (humark == 'X') compmark = 'O'
	if (humark == 'O') compmark = 'X'
	boardxo = ' '
	print *, "Current board:"
	do i = 0, 2
		do j = 1, 3
			if(boardstat(i*3+j) == 1 .or. boardstat(i*3+j) == 2) boardxo(i*3+j) = humark
			if(boardstat(i*3+j) == 3 .or. boardstat(i*3+j) == 4) boardxo(i*3+j) = compmark
			write(*,'(x,a,x)',advance='no') boardxo(i*3+j)
			if (j < 3) write(*,'(a)',advance='no') "|"
		enddo
		if (i < 2) print '(/,a)', "---+---+---"
	enddo
	print *
end subroutine PRINTBOARD

!Receives a move from player
integer function READMOVE(board)
	implicit none
	integer, dimension(1:9), intent(in) :: board
	integer :: ios, choice
	logical, external :: CHECKMOVE
	logical :: validSpot
	print *, "The board positions are as follows:"
	print '(a)', " 1 | 2 | 3 ", "---+---+---", " 4 | 5 | 6 ", "---+---+---", " 7 | 8 | 9 ", "Choose a spot to place your marker:"
	read(*,*, iostat = ios) choice
	do while (ios /= 0 .or. choice > 9 .or. choice < 1)
		print *, "Enter a number 1-9 to indicate the position of your marker:"
		read(*,*, iostat = ios) choice
	enddo
	validSpot = CHECKMOVE(board, choice)
	do while (validSpot .eqv. .FALSE.)
		print *, "That spot is taken! Choose a new spot:"
		read(*,*, iostat = ios) choice
		do while (ios /= 0 .or. choice > 9 .or. choice < 1)
			print *, "Enter a number 1-9 to indicate the position of your marker:"
			read(*,*, iostat = ios) choice
		enddo
		validSpot = CHECKMOVE(board, choice)
	enddo
	READMOVE = choice
end function READMOVE

!Checks if a move is available
logical function CHECKMOVE(boardstat, spot)
	integer, dimension(1:9), intent(in) :: boardstat
	integer, intent(in) :: spot
	if (boardstat(spot) /= 0) then
		CHECKMOVE = .FALSE.
		return
	endif
	CHECKMOVE = .TRUE.
end function CHECKMOVE

!Finds a random move for computer
integer function FINDMOVE(boardstat)
	implicit none
	integer, dimension(1:9), intent(in) :: boardstat
	integer :: i, countopen, selcount
	real :: randnum
	countopen = 0
	print *, "Computer is guessing a spot!"
	do i = 1, 9
		if (boardstat(i) == 0) countopen = countopen+1
	enddo
	call random_number(randnum)
	randnum = countopen*randnum
	selcount = int(randnum) + 1
	do i = 1, 9
		if (boardstat(i) == 0) selcount = selcount-1
		if (selcount == 0) then
			FINDMOVE = i
			exit
		endif
	enddo
	return
end function FINDMOVE

!Checks if a winner has successully filled 3 in a row
integer function CHECKWINNER(board)
	implicit none
	integer, dimension(1:9), intent(in) :: board
	integer :: j
	do j = 1,4
		if ((board(1) == j .and. board(5) == j .and. board(9) == j) .or. &
			(board(3) == j .and. board(5) == j .and. board(7) == j) .or. &
			(board(1) == j .and. board(2) == j .and. board(3) == j) .or. &
			(board(4) == j .and. board(5) == j .and. board(6) == j) .or. &
			(board(7) == j .and. board(8) == j .and. board(9) == j) .or. &
			(board(1) == j .and. board(4) == j .and. board(7) == j) .or. &
			(board(2) == j .and. board(5) == j .and. board(8) == j) .or. &
			(board(3) == j .and. board(6) == j .and. board(9) == j)) then
				CHECKWINNER = j
				return
		endif
	enddo
	if (sum(board) >= 21) then
		CHECKWINNER = 5
		return
	endif
	CHECKWINNER = 0
end function CHECKWINNER

!Prints message at the end of the game, ends program
subroutine ENDGAME(winner, hum_num)
	implicit none
	integer, intent(in) :: winner, hum_num
	if (winner == 5) then
		print *, "Meow. Cat's game! No winners this time..."
	elseif (winner == hum_num) then
		print *, "Human user wins! Congratulations!"
	else
		print *, "The computer won! Better luck next time..."
	endif
	stop
end subroutine ENDGAME

!-----------------------ASSIGNMENT:------------------------------------
!Finds a smart move for the computer
integer function FINDMOVE_DANBURY(board)
	integer, dimension(1:9), intent(in) :: board
	integer, external :: FINDMOVE
	integer :: i, countopen, selcount
	real :: randnum
	countopen = 0
	print *, "Computer is choosing a spot!"
!early choice, always center
	if (board(5) == 0) then
		FINDMOVE_DANBURY = 5
!Win moves:
	elseif (board(1) == 0 .and. ((board(9) > 2 .and. board(5) > 2) .or.&
		 (board(2) > 2 .and. board(3) > 2) .or.&
		 (board(4) > 2 .and. board(7) > 2))) then
		FINDMOVE_DANBURY = 1
	elseif (board(2) == 0 .and. ((board(3) > 2 .and. board(1) > 2) .or.&
		 (board(5) > 2 .and. board(8) > 2))) then
		FINDMOVE_DANBURY = 2
	elseif (board(3) == 0 .and. ((board(7) > 2 .and. board(5) > 2) .or.&
		 (board(1) > 2 .and. board(2) > 2) .or.&
		 (board(6) > 2 .and. board(9) > 2))) then
		FINDMOVE_DANBURY = 3
	elseif (board(4) == 0 .and. ((board(5) > 2 .and. board(6) > 2) .or.&
		 (board(7) > 2 .and. board(1) > 2))) then
		FINDMOVE_DANBURY = 4
	elseif (board(6) == 0 .and. ((board(4) > 2 .and. board(5) > 2) .or.&
		 (board(9) > 2 .and. board(3) > 2))) then
		FINDMOVE_DANBURY = 6
	elseif (board(7) == 0 .and. ((board(3) > 2 .and. board(5) > 2) .or.&
		 (board(8) > 2 .and. board(9) > 2) .or.&
		 (board(1) > 2 .and. board(4) > 2))) then
		FINDMOVE_DANBURY = 7
	elseif (board(8) == 0 .and. ((board(9) > 2 .and. board(7) > 2) .or.&
		 (board(2) > 2 .and. board(5) > 2))) then
		FINDMOVE_DANBURY = 8
	elseif (board(9) == 0 .and. ((board(1) > 2 .and. board(5) > 2) .or.&
		 (board(7) > 2 .and. board(8) > 2) .or. (board(3) > 2 .and.&
		 board(6) > 2 ))) then
		FINDMOVE_DANBURY = 9
!Don't lose moves:
	elseif (board(1) == 0 .and. (board(9) == board(5) .or.&
		 board(2) == board(3) .or. board(4) == board(7))) then
		FINDMOVE_DANBURY = 1
	elseif (board(2) == 0 .and. (board(3) == board(1) .or.&
		 board(5) == board(8))) then
		FINDMOVE_DANBURY = 2
	elseif (board(3) == 0 .and. (board(7) == board(5) .or.&
		 board(1) == board(2) .or. board(6) == board(9))) then
		FINDMOVE_DANBURY = 3
	elseif (board(4) == 0 .and. (board(5) == board(6) .or.&
		 board(7) == board(1))) then
		FINDMOVE_DANBURY = 4
	elseif (board(6) == 0 .and. (board(4) == board(5) .or.&
		 board(9) == board(3))) then
		FINDMOVE_DANBURY = 6
	elseif (board(7) == 0 .and. (board(3) == board(5) .or.&
		 board(8) == board(9) .or. board(1) == board(4))) then
		FINDMOVE_DANBURY = 7
	elseif (board(8) == 0 .and. (board(9) == board(7) .or.&
		 board(2) == board(5))) then
		FINDMOVE_DANBURY = 8
	elseif (board(9) == 0 .and. (board(1) == board(5) .or.&
		 board(7) == board(8) .or. board(3) == board(6))) then
		FINDMOVE_DANBURY = 9
!Trapping moves
	elseif (board(1) == 0 .and.&
		 ((((board(2) > 2 .or. board(3) > 2) .and. (board(3) == 0 .or. board(2) == 0)) .and.&
		 ((board(4) > 2 .or. board(7) > 2) .and. (board(4) == 0 .or. board(7) == 0))) .or.&
		 (((board(5) > 2 .and. board(9) == 0 )) .and.&
		 ((board(2) > 2 .or. board(3) > 2) .and. (board(3) == 0 .or. board(2) == 0))) .or.&
		 (((board(4) > 2 .or. board(7) > 2) .and. (board(4) == 0 .or. board(7) == 0)) .and.&
		 (board(5) > 2 .and. board(9) == 0 )))) then
		FINDMOVE_DANBURY = 1
	elseif (board(3) == 0 .and.&
		 ((((board(2) > 2 .or. board(1) > 2) .and. (board(1) == 0 .or. board(2) == 0)) .and.&
		 ((board(6) > 2 .or. board(9) > 2) .and. (board(6) == 0 .or. board(9) == 0))) .or.&
		 (((board(5) > 2 .and. board(7) == 0 )) .and.&
		 ((board(2) > 2 .or. board(1) > 2) .and. (board(1) == 0 .or. board(2) == 0))) .or.&
		 (((board(6) > 2 .or. board(9) > 2) .and. (board(6) == 0 .or. board(9) == 0)) .and.&
		 (board(5) > 2 .and. board(7) == 0 )))) then
		FINDMOVE_DANBURY = 3
	elseif (board(7) == 0 .and.&
		 ((((board(8) > 2 .or. board(9) > 2) .and. (board(8) == 0 .or. board(9) == 0)) .and.&
		 ((board(1) > 2 .or. board(4) > 2) .and. (board(1) == 0 .or. board(4) == 0))) .or.&
		 (((board(5) > 2 .and. board(3) == 0 )) .and.&
		 ((board(8) > 2 .or. board(9) > 2) .and. (board(8) == 0 .or. board(9) == 0))) .or.&
		 (((board(1) > 2 .or. board(4) > 2) .and. (board(1) == 0 .or. board(4) == 0)) .and.&
		 (board(5) > 2 .and. board(3) == 0 )))) then
		FINDMOVE_DANBURY = 7
	elseif (board(9) == 0 .and.&
		 ((((board(7) > 2 .or. board(8) > 2) .and. (board(7) == 0 .or. board(8) == 0)) .and.&
		 ((board(6) > 2 .or. board(3) > 2) .and. (board(6) == 0 .or. board(3) == 0))) .or.&
		 (((board(5) > 2 .and. board(1) == 0 )) .and.&
		 ((board(7) > 2 .or. board(8) > 2) .and. (board(7) == 0 .or. board(8) == 0))) .or.&
		 (((board(6) > 2 .or. board(3) > 2) .and. (board(6) == 0 .or. board(3) == 0)) .and.&
		 (board(5) > 2 .and. board(1) == 0 )))) then
		FINDMOVE_DANBURY = 9
	elseif (board(2) == 0 .and.&
		 (((board(1) > 2 .or. board(3) > 2) .and. (board(1) == 0 .or. board(3) == 0)) .and.&
		 (board(5) > 2 .and. board(8) == 0 ))) then
		FINDMOVE_DANBURY = 2
	elseif (board(4) == 0 .and.&
		 (((board(1) > 2 .or. board(7) > 2) .and. (board(1) == 0 .or. board(7) == 0)) .and.&
		 (board(5) > 2 .and. board(6) == 0 ))) then
		FINDMOVE_DANBURY = 4
	elseif (board(6) == 0 .and.&
		 (((board(3) > 2 .or. board(9) > 2) .and. (board(9) == 0 .or. board(3) == 0)) .and.&
		 (board(5) > 2 .and. board(4) == 0 ))) then
		FINDMOVE_DANBURY = 6
	elseif (board(8) == 0 .and.&
		 (((board(7) > 2 .or. board(9) > 2) .and. (board(9) == 0 .or. board(7) == 0)) .and.&
		 (board(5) > 2 .and. board(2) == 0 ))) then
		FINDMOVE_DANBURY = 8
!Lining up win
	elseif (board(1) == 0 .and.&
		 ((board(3) > 2 .and. board(2) == 0) .or. (board(2) > 2 .and. board(3) == 0) .or.&
		 (board(7) > 2 .and. board(4) == 0) .or. (board(4) > 2 .and. board(7) == 0) .or.&
		 (board(5) > 2 .and. board(9) == 0))) then
		FINDMOVE_DANBURY = 1
	elseif (board(3) == 0 .and.&
		 ((board(1) > 2 .and. board(2) == 0) .or. (board(2) > 2 .and. board(1) == 0) .or.&
		 (board(9) > 2 .and. board(6) == 0) .or. (board(6) > 2 .and. board(9) == 0) .or.&
		 (board(5) > 2 .and. board(7) == 0))) then
		FINDMOVE_DANBURY = 3
	elseif (board(7) == 0 .and.&
		 ((board(8) > 2 .and. board(9) == 0) .or. (board(9) > 2 .and. board(8) == 0) .or.&
		 (board(1) > 2 .and. board(4) == 0) .or. (board(4) > 2 .and. board(1) == 0) .or.&
		 (board(5) > 2 .and. board(3) == 0))) then
		FINDMOVE_DANBURY = 7
	elseif (board(9) == 0 .and.&
		 ((board(7) > 2 .and. board(8) == 0) .or. (board(8) > 2 .and. board(7) == 0) .or.&
		 (board(6) > 2 .and. board(3) == 0) .or. (board(3) > 2 .and. board(6) == 0) .or.&
		 (board(5) > 2 .and. board(1) == 0))) then
		FINDMOVE_DANBURY = 9
!Otherwise just random!
	else
		FINDMOVE_DANBURY = FINDMOVE(board)
	endif
	return
end function FINDMOVE_DANBURY