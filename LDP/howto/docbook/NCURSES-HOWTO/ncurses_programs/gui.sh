#!/bin/bash


# Front end to the ncurses programs compilation and run
# Implemented using 'dialog' which inturn uses ncurses


# Author: N N Ashok (nnashok@yahoo.com)
# Date: 07/15/2002
#
# Modified by: Pradeep Padala (ppadala@cise.ufl.edu)

# Notes:
# Basics:
#	Makefile does not build acs_vars
#	Done: hello_world: Nothing displayed to user??
#	Done: init_func_example: Nothing displayed to user??
#	Done: key_code: Does not exit with status 0
#	mouse_menu: Didnot work for me. Had to hit ^C
#	Done: simple_attr: The output does not stay, is scrolled fast
#	Done: simple_color: Nothing displayed to user??
#	temp_leave: When executed using the gui, the tty is not reset. Nothing
#	            echos to the screen
#	Done: with_chgat: Nothing displayed to user??
#	with_chgat: Does not indicate how to exit
#
# Forms:
#	None of the programs indicate how to exit. F1 exits the program.
# Menus:
#	menu_simple does not indicate how to exit. F1 exits the program.
#	menu_win does not indicate how to exit. F1 exits the program.
# Panels:
#	panel_resize: It seg faulted when I was resizing. Probably
#	the size had gone to negative value (I cant see the size being reduced,
#	only after I press the Enter do I see the new size).
#	panel_simple: Exists as soon as I press any key.

# Modified source files:
# basics/hello_world.c
# basics/init_func_example.c
# basics/key_code.c
# basics/simple_attr.c
# basics/simple_color.c
# basics/with_chgat.c

	

# Constants used
TRUE=0;
FALSE=-1;
EXEC_DIR="../demo/exe";
TEMP_FILE="/tmp/make.out";
tmp="tmp.out"


# Function declarations

# execMake: Function to execute 'make'
# Arguments:
# clean: Spcifies to do a 'make clean'
execMake()
{
	local clean;
	local result;

	# Check for arguments
	if [ "$1" == "clean" ]
	then
		clean="clean";
	else
		clean="";
	fi

	make $clean > $TEMP_FILE 2>&1
	result=$?;

	return $result;
}


# source_menu: Function to display the source code menu
# Arguments: None
source_menu()
{

	local menu_items;

	files_c=`ls *.c`;
	files=`echo $files_c | sed -e 's/\.c//g'`;

	title="Source code";

	command_options="";
	# Set to 1 to include the "Previous" entry and an extra space at the end
	menu_items=2;
	for i in $files
	do
		command_options="$command_options $i $i.c";
		menu_items=`expr $menu_items + 1`;
	done;

	if [ $menu_items -gt 13 ]
	then
		menu_items=13;
	fi

	# While the user selects some menu option, repeat
	statusSource=0;
	while (test "$statusSource" = "0")
	do
        dialog --clear --menu "$title" 20 60 $menu_items $command_options Previous "Return to previous screen" 2>$tmp
		resultSource=`cat $tmp`;
		statusSource=`echo $?`;

		# None of the programs need additional arguments and all exit 
		# normally (^C not required to exit)
		if [ $statusSource -eq 0 ]
		then
			if [ "$resultSource" == "Previous" ]
			then
				statusSource=1;
			else
				if [ -n  "$EDITOR" ]
				then
					$EDITOR $resultSource.c;
				else
					dialog --clear --msgbox "EDITOR environment variable is not set. Please set it to your favorite editor and rerun the program." 10 40;
					return $FALSE;
				fi
			fi
		fi
	done

	return $TRUE;
}



# runBasics: Function to run the programs in the Basics category
# Arguments: None
runBasics()
{
	local cwd;
	local progs_array;
	local title;
	local count;
	local command_options;
	local statusRunBasics;
	local resultRunBasics;
	local string_args;

	
	# Programs to run
	progs_array[1]="acs_vars";
	progs_array[2]="hello_world";
	progs_array[3]="init_func_example";
	progs_array[4]="key_code";
	progs_array[5]="mouse_menu";
	progs_array[6]="other_border";
	progs_array[7]="printw_example";
	progs_array[8]="scanw_example";
	progs_array[9]="simple_attr";
	progs_array[10]="simple_color";
	progs_array[11]="simple_key";
	progs_array[12]="temp_leave";
	progs_array[13]="win_border";
	progs_array[14]="with_chgat";


	# Save current directory
	cwd=`pwd`;

	cd $EXEC_DIR;
	if [ $? -ne 0 ]
	then
		dialog --clear --msgbox "Unable to change to $EXEC_DIR" 5 40;
		return $FALSE;
	fi

	title="Basics";

	# Number of programs
	count=14;
	command_options="";
	while [ $count -gt 0 ]
	do
		command_options="$command_options ${progs_array[$count]} ${progs_array[$count]}";
		count=`expr $count - 1`;
	done


	# While the user selects some menu option, repeat
	statusRunBasics=0;
	while (test "$statusRunBasics" = "0")
	do
        dialog --clear --menu "$title" 20 60 12 $command_options Previous "Return to previous screen" 2>$tmp
		resultRunBasics=`cat $tmp`;
		statusRunBasics=`echo $?`;

		# None of the programs except "simple_attr" need additional 
		# arguments and all exit normally (^C not required to exit)
		if [ $statusRunBasics -eq 0 ]
		then
			if [ "$resultRunBasics" == "Previous" ]
			then
				statusRunBasics=1;
			elif [ "$resultRunBasics" == "simple_attr" ]
			then
                dialog --clear --inputbox "Enter the name of a C file (pwd: demo/exe)" 10 60 2>$tmp
				string_arg=`cat $tmp`;
				if [ $? -eq 0 ]
				then
					./$resultRunBasics $string_arg 2>$TEMP_FILE;
					if [ $? -ne 0 ]
					then
						echo "
Unable to run './$resultRunBasics'" >> $TEMP_FILE;
						dialog --clear --textbox $TEMP_FILE 15 60;
					fi
				fi
			else
				./$resultRunBasics 2> $TEMP_FILE;
				if [ $? -ne 0 ]
				then
					if [ `wc -c $TEMP_FILE | awk {'print \$1'}` -ne 0 ]
					then
						echo "
Unable to run './$resultRunBasics'" >> $TEMP_FILE;
						dialog --clear --textbox $TEMP_FILE 15 60;
					fi
				fi
			fi
		fi
	done

	cd $cwd;
	if [ $? -ne 0 ]
	then
		dialog --clear --msgbox "Unable to change to $cwd" 5 40;
		return $FALSE;
	fi

	return $TRUE;
}


# runForms: Function to run the programs in the Forms category
# Arguments: None
runForms()
{
	local cwd;
	local progs_array;
	local title;
	local count;
	local command_options;
	local statusRunForms;
	local resultRunForms;



	# Programs to run
	progs_array[1]="form_attrib";
	progs_array[2]="form_options";
	progs_array[3]="form_simple";
	progs_array[4]="form_win";


	# Save current directory
	cwd=`pwd`;

	cd $EXEC_DIR;
	if [ $? -ne 0 ]
	then
		dialog --clear --msgbox "Unable to change to $EXEC_DIR" 5 40;
		return $FALSE;
	fi

	title="Forms";

	# Number of programs
	count=4;
	command_options="";
	while [ $count -gt 0 ]
	do
		command_options="$command_options ${progs_array[$count]} ${progs_array[$count]}";
		count=`expr $count - 1`;
	done


	# While the user selects some menu option, repeat
	statusRunForms=0;
	while (test "$statusRunForms" = "0")
	do
        dialog --clear --menu "$title" 20 60 7 $command_options Previous "Return to previous screen" 2>$tmp
		resultRunForms=`cat $tmp`;
		statusRunForms=`echo $?`;

		# None of the programs need additional arguments and all exit 
		# normally (^C not required to exit)
		if [ $statusRunForms -eq 0 ]
		then
			if [ "$resultRunForms" == "Previous" ]
			then
				statusRunForms=1;
			else
				./$resultRunForms 2> $TEMP_FILE;
				if [ $? -ne 0 ]
				then
					if [ `wc -c $TEMP_FILE | awk {'print \$1'}` -ne 0 ]
					then
						echo "
Unable to run './$resultRunForms'" >> $TEMP_FILE;
						dialog --clear --textbox $TEMP_FILE 15 60;
					fi
				fi
			fi
		fi
	done

	cd $cwd;
	if [ $? -ne 0 ]
	then
		dialog --clear --msgbox "Unable to change to $cwd" 5 40;
		return $FALSE;
	fi

	return $TRUE;
}


# runMenus: Function to run the programs in the Menus category
# Arguments: None
runMenus()
{
	local cwd;
	local progs_array;
	local title;
	local count;
	local command_options;
	local statusRunMenus;
	local resultRunMenus;



	# Programs to run
	progs_array[1]="menu_attrib";
	progs_array[2]="menu_item_data";
	progs_array[3]="menu_multi_column";
	progs_array[4]="menu_scroll";
	progs_array[5]="menu_simple";
	progs_array[6]="menu_toggle";
	progs_array[7]="menu_userptr";
	progs_array[8]="menu_win";


	# Save current directory
	cwd=`pwd`;

	cd $EXEC_DIR;
	if [ $? -ne 0 ]
	then
		dialog --clear --msgbox "Unable to change to $EXEC_DIR" 5 40;
		return $FALSE;
	fi

	title="Menus";

	# Number of programs
	count=8;
	command_options="";
	while [ $count -gt 0 ]
	do
		command_options="$command_options ${progs_array[$count]} ${progs_array[$count]}";
		count=`expr $count - 1`;
	done


	# While the user selects some menu option, repeat
	statusRunMenus=0;
	while (test "$statusRunMenus" = "0")
	do
        dialog --clear --menu "$title" 20 60 10 $command_options Previous "Return to previous screen" 2>$tmp
		resultRunMenus=`cat $tmp`;
		statusRunMenus=`echo $?`;

		# None of the programs need additional arguments and all exit 
		# normally (^C not required to exit)
		if [ $statusRunMenus -eq 0 ]
		then
			if [ "$resultRunMenus" == "Previous" ]
			then
				statusRunMenus=1;
			else
				./$resultRunMenus 2> $TEMP_FILE;
				if [ $? -ne 0 ]
				then
					if [ `wc -c $TEMP_FILE | awk {'print \$1'}` -ne 0 ]
					then
						echo "
Unable to run './$resultRunMenus'" >> $TEMP_FILE;
						dialog --clear --textbox $TEMP_FILE 15 60;
					fi
				fi
			fi
		fi
	done

	cd $cwd;
	if [ $? -ne 0 ]
	then
		dialog --clear --msgbox "Unable to change to $cwd" 5 40;
		return $FALSE;
	fi

	return $TRUE;
}


# runPanels: Function to run the programs in the Panels category
# Arguments: None
runPanels()
{
	local cwd;
	local progs_array;
	local title;
	local count;
	local command_options;
	local statusRunPanels;
	local resultRunPanels;



	# Programs to run
	progs_array[1]="panel_browse";
	progs_array[2]="panel_hide";
	progs_array[3]="panel_resize";
	progs_array[4]="panel_simple";


	# Save current directory
	cwd=`pwd`;

	cd $EXEC_DIR;
	if [ $? -ne 0 ]
	then
		dialog --clear --msgbox "Unable to change to $EXEC_DIR" 5 40;
		return $FALSE;
	fi

	title="Panels";

	# Number of programs
	count=8;
	command_options="";
	while [ $count -gt 0 ]
	do
		command_options="$command_options ${progs_array[$count]} ${progs_array[$count]}";
		count=`expr $count - 1`;
	done


	# While the user selects some menu option, repeat
	statusRunPanels=0;
	while (test "$statusRunPanels" = "0")
	do
        dialog --clear --menu "$title" 20 60 7 $command_options Previous "Return to previous screen" 2>$tmp
		resultRunPanels=`cat $tmp`;
		statusRunPanels=`echo $?`;

		# None of the programs need additional arguments and all exit 
		# normally (^C not required to exit)
		if [ $statusRunPanels -eq 0 ]
		then
			if [ "$resultRunPanels" == "Previous" ]
			then
				statusRunPanels=1;
			else
				./$resultRunPanels 2> $TEMP_FILE;
				if [ $? -ne 0 ]
				then
					if [ `wc -c $TEMP_FILE | awk {'print \$1'}` -ne 0 ]
					then
						echo "
Unable to run './$resultRunPanels'" >> $TEMP_FILE;
						dialog --clear --textbox $TEMP_FILE 15 60;
					fi
				fi
			fi
		fi
	done

	cd $cwd;
	if [ $? -ne 0 ]
	then
		dialog --clear --msgbox "Unable to change to $cwd" 5 40;
		return $FALSE;
	fi

	return $TRUE;
}


# runJustForFun: Function to run the programs in the JustForFun category
# Arguments: None
runJustForFun()
{
	local cwd;
	local progs_array;
	local title;
	local count;
	local command_options;
	local statusRunJustForFun;
	local resultRunJustForFun;
	local num_arg;



	# Programs to run
	progs_array[1]="hanoi";
	progs_array[2]="life";
	progs_array[3]="magic";
	progs_array[4]="queens";
	progs_array[5]="shuffle";
	progs_array[6]="tt";


	# Save current directory
	cwd=`pwd`;

	cd $EXEC_DIR;
	if [ $? -ne 0 ]
	then
		dialog --clear --msgbox "Unable to change to $EXEC_DIR" 5 40;
		return $FALSE;
	fi

	title="Just For Fun";

	# Number of programs
	count=6;
	command_options="";
	while [ $count -gt 0 ]
	do
		command_options="$command_options ${progs_array[$count]} ${progs_array[$count]}";
		count=`expr $count - 1`;
	done


	# While the user selects some menu option, repeat
	statusRunJustForFun=0;
	while (test "$statusRunJustForFun" = "0")
	do
		resultRunJustForFun=`dialog --clear --menu "$title" 20 60 10 $command_options Previous "Return to previous screen" 2>&1`;
		statusRunJustForFun=`echo $?`;

		case "$resultRunJustForFun" in
			"hanoi")
				./hanoi 2> $TEMP_FILE;
				if [ $? -ne 0 ]
				then
					echo "
Unable to run './hanoi'" >> $TEMP_FILE;
					dialog --clear --textbox $TEMP_FILE 15 60;
				fi

				;;
			"life")
				./life 2> $TEMP_FILE;
				if [ $? -ne 0 ]
				then
					if [ `wc -c $TEMP_FILE | awk {'print \$1'}` -ne 0 ]
					then
						echo "
Unable to run './hanoi'" >> $TEMP_FILE;
						dialog --clear --textbox $TEMP_FILE 15 60;
					fi
				fi
				
				;;
			"magic")
				num_arg=`dialog --clear --inputbox "Enter the size of the magic square" 10 40 2>&1`;
				if [ $? -eq 0 ]
				then
					# Check if an integer
					echo $num_arg | grep -E -e [^0-9];
					if [ $? -ne 0 ]
					then
						./magic $num_arg 2>$TEMP_FILE;
						if [ $? -ne 0 ]
						then
							echo "
Unable to run './magic'" >> $TEMP_FILE;
							dialog --clear --textbox $TEMP_FILE 15 60;
						fi
					fi
				fi

				;;
			"queens")
				num_arg=`dialog --clear --inputbox "Enter the number of qeens (chess board order) ( > 3)" 10 40 2>&1`;
				if [ $? -eq 0 ]
				then
					# Check if an integer
					echo $num_arg | grep -E -e [^0-9];
					if [ $? -ne 0 ]
					then
						./queens $num_arg 2>$TEMP_FILE;
						if [ $? -ne 0 ]
						then
							echo "
Unable to run './queens'" >> $TEMP_FILE;
							dialog --clear --textbox $TEMP_FILE 15 60;
						fi
					fi
				fi
				
				;;
			"shuffle")
				num_arg=`dialog --clear --inputbox "Enter the order of the shuffle board" 10 40 2>&1`;
				if [ $? -eq 0 ]
				then
					# Check if an integer
					echo $num_arg | grep -E -e [^0-9];
					if [ $? -ne 0 ]
					then
						./shuffle $num_arg 2>$TEMP_FILE;
						if [ $? -ne 0 ]
						then
							if [ `wc -c $TEMP_FILE | awk {'print \$1'}` -ne 0 ]
							then
								echo "
Unable to run './shuffle'" >> $TEMP_FILE;
								dialog --clear --textbox $TEMP_FILE 15 60;
							fi
						fi
					fi
				fi
				
				;;
			"tt")
				./tt 2>$TEMP_FILE;
				if [ $? -ne 0 ]
				then
					if [ `wc -c $TEMP_FILE | awk {'print \$1'}` -ne 0 ]
					then
						echo "
Unable to run './tt'" >> $TEMP_FILE;
						dialog --clear --textbox $TEMP_FILE 15 60;
					fi
				fi
				;;
			Previous)	
				statusRunJustForFun="1";
				;;
		esac
	done

	cd $cwd;
	if [ $? -ne 0 ]
	then
		dialog --clear --msgbox "Unable to change to $cwd" 5 40;
		return $FALSE;
	fi

	return $TRUE;
}



# submenu: Generic function to process submenus (display submenu for a 
#          category
# Arguments: Title, run_function
# run_function: This function is invoked when the 'Run' item is choosen
submenu()
{
	local cwdSubmenu;
	local statusSubmenu;
	local title
	local resultSubmenu;

	# Save current working directory
	cwdSubmenu=`pwd`;

	#While the user selects some menu option, repeat
	statusSubmenu=0
	title="$1";
	while (test "$statusSubmenu" = "0") 
	do
		# Create the main menu dialog box
        dialog --clear --menu "NCURSES Programming HOWTO $title Sample Programs" 20 60 8 Make "Make programs" Clean "Clean programs" Run "Run programs" Source "View source code for programs" readme "View the readme file" makefile "View the Makefile" Previous "Return to previous screen" 2>$tmp
		resultSubmenu=`cat $tmp`
		statusSubmenu=`echo $?`
		case $resultSubmenu in 
			Make)
				execMake
				if [ $? -eq 0 ]
				then
					echo "
'make' successful" >> $TEMP_FILE;
				else
					echo "
Unable to run 'make'" >> $TEMP_FILE;
				fi
				dialog --clear --textbox $TEMP_FILE 15 60;
			
				;;
			Clean)
				execMake "clean";
				if [ $? -eq 0 ]
				then
					echo "
'make clean' successful" >> $TEMP_FILE;
				else
					echo "
Unable to run 'make clean'" >> $TEMP_FILE;
				fi
				dialog --clear --textbox $TEMP_FILE 15 60;
			
				;;
			Run)
				# Run the programs: The function name passed
				# to this function as $2
				$2;
				
				;;
			Source)
				# Bring up the source code menu
				source_menu;

				;;
			readme)
				if [ -n  "$EDITOR" ]
				then
					$EDITOR README;
				else
					dialog --clear --msgbox "EDITOR environment variable is not set. Please set it to your favorite editor and rerun the program." 10 40;
				fi

				;;
			makefile)
				if [ -n  "$EDITOR" ]
				then
					$EDITOR Makefile;
				else
					dialog --clear --msgbox "EDITOR environment variable is not set. Please set it to your favorite editor and rerun the program." 10 40;
				fi

				;;
			Previous)	
				statusSubmenu="1";
				;;
		esac
	done

	return $TRUE;
}




# Code starts

# Initialize the variables
basics="basics";
forms="forms";
menus="menus";
panels="panels";
JustForFun="JustForFun";

# Save the current working directory
cwd=`pwd`;


#While the user selects some menu option, repeat
status=0
while (test "$status" = "0") 
do
	#Create the main menu dialog box
	dialog --clear --menu "NCURSES Programming HOWTO Sample Programs" 20 60 10 basics "Basics" forms "Forms" menus "Menus" panels "Panels" JustForFun "Just For Fun" makeall "Make all programs" cleanall "Make clean all programs" readme "View the readme file" makefile "View the Makefile" Quit "Quit" 2>$tmp 
	status=`echo $?`
    result=`cat $tmp`
	case $result in 
		basics)	
			cd $basics || dialog --clear --msgbox "Unable to change to directory $basics" 5 40;

			# Call the basics function
			submenu "Basics" runBasics;
			if [ $? -ne 0 ];
			then
				dialog --clear --msgbox  "Error processing basics" 5 40;
			fi
			
			# Change back to the earlier working directory
			cd $cwd;
			;;
		forms)	
			cd $forms || dialog --clear --msgbox "Unable to change to directory $forms" 5 40;

			# Call the forms function
			submenu "Forms" runForms;
			if [ $? -ne 0 ];
			then
				dialog --clear --msgbox  "Error processing forms" 5 40;
			fi
			
			# Change back to the earlier working directory
			cd $cwd;
			;;
		menus)	
			cd $menus || dialog --clear --msgbox "Unable to change to directory $menus" 5 40;

			# Call the menus function
			submenu "Menus" runMenus;
			if [ $? -ne 0 ];
			then
				dialog --clear --msgbox  "Error processing menus" 5 40;
			fi
			
			# Change back to the earlier working directory
			cd $cwd;
			;;
		panels)	
			cd $panels || dialog --clear --msgbox "Unable to change to directory $panels" 5 40;

			# Call the menus function
			submenu "Panels" runPanels;
			if [ $? -ne 0 ];
			then
				dialog --clear --msgbox  "Error processing panels" 5 40;
			fi
			
			# Change back to the earlier working directory
			cd $cwd;
			;;
		JustForFun) 
			cd $JustForFun || dialog --clear --msgbox "Unable to change to directory $JustForFun" 5 40;

			# Call the JustForFun function
			submenu "JustForFun" runJustForFun;
			if [ $? -ne 0 ];
			then
				dialog --clear --msgbox  "Error processing JustForFun" 5 40;
			fi
			
			# Change back to the earlier working directory
			cd $cwd;
			;;
		makeall)
			# Call the execMake function
			execMake;
			if [ $? -eq 0 ]
			then
				echo "
'make' successful" >> $TEMP_FILE;
			else
				echo "
Unable to run 'make'" >> $TEMP_FILE;
			fi
			dialog --clear --textbox $TEMP_FILE 15 60;
			
			;;
		cleanall)
			# Call the execMake function
			execMake "clean";
			if [ $? -eq 0 ]
			then
				echo "
'make clean' successful" >> $TEMP_FILE;
			else
				echo "
Unable to run 'make clean'" >> $TEMP_FILE;
			fi
			dialog --clear --textbox $TEMP_FILE 15 60;
			
			;;
		readme)
			if [ -n  "$EDITOR" ]
			then
				$EDITOR README;
			else
				dialog --clear --msgbox "EDITOR environment variable is not set. Please set it to your favorite editor and rerun the program." 10 40;
			fi

			;;
		makefile)
			if [ -n  "$EDITOR" ]
			then
				$EDITOR Makefile;
			else
				dialog --clear --msgbox "EDITOR environment variable is not set. Please set it to your favorite editor and rerun the program." 10 40;
			fi

			;;
		Quit)
			# Remove the TEMP_FILE
			rm -f $TEMP_FILE;
            rm -f $tmp;

			status="1";
			;;
	esac
done
