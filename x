#!/bin/bash
case $1 in
	clean)
	exec=clean startx
	;;

	ob)
	exec=openbox startx
	;;

	*)
	exec="$@" startx
	;;
esac
