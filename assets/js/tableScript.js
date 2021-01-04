//asynchronously load the file, change true to false for synchronous
//https://www.artylope.com/blog/2016/12/28/load-a-local-json.html
function loadJSON(file, callback) {
    var rawFile = new XMLHttpRequest();
    rawFile.overrideMimeType("application/json");
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function() {
        if (rawFile.readyState == 4 && rawFile.status == "200") {
            callback(rawFile.responseText);
        }
    }
    rawFile.send(null);
}




function createJamesCurStocksTable(){
    
    loadJSON('jamesCurStocks.json', function(data) {
        var stockList = JSON.parse(data);
        stockList = stockList["stocks"];
           
            var myTable= "<table><tr><td style='width: 100px; color: red;'><strong>Stock</strong></td>";
            myTable+= "<td style='width: 100px; color: red; text-align: right;'><strong>10-Day % Return</strong></td>";
            myTable+="<td style='width: 100px; color: red; text-align: right;'><strong>30-Day % Return</strong></td></tr>";


              for (var i=0; i<stockList.length; i++) {
                myTable+="<tr><td style='width: 100px;'>" + stockList[i]["stock"] + ":</td>";
                
                myTable+="<td style='width: 100px; text-align: right;'>" + stockList[i]["10 day return"].toFixed(2) + "%</td>";
                myTable+="<td style='width: 100px; text-align: right;'>" + stockList[i]["30 day return"].toFixed(2) + "%</td></tr>"; 
                //if table disappears something above is wrong
            }  
            
            myTable+="</table>";

            var tempDiv = document.createElement('div');
            tempDiv.className = "inner";
            tempDiv.innerHTML = myTable;
        
            var prependedData = $('#one').children().last()[0];
            document.getElementById("one").insertBefore(tempDiv,prependedData);
    });
   
    
}