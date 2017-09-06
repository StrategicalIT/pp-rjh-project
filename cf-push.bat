cd C:\Users\richard_houghton\Documents\GitHub\pp-rjh-project
REM cf login -a https://api.run.pivotal.io -u richard_houghton@dell.com
cf push pp-light
IF /I "%ERRORLEVEL%" NEQ "0" pause