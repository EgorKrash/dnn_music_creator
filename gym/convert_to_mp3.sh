#! /bin/bash
timidity -Ow -o - $1 | lame - $2
