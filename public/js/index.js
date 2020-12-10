
function init() {
    var dataset = Array.apply(null, new Array(200)).map(Number.prototype.valueOf,0);
    var datasetb = Array.apply(null, new Array(200)).map(Number.prototype.valueOf,0);
    var cd = Array.apply(null, new Array(200)).map(Number.prototype.valueOf,0);
    var cdx = document.getElementById('pic_cd').getContext('2d');
    var ctx = document.getElementById('pic_hr0').getContext('2d');
    var ctxb = document.getElementById('pic_br0').getContext('2d');
    var xl = new Array(200)
    var cdch = new Chart(cdx, {
        type: 'line',
        data: {
          labels: xl,
          datasets: [{
            label: 'chest displacement',
            data: cd,
            lineTension: 0,                    
            backgroundColor:'#FF5376',     
            borderColor: '#FF5376',          
            fill: true,                    
            borderWidth: 2,        
            pointRadius: 1,           
            pointHoverRadius: 7, 
          }]
        },
        options: {
          responsive: false    
        }
    });
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: xl,
          datasets: [{
            label: 'heart rate',
            data: dataset,
            lineTension: 0,                    
            backgroundColor:'#FF5376',     
            borderColor: '#FF5376',          
            fill: false,                    
            borderWidth: 2,        
            pointRadius: 1,           
            pointHoverRadius: 7, 
          }]
        },
        options: {
          responsive: false    
        }
    });
    var chartb = new Chart(ctxb, {
        type: 'line',
        data: {
          labels: xl,
          datasets: [{
            label: 'breath rate',
            data: datasetb,
            lineTension: 0,                    
            backgroundColor:'#FF5376',     
            borderColor: '#FF5376',          
            fill: false,                    
            borderWidth: 2,        
            pointRadius: 1,           
            pointHoverRadius: 7, 
          }]
        },
        options: {
          responsive: false    
        }
    });

    var str_before_username = "<div class='my-3 p-3 bg-white rounded'>";
    var str_before_me = "<div class='container bg-purple rounded text-white-50' style=' width:30%;float:right;'><h5>";
    var str_after_content = "</h5></div></div>\n";
    function run(){
        var postsRef = firebase.database().ref('0');
        var postsRef_cd = firebase.database().ref('1/cd');
        var i = 199;
        postsRef_cd.limitToFirst(200).once('value')
            .then(function (snapshot) { 
                snapshot.forEach(function (childSnapshot) {
                    var childData = childSnapshot.val();
                    cd[i] = childData;
                    i = i - 1;
                });
            })
            .catch(e => console.log(e.message));
        postsRef.once('value')
            .then(function (snapshot) {
                snapshot.forEach(function(childSnapshot) {
                    var key = childSnapshot.key;
                    var childData = childSnapshot.val();
                    if(key=="breath rate"){
                        datasetb = datasetb.slice(1, 200);
                        datasetb.push(parseFloat(childData));
                        document.getElementById('br_txt').innerHTML = parseFloat(childData).toFixed(4);
                    }
                    else if(key=="heart rate"){
                        dataset = dataset.slice(1, 200);
                        dataset.push(parseFloat(childData));
                        document.getElementById('hr_txt').innerHTML = parseFloat(childData).toFixed(4);
                    }
                    /*else if(key=="cd"){
                        dataset = dataset.slice(1, 200);
                        dataset.push(parseFloat(childData));
                        document.getElementById('cd_txt').innerHTML = parseFloat(childData).toFixed(4) ;
                    }*/
                    else if(key=="stat"){
                        if(parseInt(childData)==0){
                            document.getElementById('stat').innerHTML = "<h1 style='font-size:72px;color:red;text-align: center;'>alert</h1>";
                        }
                        else if(parseInt(childData)==1){
                            document.getElementById('stat').innerHTML = "<h1 style='font-size:72px;color:black;text-align: center;'>human</h1>";
                        }
                        else if(parseInt(childData)==2){
                            document.getElementById('stat').innerHTML = "<h1 style='font-size:72px;color:black;text-align: center;'>move</h1>";
                        }
                    }
                });
            })
            .catch(e => console.log(e.message));
        //setTimeout(run, 1000); 
        chart.data.datasets[0].data=dataset;
        chart.update();
        chartb.data.datasets[0].data=datasetb;
        chartb.update();
        cdch.data.datasets[0].data=cd;
        cdch.update();
    }
    setInterval(run, 1000);

}
window.onload = function () {
    init();
};