//asynchronously load the file, change true to false for synchronous
//https://www.artylope.com/blog/2016/12/28/load-a-local-json.html
//https://stackoverflow.com/questions/881510/sorting-json-by-values
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

function sortJSON(arr, key, way) {
    return arr.sort(function(a, b) {
        var x = a[key]; var y = b[key];
        if (way === 'descending') { return ((x < y) ? -1 : ((x > y) ? 1 : 0)); }
        if (way === 'ascending') { return ((x > y) ? -1 : ((x < y) ? 1 : 0)); }
    });
}
// ------ helper functions ------------------
var sortMethod = "stock";
var sortArrangement = "ascending";

function setStock(){
    sortMethod = "stock";
}

function set10DayReturn(){
    sortMethod = "10 day return";
}

function set30DayReturn(){
    sortMethod = "30 day return";
}

function setAscending(){
    sortArrangement = "ascending";
}
function setDescending(){
    sortArrangement = "descending";
}

function createJamesCurStocksTable(){
    
    loadJSON('jamesCurStocks.json', function(data) {
        var stockList = JSON.parse(data);
        stockList = stockList["stocks"];
        stockList = sortJSON(stockList, sortMethod, sortArrangement);
        $('#one').children().remove(".table");
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
        tempDiv.className = "table";
        tempDiv.innerHTML = myTable;
    
        var prependedData = $('#one').children().last()[0];
        document.getElementById("one").appendChild(tempDiv);
    });
    
}


function createDOWStocksTable(){
    
    loadJSON('DOWstocks.json', function(data) {
        var stockList = JSON.parse(data);
        stockList = stockList["stocks"];
        stockList = sortJSON(stockList, sortMethod, sortArrangement);
        //stockList = sortJSON(stockList, '30 day return', '321');
        //stockList = sortJSON(stockList, 'stock', '123');
        
       
        console.log(stockList)
        $('#one').children().remove(".table");
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
        tempDiv.className = "table";
        tempDiv.innerHTML = myTable;
    
        var prependedData = $('#one').children().last()[0];
        document.getElementById("one").appendChild(tempDiv);
    });
    
}
function createSandPStocksTable(){
    
    loadJSON('SandPstocks.json', function(data) {
        var stockList = JSON.parse(data);
        console.log(stockList)
        stockList = stockList["stocks"];
        stockList = sortJSON(stockList, sortMethod, sortArrangement);
        $('#one').children().remove(".table");
        var myTable= "<table><tr><td style='width: 100px; color: red;'><strong>Stock</strong></td>";
        myTable+= "<td style='width: 100px; color: red; text-align: right;'><strong>10-Day % Return</strong></td>";
        myTable+="<td style='width: 100px; color: red; text-align: right;'><strong>30-Day % Return</strong></td></tr>";


            for (var i=0; i<stockList.length; i++) {
            myTable+="<tr><td style='width: 100px;'>" + stockList[i]["stock"] + ":</td>";
            myTable+="<td style='width: 100px; text-align: right;'>" + Number(stockList[i]["10 day return"]).toFixed(2) + "%</td>";
            myTable+="<td style='width: 100px; text-align: right;'>" + Number(stockList[i]["30 day return"]).toFixed(2) + "%</td></tr>"; 
            //if table disappears something above is wrong
        }  
        
        myTable+="</table>";

        var tempDiv = document.createElement('div');
        tempDiv.className = "table";
        tempDiv.innerHTML = myTable;
    
        var prependedData = $('#one').children().last()[0];
        document.getElementById("one").appendChild(tempDiv);
    });
    
}