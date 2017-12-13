function refresh() {
    setInterval(fresh,10000);
    function fresh() {
        $("#isAsleep").text(IsAsleep);
        $("#isCrying").text(IsCrying);
        $("#sleeptime").text(getSleepTime);
        $("#sleeptemp").text(getSleepTemp);
        $("#isWet").text(IsWet);
        $("#isInbed").text(IsInBed);
    }
}

i=0;
function IsAsleep() {
    i++;
    if(i%2 == 0)
        return "否"
    if(i%2 ==1 )
        return "是"
}

function IsCrying() {
    return "nop"
}

function IsInBed() {
    return "nop"
}

function getSleepTemp() {
    return "nop"
}

function IsWet() {
    return "nop"
}

function getSleepTime(){
    return "nop"
}

