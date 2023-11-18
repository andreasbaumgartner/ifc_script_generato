chcp 1252
    del \*.ifc

    "C:\Program Files\Trimble\nova16\Nova.exe" /writeIfc:"sql-adznova.antec.local:NovaProjects::";"";"" 
    timeout /t 5 /nobreak
    ren \*Lueftung_alle*.ifc Lueftung_alle.ifc
    xcopy \Lueftung_alle.ifc "" /Y
    