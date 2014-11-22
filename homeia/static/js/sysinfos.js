$(function loadTemp(){
    $.getJSON("/sysinfos", 
         function(data) {
             $('#time').html(data.NetTime);
             $('#temperature').html(data.temperature + ' °C');
             $('#lastReboot').html(data.lastReboot);
         }); 
    setTimeout(loadTemp,3000);
 });