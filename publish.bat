:: Annoying, this actually ends up copying all the files because the destination server
:: is on a different time zone and windows will keep thinking our files are newer. Don't know how to fix...

robocopy public\2021 \\myfiles.fastmail.com@SSL\DavWWWRoot\site\2021 /MIR /R:3 /W:10 /XO /fft /copy:dat /log:publish.log /tee /ts /dst /timfix
