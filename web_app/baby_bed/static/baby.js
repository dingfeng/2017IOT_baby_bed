function refresh() {
    fresh();
    setInterval(fresh,10000);
    //etInterval(updateHistory,1000);
    function fresh() {
        //
        IsAsleep();
        IsCrying();
        IsInBed();
        getSleepTemp();
        getSleepTime();
        IsWet();
        getRows();
    }
}


function IsAsleep() {   
    $.ajax({url:"http://127.0.0.1:8001/isSleeping",async:true,dataType:"json",success:function(data){
        //alert(data.res);
        $("#isAsleep").text(data.res);
    }});
    
    
}

function IsCrying() {
    $.ajax({url:"http://127.0.0.1:8001/isCry",async:true,dataType:"json",success:function(data){
        //alert(data.res);
        $("#isCrying").text(data.res);
    }});
}

function IsInBed() {
    $.ajax({url:"http://127.0.0.1:8001/inBed",async:true,dataType:"json",success:function(data){
        //alert(data.res);
        $("#isInbed").text(data.res);
    }});
}

function getSleepTemp() {
    $.ajax({url:"http://127.0.0.1:8001/temp",async:true,dataType:"json",success:function(data){
        //alert(data.res);
        $("#sleeptemp").text(data.res);
    }});
}

function IsWet() {
    $.ajax({url:"http://127.0.0.1:8001/bed-wetting",async:true,dataType:"json",success:function(data){
        //alert(data.res);
        $("#isWet").text(data.res);
    }});
}

function getSleepTime(){
    $.ajax({url:"http://127.0.0.1:8001/sleepTime",async:true,dataType:"json",success:function(data){
        //alert(data.res);
        $("#sleeptime").text(data.res);
    }});
}

$("#open").click(function(){
    $.ajax({url:"http://127.0.0.1:8001/on",async:true,success:function(){
        alert("开启成功");
        //$("#sleeptime").text(data.res);
    }});
});

$("#close").click(function(){
    $.ajax({url:"http://127.0.0.1:8001/off",async:true,success:function(){
        alert("关闭成功");
        //$("#sleeptime").text(data.res);
    }});
});

function updateHistory(rows){
  google.charts.load("current", {packages:["timeline"]});
  google.charts.setOnLoadCallback(drawChart);
  function drawChart() {

    var container = document.getElementById('chart');
    var chart = new google.visualization.Timeline(container);
    var dataTable = new google.visualization.DataTable();
    dataTable.addColumn({ type: 'string', id: 'Position' });
    dataTable.addColumn({ type: 'string', id: 'Name' });
    dataTable.addColumn({ type: 'date', id: 'Start' });
    dataTable.addColumn({ type: 'date', id: 'End' });
    dataTable.addRows(rows);
    
    var options = {
      colors: ['#bce8f1', '#faebcc', '#d6e9c6'],
    };
    chart.draw(dataTable,options);
  }
}



function getRows(){
    $.ajax({url:"http://127.0.0.1:8001/history",async:true,dataType:"json",success:function(result){
        var rows = new Array();
        var i = 0;
        var length = result.data.length;
        //alert(length);
        $.each(result.data,function(index,value){
            //alert(value.action_type);
            var row=new Array();
            row[0]='Status',
            row[1]=value.action_type;
            row[2]=new Date(value.time);
            if( i < length-1){
                row[3]=new Date(result.data[i+1].time);
            }
            else{
                row[3]=new Date();
            }
            //alert(row[3]);
            //row[3]=
            rows[i]=row;
            i++;
        });
        //alert(rows);
        updateHistory(rows);
    }});

}


