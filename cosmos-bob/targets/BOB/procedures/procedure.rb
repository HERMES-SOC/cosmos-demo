# Script Runner test script
cmd("BOB EXAMPLE")
wait_check("BOB STATUS BOOL == 'FALSE'", 5)
